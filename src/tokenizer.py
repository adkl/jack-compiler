from typing import Tuple

from src.enumerations import TokenType
from src.grammar import identifier_re, int_constant_re, symbol_re, string_constant_re, keywords_re, inline_comment_re, \
    block_comment_re


class Tokenizer:
    def __init__(self, file_path: str):
        self._token_type = None
        self._identifier = None
        self._keyword = None
        self._symbol = None
        self._int_val = None
        self._string_val = None

        self.file_path = file_path
        self.source_file = ""

        self.__remove_comments()

    def has_more_tokens(self):
        return bool(self.source_file.lstrip())

    def advance(self):
        matched = False

        # Remove any leading spaces
        self.source_file = self.source_file.lstrip()

        if not self.source_file:
            return

        keyword_matched = keywords_re.match(self.source_file)
        if keyword_matched and not matched:
            matched = True
            self._keyword = keyword_matched.group(1)
            self._token_type = TokenType.keyword
            self.__eat_matched(keyword_matched.regs[1])

        identifier_matched = identifier_re.match(self.source_file)
        if identifier_matched and not matched:
            matched = True
            self._identifier = identifier_matched.group(0)
            self._token_type = TokenType.identifier
            self.__eat_matched(identifier_matched.regs[0])

        symbol_matched = symbol_re.match(self.source_file)
        if symbol_matched and not matched:
            matched = True
            self._symbol = symbol_matched.group(0)
            self._token_type = TokenType.symbol
            self.__eat_matched(symbol_matched.regs[0])

        string_matched = string_constant_re.match(self.source_file)
        if string_matched and not matched:
            matched = True
            self._string_val = string_matched.group(1)
            self._token_type = TokenType.string_constant
            self.__eat_matched(string_matched.regs[0])

        int_matched = int_constant_re.match(self.source_file)
        if int_matched and not matched:
            matched = True
            self._int_val = int_matched.group(0)
            self._token_type = TokenType.int_constant
            self.__eat_matched(int_matched.regs[0])

        if not matched:
            raise SyntaxError(f"Token invalid at {self.source_file}")

    @property
    def token_type(self) -> TokenType:
        return self._token_type

    @property
    def identifier(self):
        return self._identifier

    @property
    def keyword(self):
        return self._keyword

    @property
    def symbol(self):
        return self._symbol

    @property
    def int_val(self):
        return self._int_val

    @property
    def string_val(self):
        return self._string_val

    def __eat_matched(self, boundaries: Tuple[int, int]):
        _, end = boundaries
        self.source_file = self.source_file[end:]

    def __remove_comments(self):
        with open(self.file_path, 'r') as f:
            for line in f.readlines():
                self.source_file += inline_comment_re.sub('', line)

        self.source_file = block_comment_re.sub('', self.source_file)
