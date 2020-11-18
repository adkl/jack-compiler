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

        self._current_token_indices = (0, 0)

        self.file_path = file_path
        self.source_file = ""

        self.__remove_comments()

    def has_more_tokens(self):
        return bool(self.source_file.lstrip())

    def advance(self, eat=True):
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
            self._current_token_indices = keyword_matched.regs[1]

        identifier_matched = identifier_re.match(self.source_file)
        if identifier_matched and not matched:
            matched = True
            self._identifier = identifier_matched.group(0)
            self._token_type = TokenType.identifier
            self._current_token_indices = identifier_matched.regs[0]

        symbol_matched = symbol_re.match(self.source_file)
        if symbol_matched and not matched:
            matched = True
            self._symbol = symbol_matched.group(0)
            self._token_type = TokenType.symbol
            self._current_token_indices = symbol_matched.regs[0]

        string_matched = string_constant_re.match(self.source_file)
        if string_matched and not matched:
            matched = True
            self._string_val = string_matched.group(1)
            self._token_type = TokenType.string_constant
            self._current_token_indices = string_matched.regs[0]

        int_matched = int_constant_re.match(self.source_file)
        if int_matched and not matched:
            matched = True
            self._int_val = int_matched.group(0)
            self._token_type = TokenType.int_constant
            self._current_token_indices = int_matched.regs[0]

        if not matched:
            raise SyntaxError(f"Token invalid at {self.source_file}")

        if eat:
            self.__eat_matched(self._current_token_indices)

    def eat_current(self):
        self.__eat_matched(self._current_token_indices)

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

    def __repr__(self):
        repr_template = f"Tokenizer(type={self._token_type.value}, value=%s)"
        value = str()

        if self._token_type == TokenType.symbol:
            value = self._symbol

        if self._token_type == TokenType.identifier:
            value = self._identifier

        if self._token_type == TokenType.keyword:
            value = self._keyword

        if self._token_type == TokenType.int_constant:
            value = self._int_val

        if self._token_type == TokenType.string_constant:
            value = self._string_val

        return repr_template % value
