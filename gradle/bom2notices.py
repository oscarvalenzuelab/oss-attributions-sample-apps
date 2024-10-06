import xml.etree.ElementTree as ET

def parse_sbom_to_legal_notices(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'cyclonedx': 'http://cyclonedx.org/schema/bom/1.5'}

    with open(output_file, 'w') as f:
        f.write("Legal Notices\n")
        f.write("====================\n\n")
        
        # Loop through all components in the SBOM
        for component in root.findall('cyclonedx:components/cyclonedx:component', ns):
            name = component.find('cyclonedx:name', ns).text if component.find('cyclonedx:name', ns) is not None else "Unknown"
            version = component.find('cyclonedx:version', ns).text if component.find('cyclonedx:version', ns) is not None else "Unknown"
            publisher = component.find('cyclonedx:publisher', ns).text if component.find('cyclonedx:publisher', ns) is not None else "Unknown"
            purl = component.find('cyclonedx:purl', ns).text if component.find('cyclonedx:purl', ns) is not None else "Unknown"
            
            licenses = component.findall('cyclonedx:licenses/cyclonedx:license', ns)
            license_info = []
            for license in licenses:
                license_id = license.find('cyclonedx:id', ns).text if license.find('cyclonedx:id', ns) is not None else "Unknown"
                license_url = license.find('cyclonedx:url', ns).text if license.find('cyclonedx:url', ns) is not None else "No URL provided"
                license_info.append(f"{license_id} ({license_url})")
            
            f.write(f"Component: {name}\n")
            f.write(f"Version: {version}\n")
            f.write(f"Publisher: {publisher}\n")
            f.write(f"Package URL (PURL): {purl}\n")
            f.write("Licenses:\n")
            for lic in license_info:
                f.write(f"  - {lic}\n")
            f.write("\n")

# Run the script with input and output files
parse_sbom_to_legal_notices('app/build/reports/bom.xml', 'legal_notices.txt')
