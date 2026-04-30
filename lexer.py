import re
from typing import List, NamedTuple, Optional

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class LexerError(Exception):
    pass

class Lexer:
    KEYWORDS = {'SET', 'TO', 'DISPLAY', 'IF', 'THEN', 'END'}
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def advance(self, step=1):
        for _ in range(step):
            if self.pos < len(self.source):
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1

    def peek(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return ''

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            char = self.peek()

            if char.isspace():
                self.advance()
                continue

            # Identifiers and Keywords
            if char.isalpha() or char == '_':
                start_col = self.column
                value = ''
                while self.pos < len(self.source) and (self.peek().isalnum() or self.peek() == '_'):
                    value += self.peek()
                    self.advance()
                
                token_type = 'KEYWORD' if value in self.KEYWORDS else 'IDENTIFIER'
                self.tokens.append(Token(token_type, value, self.line, start_col))
                continue

            # Numbers
            if char.isdigit():
                start_col = self.column
                value = ''
                is_float = False
                while self.pos < len(self.source) and (self.peek().isdigit() or self.peek() == '.'):
                    if self.peek() == '.':
                        if is_float:
                            break # Second dot, probably an error handled by parser/later or we could raise LexerError
                        is_float = True
                    value += self.peek()
                    self.advance()
                
                self.tokens.append(Token('NUMBER', value, self.line, start_col))
                continue

            # Operators and Punctuation
            start_col = self.column
            
            # Multi-character operators
            if char in '><=!':
                value = char
                self.advance()
                if self.peek() == '=':
                    value += '='
                    self.advance()
                self.tokens.append(Token('OPERATOR', value, self.line, start_col))
                continue

            if char in '+-*÷()':
                self.tokens.append(Token('OPERATOR' if char in '+-*÷' else 'PUNCTUATION', char, self.line, start_col))
                self.advance()
                continue

            # If we reach here, unrecognized character
            raise LexerError(f"Lexical Error: Unrecognized character '{char}' at line {self.line}, column {self.column}")

        self.tokens.append(Token('EOF', '', self.line, self.column))
        return self.tokens

    def print_tokens(self):
        for t in self.tokens:
            print(f"[{t.line}:{t.column}] {t.type} '{t.value}'")
