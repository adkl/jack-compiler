import sys

from src.compilation_engine import CompilationEngine
from src.tokenizer import Tokenizer


class JackAnalyzer:
    def __init__(self, path: str):
        self.compilation_engine = CompilationEngine(path)

        tokenizer = Tokenizer(None)

    def build_xml(self):
        self.compilation_engine.compile_to_xml()


if __name__ == '__main__':
    JackAnalyzer(None).build_xml()
