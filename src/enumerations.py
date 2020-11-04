from enum import Enum


class TokenType(Enum):
    identifier = 'identifier'
    symbol = 'symbol'
    string_constant = 'stringConstant'
    int_constant = 'integerConstant'
    keyword = 'keyword'
