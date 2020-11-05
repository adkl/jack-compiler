import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from src.enumerations import TokenType
from src.tokenizer import Tokenizer


class CompilationEngine:
    def __init__(self, path: str):
        self.file_paths_to_compile = self.__get_paths_to_compile(path)
        self.is_directory = Path(path).is_dir()

    def compile(self, export_xml: bool = True):
        for file_path in self.file_paths_to_compile:
            self.compile_file(file_path, export_xml)

    def compile_file(self, file_path: str, export_xml: bool = True):
        tokenizer = Tokenizer(file_path)

        data = ET.Element('tokens')
        data.tail = '\n'

        while tokenizer.has_more_tokens():
            tokenizer.advance()

            token_element = ET.SubElement(data, tokenizer.token_type.value)

            token = None
            if tokenizer.token_type == TokenType.symbol:
                token = tokenizer.symbol

            if tokenizer.token_type == TokenType.identifier:
                token = tokenizer.identifier

            if tokenizer.token_type == TokenType.int_constant:
                token = tokenizer.int_val

            if tokenizer.token_type == TokenType.string_constant:
                token = tokenizer.string_val

            if tokenizer.token_type == TokenType.keyword:
                token = tokenizer.keyword

            token_element.text = f' {token} '
            token_element.tail = '\n'

        if export_xml:
            tokens = ET.tostring(data).decode('UTF-8')

            xml = open(str(Path(file_path).with_suffix('.xml')), 'w')
            xml.write(tokens)

    def __get_paths_to_compile(self, path: str) -> List[str]:
        os_path = Path(path)

        if os_path.is_dir():
            return [str(entry) for entry in os_path.iterdir() if entry.suffix == '.jack']

        return [path]
