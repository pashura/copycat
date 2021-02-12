from distutils import util

from lxml import etree, objectify


class XMLParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def parse(self):
        tree = etree.fromstring(self.xml_file)
        tree = etree.ElementTree(tree)
        root = tree.getroot()
        doc = {}
        self.xml_to_json(root, doc, tree)
        return doc

    def xml_to_json(self, elem, parent, tree):
        if not parent:
            parent['name'] = elem.tag
            parent['location'] = tree.getpath(elem)
            parent['children'] = []
            for child in list(elem):
                self.xml_to_json(child, parent, tree)
        else:
            this = {'name': elem.tag, 'location': tree.getpath(elem)}
            if elem.text and isinstance(elem.text, str) and not elem.text.isspace():
                this['text'] = elem.text
                this['length'] = len(elem.text)
                if elem.text in ["true", "false"]:
                    this['text'] = bool(util.strtobool(elem.text))
                this['type'] = self._guess_type(elem)
            if parent:
                parent['children'].append(this)
            if list(elem):
                this['children'] = []
            for child in list(elem):
                self.xml_to_json(child, this, tree)

    @staticmethod
    def _guess_type(elem) -> str:
        objectify.annotate(elem)
        dumped = objectify.dump(elem).split('*')
        return dumped[1].split('\'')[1] if len(dumped) > 0 else ''
