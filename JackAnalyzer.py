import sys

from src.compilation_engine import CompilationEngine
from src.tokenizer import Tokenizer


class JackAnalyzer:
    def __init__(self, path: str):
        self.compilation_engine = CompilationEngine(path)

    def compile(self):
        self.compilation_engine.compile()


if __name__ == '__main__':
    JackAnalyzer(sys.argv[1]).compile()
