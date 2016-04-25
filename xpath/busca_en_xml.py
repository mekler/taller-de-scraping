import xml.etree.ElementTree as ET
tree = ET.parse('demo.xml')
root = tree.getroot()

for element in root.findall("."):
    print (ET.dump(element))