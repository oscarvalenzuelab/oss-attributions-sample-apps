import xml.etree.ElementTree as ET
import importlib.metadata as metadata

def parse_bom(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define the namespace
    ns = {'cyclonedx': 'http://cyclonedx.org/schema/bom/1.5'}

    # Extract components
    components = []
    for component in root.findall('.//cyclonedx:component', ns):
        comp_info = {}

        # Get name, version, description, and purl
        comp_info['name'] = component.find('cyclonedx:name', ns).text
        comp_info['version'] = component.find('cyclonedx:version', ns).text
        comp_info['description'] = component.find('cyclonedx:description', ns).text if component.find('cyclonedx:description', ns) is not None else "No description"
        comp_info['purl'] = component.find('cyclonedx:purl', ns).text if component.find('cyclonedx:purl', ns) is not None else "No PURL"

        # Get licenses
        licenses = component.findall('.//cyclonedx:license/cyclonedx:id', ns)
        if licenses:
            comp_info['licenses'] = [license.text for license in licenses]
        else:
            comp_info['licenses'] = ["No licenses"]

        # Extract additional information (copyright, etc.)
        copyright_info = extract_copyright_from_metadata(comp_info['name'])
        comp_info['copyright'] = copyright_info if copyright_info else "No copyright information"

        components.append(comp_info)

    return components

def extract_copyright_from_metadata(package_name):
    try:
        # Use importlib.metadata to retrieve metadata from the installed package
        dist = metadata.distribution(package_name)
        metadata_info = dist.metadata

        # Extract relevant metadata
        copyright_info = []
        author = metadata_info.get('Author')
        author_email = metadata_info.get('Author-email')
        license_info = metadata_info.get('License')

        if author:
            copyright_info.append(f"Author: {author}")
        if author_email:
            copyright_info.append(f"Author Email: {author_email}")
        if license_info:
            copyright_info.append(f"License: {license_info}")

        # Check for classifiers or any extra metadata fields
        if 'Classifier' in metadata_info:
            for classifier in metadata_info.get_all('Classifier'):
                if 'copyright' in classifier.lower():
                    copyright_info.append(classifier)

        return ', '.join(copyright_info) if copyright_info else None

    except metadata.PackageNotFoundError:
        return None


def main():
    bom_file = 'bom.xml'  # Replace with your BOM file path
    components = parse_bom(bom_file)

    for component in components:
        print(f"Name: {component['name']}")
        print(f"Version: {component['version']}")
        print(f"Description: {component['description']}")
        print(f"PURL: {component['purl']}")
        print(f"Licenses: {', '.join(component['licenses'])}")
        print(f"Copyright: {component['copyright']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
