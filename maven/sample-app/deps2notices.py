import re
import requests
import xml.etree.ElementTree as ET

MAVEN_CENTRAL_API = "https://search.maven.org/solrsearch/select"

def fetch_package_metadata(group_id, artifact_id, version):
    """
    Fetch metadata about a Maven package from the Maven Central Repository.
    """
    query = f"g:\"{group_id}\" AND a:\"{artifact_id}\" AND v:\"{version}\""
    params = {
        "q": query,
        "rows": 1,
        "wt": "json"
    }
    
    response = requests.get(MAVEN_CENTRAL_API, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["response"]["numFound"] > 0:
            return data["response"]["docs"][0]
        else:
            print(f"No metadata found for {group_id}:{artifact_id}:{version}")
            return None
    else:
        print(f"Error fetching metadata for {group_id}:{artifact_id}:{version}. Status code: {response.status_code}")
        return None

def fetch_pom_file(group_id, artifact_id, version):
    """
    Download and parse the POM file from Maven Central to extract license and publisher information.
    """
    group_path = group_id.replace('.', '/')
    url = f"https://repo1.maven.org/maven2/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            # Parse the POM file using ElementTree
            pom_xml = response.content
            root = ET.fromstring(pom_xml)
            namespaces = {'maven': 'http://maven.apache.org/POM/4.0.0'}

            # Extract license information from the POM
            licenses = root.findall(".//maven:license", namespaces)
            license_info = []
            for license_elem in licenses:
                name = license_elem.find("maven:name", namespaces)
                url = license_elem.find("maven:url", namespaces)
                if name is not None and url is not None:
                    license_info.append((name.text, url.text))

            # Extract publisher information from <organization> or <developers>
            organization = root.find(".//maven:organization/maven:name", namespaces)
            publisher = None
            if organization is not None:
                publisher = organization.text
            else:
                # Fallback to <developers> section
                developer = root.find(".//maven:developers/maven:developer/maven:name", namespaces)
                if developer is not None:
                    publisher = developer.text
            
            # Check for parent POM if no license info found
            if not license_info:
                parent = root.find(".//maven:parent", namespaces)
                if parent is not None:
                    parent_group_id = parent.find("maven:groupId", namespaces).text
                    parent_artifact_id = parent.find("maven:artifactId", namespaces).text
                    parent_version = parent.find("maven:version", namespaces).text
                    print(f"No license found for {group_id}:{artifact_id}:{version}. Trying parent POM: {parent_group_id}:{parent_artifact_id}:{parent_version}")
                    return fetch_pom_file(parent_group_id, parent_artifact_id, parent_version)
                else:
                    print(f"No license and no parent POM found for {group_id}:{artifact_id}:{version}")
            
            return license_info, publisher
        
        except ET.ParseError as e:
            print(f"Error parsing POM file for {group_id}:{artifact_id}:{version}: {e}")
            return None, None
    else:
        print(f"Error fetching POM file for {group_id}:{artifact_id}:{version}. Status code: {response.status_code}")
        return None, None

def clean_dependency_line(line):
    """
    Clean and extract the groupId, artifactId, and version from a dependency line.
    Handles cases where the line contains extra information after the version.
    """
    clean_line = line.strip()
    match = re.match(r'([a-zA-Z0-9\.\-]+):([a-zA-Z0-9\.\-]+):jar:([0-9\.]+)', clean_line)
    
    if match:
        group_id = match.group(1)
        artifact_id = match.group(2)
        version = match.group(3)
        return group_id, artifact_id, version
    else:
        print(f"No match found in line: {clean_line}")
        return None, None, None

def generate_attribution(input_file, output_file):
    """
    Generate a legal attribution file by fetching metadata and POM files from Maven Central.
    This version includes the publisher (organization) in the output.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("Legal Notices Attribution File\n\n")
        
        for line in infile:
            group_id, artifact_id, version = clean_dependency_line(line)
            
            if group_id and artifact_id and version:
                print(f"Processing dependency {group_id}:{artifact_id}:{version}")
                
                # Fetch the POM file and extract license and publisher information
                license_info, publisher = fetch_pom_file(group_id, artifact_id, version)
                
                if license_info:
                    outfile.write(f"Package: {artifact_id}\n")
                    outfile.write(f"Version: {version}\n")
                    outfile.write(f"Group: {group_id}\n")
                    
                    for name, url in license_info:
                        outfile.write(f"License: {name}\n")
                        outfile.write(f"License URL: {url}\n")
                    
                    # Include the publisher (if found)
                    if publisher:
                        outfile.write(f"Publisher: {publisher}\n")
                    
                    outfile.write("\n---\n\n")
                else:
                    print(f"Failed to find license information for {group_id}:{artifact_id}:{version}")
            else:
                print(f"Failed to process line: {line.strip()}")

# Run the script and output debugging info
generate_attribution('dependencies.txt', 'legal_attribution.txt')
