import json

from lxml import etree, objectify


def xml_to_json(elem, parent, tree):
    if not parent:
        parent['name'] = str(elem.tag)

        # in case there are attributes
        # parent['attributes'] = dict(elem.attrib)
        parent['children'] = []
        for child in list(elem):
            xml_to_json(child, parent, tree)
    else:
        this = {'name': str(elem.tag)}
        if elem.attrib:
            this['attributes'] = dict(elem.attrib)
        if elem.text and any(type(elem.text) == t for t in [str, str]) \
           and not elem.text.isspace():
            this['text'] = elem.text
            this['length'] = len(elem.text)
            this['location'] = tree.getpath(elem)
            if elem.text == "true":
                this['text'] = True
            elif elem.text == "false":
                this['text'] = False
            objectify.annotate(elem)
            dumped = objectify.dump(elem).split('*')
            if len(dumped) > 0:
                this['type'] = dumped[1].split('=')[1]

        if parent:
            parent['children'].append(this)
        if list(elem):
            this['children'] = []
        for child in list(elem):
            xml_to_json(child, this, tree)


def parse_xml(xml_file):
    """Given an .xml file returns contents converted to JSON"""
    tree = etree.parse(xml_file)
    root = tree.getroot()
    doc = {}
    xml_to_json(root, doc, tree)
    return json.JSONEncoder().encode(doc)
