import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from src.enumerations import TokenType
from src.tokenizer import Tokenizer


class CompilationEngine:
    def __init__(self, path: str):
        self.file_paths_to_compile = self.__get_paths_to_compile(path)
        self.is_directory = Path(path).is_dir()

        self.tokenizer = None

    def compile(self, export_xml: bool = True):
        for file_path in self.file_paths_to_compile:
            self.compile_file(file_path, export_xml)

    def compile_file(self, file_path: str, export_xml: bool = True):
        self.tokenizer = Tokenizer(file_path)

        self.__compile_class()

    def __get_paths_to_compile(self, path: str) -> List[str]:
        os_path = Path(path)

        if os_path.is_dir():
            return [str(entry) for entry in os_path.iterdir() if entry.suffix == '.jack']

        return [path]

    def __compile_class(self):
        tokenizer = self.tokenizer

        tokenizer.advance()
        if tokenizer.token_type != TokenType.keyword or tokenizer.keyword != 'class':
            raise SyntaxError("The code must be wrapped inside a class.")

        tokenizer.advance()
        if tokenizer.token_type != TokenType.identifier:
            raise SyntaxError("Class name expected.")

        tokenizer.advance()
        self.__check_is_left_curly_brace(tokenizer)

        self.__compile_class_var_dec()

        self.__compile_subroutine_dec()

        self.__check_is_right_curly_brace(tokenizer)

    def __compile_class_var_dec(self):
        tokenizer = self.tokenizer

        tokenizer.advance()
        is_var = tokenizer.token_type == TokenType.keyword and tokenizer.keyword in ['static', 'field']

        if not is_var:
            return

        while is_var:
            tokenizer.advance()
            if not self.__is_type(tokenizer):
                raise SyntaxError("Invalid type in class variable declaration.")

            tokenizer.advance()
            if not tokenizer.token_type == TokenType.identifier:
                raise SyntaxError("Invalid identifier in class variable declaration.")

            self.__compile_var_name_list()
            self.__check_is_semicolon(tokenizer)

            tokenizer.advance()
            is_var = tokenizer.token_type == TokenType.keyword and tokenizer.keyword in ['static', 'field']

    def __compile_subroutine_dec(self):
        tokenizer = self.tokenizer

        is_subroutine = tokenizer.token_type == TokenType.keyword \
                        and tokenizer.keyword in ['constructor', 'function', 'method']

        if not is_subroutine:
            return

        while is_subroutine:
            tokenizer.advance()
            if not (self.__is_type(tokenizer) or tokenizer.keyword == 'void'):
                raise SyntaxError("Subroutine name should be followed by type.")

            tokenizer.advance()
            if tokenizer.token_type != TokenType.identifier:
                raise SyntaxError(f"Invalid identifier for subroutine {tokenizer.identifier}.")

            tokenizer.advance()
            self.__check_is_left_brace(tokenizer)
            self.__compile_params_list()
            self.__check_is_right_brace(tokenizer)

            tokenizer.advance()
            self.__check_is_left_curly_brace(tokenizer)

            self.__compile_var_dec()
            self.__compile_statements()

            self.__check_is_right_curly_brace(tokenizer)

            is_subroutine = tokenizer.token_type == TokenType.keyword \
                            and tokenizer.keyword in ['constructor', 'function', 'method']

    def __compile_var_dec(self):
        tokenizer = self.tokenizer

        is_var = tokenizer.token_type == TokenType.keyword and tokenizer.keyword == 'var'

        if not is_var:
            return

        while is_var:
            tokenizer.advance()
            if not self.__is_type(tokenizer):
                raise SyntaxError("Type expected")

            tokenizer.advance()
            if not tokenizer.token_type != TokenType.identifier:
                raise SyntaxError("Identifier expected")

            self.__compile_var_name_list()
            self.__check_is_semicolon(tokenizer)

    def __compile_params_list(self):
        tokenizer = self.tokenizer
        tokenizer.advance()

        if not self.__is_type(tokenizer):
            return

        tokenizer.advance()
        if not tokenizer.token_type == TokenType.identifier:
            raise SyntaxError("Identifier expected in method params declaration.")

        tokenizer.advance()
        has_next = tokenizer.token_type == TokenType.symbol and tokenizer.symbol == ','

        while has_next:
            tokenizer.advance()
            if not self.__is_type(tokenizer):
                raise SyntaxError("Type expected in method param declaration.")

            tokenizer.advance()
            if not tokenizer.token_type == TokenType.identifier:
                raise SyntaxError("Identifier expected in method params declaration.")

            tokenizer.advance()
            has_next = tokenizer.token_type == TokenType.symbol and tokenizer.symbol == ','

    def __compile_var_name_list(self):
        tokenizer = self.tokenizer
        tokenizer.advance()

        has_next = tokenizer.token_type == TokenType.symbol and tokenizer.symbol == ','

        while has_next:
            tokenizer.advance()
            if not tokenizer.token_type == TokenType.identifier:
                raise SyntaxError("Identifier expected")

            tokenizer.advance()
            has_next = tokenizer.token_type == TokenType.symbol and tokenizer.symbol == ','

    def __compile_statements(self):
        statements = {
            'let': self.__compile_let_stm,
            'do': self.__compile_do_stm,
            'if': self.__compile_if_stm,
            'else': self.__compile_else_stm,
            'while': self.__compile_while_stm
        }
        tokenizer = self.tokenizer

        has_more_statements = True
        while has_more_statements:
            if tokenizer.token_type == TokenType.keyword:
                compile_statement_method = statements.get(tokenizer.keyword)

                if not compile_statement_method:
                    raise SyntaxError("Invalid statement defined.")

                compile_statement_method()
                tokenizer.advance()

            has_more_statements = tokenizer.token_type == TokenType.keyword and tokenizer.keyword in statements.keys()

    @staticmethod
    def __is_type(tokenizer):
        return tokenizer.token_type in [TokenType.keyword, TokenType.identifier] \
               or tokenizer.keyword in ['int', 'char', 'boolean']

    @staticmethod
    def __check_is_left_curly_brace(tokenizer):
        if tokenizer.token_type != TokenType.symbol or tokenizer.symbol != '{':
            raise SyntaxError("Expected {.")

    @staticmethod
    def __check_is_right_curly_brace(tokenizer):
        if tokenizer.token_type != TokenType.symbol or tokenizer.symbol != '}':
            raise SyntaxError("Expected }.")

    @staticmethod
    def __check_is_semicolon(tokenizer):
        if tokenizer.token_type != TokenType.symbol or tokenizer.symbol != ';':
            raise SyntaxError("Semicolon expected.")

    @staticmethod
    def __check_is_left_brace(tokenizer):
        if tokenizer.token_type != TokenType.symbol or tokenizer.symbol != '(':
            raise SyntaxError("Semicolon expected.")

    @staticmethod
    def __check_is_right_brace(tokenizer):
        if tokenizer.token_type != TokenType.symbol or tokenizer.symbol != ')':
            raise SyntaxError("Semicolon expected.")
