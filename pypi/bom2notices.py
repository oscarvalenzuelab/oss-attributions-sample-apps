import xml.etree.ElementTree as ET

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

        components.append(comp_info)

    return components


def main():
    bom_file = 'bom.xml'  # Replace with your BOM file path
    components = parse_bom(bom_file)

    for component in components:
        print(f"Name: {component['name']}")
        print(f"Version: {component['version']}")
        print(f"Description: {component['description']}")
        print(f"PURL: {component['purl']}")
        print(f"Licenses: {', '.join(component['licenses'])}")
        print("-" * 40)

if __name__ == "__main__":
    main()
