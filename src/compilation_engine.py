import xml.etree.ElementTree as ET

from src.enumerations import TokenType
from src.tokenizer import Tokenizer


class CompilationEngine:
    def __init__(self, path: str):
        self.path = path

        self.tokenizer = Tokenizer(None)

    def compile_to_xml(self):
        data = ET.Element('tokens')\

        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

            token_element = ET.SubElement(data, self.tokenizer.token_type.value)

            token = None
            if self.tokenizer.token_type == TokenType.symbol:
                token = self.tokenizer.symbol

            if self.tokenizer.token_type == TokenType.identifier:
                token = self.tokenizer.identifier

            if self.tokenizer.token_type == TokenType.int_constant:
                token = self.tokenizer.int_val

            if self.tokenizer.token_type == TokenType.string_constant:
                token = self.tokenizer.string_val

            if self.tokenizer.token_type == TokenType.keyword:
                token = self.tokenizer.keyword

            token_element.text = token

        tokens = str(ET.tostring(data))

        xml = open('./export.xml', 'w')
        xml.write(tokens)