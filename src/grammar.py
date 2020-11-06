import re

from src.constants import symbols, keywords

string_constant_re = re.compile(r'"([^"\n]*)"')

int_constant_re = re.compile(r'\d+')

identifier_re = re.compile(r'_*[a-zA-Z]+[a-zA-Z0-9_]*')

symbols_prepared = "\\" + '\\'.join(symbols)
symbol_re = re.compile(fr'[{symbols_prepared}]{{1}}')

keywords_prepared = '(' + '|'.join(keywords) + ')\W'
keywords_re = re.compile(fr'{keywords_prepared}')

inline_comment_re = re.compile(r'\/\/.*$')

# *? means non-greedy *, match as less as possible
block_comment_re = re.compile(r'\/\*.*?\*\/', re.DOTALL | re.MULTILINE | re.U)
