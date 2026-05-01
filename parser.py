from lexer import Token
from typing import List, Optional

# --- AST Nodes ---
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Assignment(ASTNode):
    def __init__(self, identifier: str, expression: ASTNode):
        self.identifier = identifier
        self.expression = expression

class Display(ASTNode):
    def __init__(self, expression: ASTNode):
        self.expression = expression

class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, statements: List[ASTNode]):
        self.condition = condition
        self.statements = statements

class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

class Number(ASTNode):
    def __init__(self, value: float):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name

class ParserError(Exception):
    pass

# --- Parser ---
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1] # EOF

    def match(self, expected_type: str, expected_value: Optional[str] = None) -> Token:
        token = self.current_token()
        if token.type == expected_type and (expected_value is None or token.value == expected_value):
            self.pos += 1
            return token
        
        expected_str = f"{expected_type}" + (f" '{expected_value}'" if expected_value else "")
        raise ParserError(f"Syntax Error at line {token.line}, column {token.column}: Expected {expected_str}, found {token.type} '{token.value}'")

    def parse(self) -> Program:
        statements = self.parse_statement_list()
        self.match('EOF')
        return Program(statements)

    def parse_statement_list(self) -> List[ASTNode]:
        statements = []
        while self.current_token().type != 'EOF' and not (self.current_token().type == 'KEYWORD' and self.current_token().value == 'END'):
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self) -> ASTNode:
        token = self.current_token()
        if token.type == 'KEYWORD':
            if token.value == 'SET':
                return self.parse_assignment()
            elif token.value == 'DISPLAY':
                return self.parse_display()
            elif token.value == 'IF':
                return self.parse_if()
        
        raise ParserError(f"Syntax Error at line {token.line}, column {token.column}: Unexpected token {token.type} '{token.value}', expected statement (SET, DISPLAY, IF)")

    def parse_assignment(self) -> Assignment:
        self.match('KEYWORD', 'SET')
        identifier_token = self.match('IDENTIFIER')
        self.match('KEYWORD', 'TO')
        expr = self.parse_expression()
        return Assignment(identifier_token.value, expr)

    def parse_display(self) -> Display:
        self.match('KEYWORD', 'DISPLAY')
        expr = self.parse_expression()
        return Display(expr)

    def parse_if(self) -> IfStatement:
        self.match('KEYWORD', 'IF')
        condition = self.parse_expression() # We allow boolean operators in expression parser
        self.match('KEYWORD', 'THEN')
        statements = self.parse_statement_list()
        self.match('KEYWORD', 'END')
        return IfStatement(condition, statements)

    def parse_expression(self) -> ASTNode:
        # Handles logic and arithmetic: lowest precedence first
        return self.parse_relational()

    def parse_relational(self) -> ASTNode:
        node = self.parse_term()
        
        while self.current_token().type == 'OPERATOR' and self.current_token().value in ('>', '<', '>=', '<=', '==', '!='):
            op = self.current_token().value
            self.match('OPERATOR', op)
            right = self.parse_term()
            node = BinaryOp(node, op, right)
            
        return node

    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        
        while self.current_token().type == 'OPERATOR' and self.current_token().value in ('+', '-'):
            op = self.current_token().value
            self.match('OPERATOR', op)
            right = self.parse_factor()
            node = BinaryOp(node, op, right)
            
        return node

    def parse_factor(self) -> ASTNode:
        node = self.parse_primary()
        
        while self.current_token().type == 'OPERATOR' and self.current_token().value in ('*', '÷'):
            op = self.current_token().value
            self.match('OPERATOR', op)
            right = self.parse_primary()
            node = BinaryOp(node, op, right)
            
        return node

    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == 'NUMBER':
            self.match('NUMBER')
            return Number(float(token.value) if '.' in token.value else int(token.value))
            
        if token.type == 'IDENTIFIER':
            self.match('IDENTIFIER')
            return Identifier(token.value)
            
        if token.type == 'PUNCTUATION' and token.value == '(':
            self.match('PUNCTUATION', '(')
            node = self.parse_expression()
            self.match('PUNCTUATION', ')')
            return node
            
        raise ParserError(f"Syntax Error at line {token.line}, column {token.column}: Expected NUMBER, IDENTIFIER or '(', found {token.type} '{token.value}'")

def print_ast(node: ASTNode, indent=""):
    if isinstance(node, Program):
        print(indent + "Program:")
        for stmt in node.statements:
            print_ast(stmt, indent + "  ")
    elif isinstance(node, Assignment):
        print(indent + f"Assignment (Var: {node.identifier})")
        print_ast(node.expression, indent + "  ")
    elif isinstance(node, Display):
        print(indent + "Display:")
        print_ast(node.expression, indent + "  ")
    elif isinstance(node, IfStatement):
        print(indent + "If:")
        print_ast(node.condition, indent + "  Condition: ")
        print(indent + "  Body:")
        for stmt in node.statements:
            print_ast(stmt, indent + "    ")
    elif isinstance(node, BinaryOp):
        print(indent + f"BinaryOp ({node.operator})")
        print_ast(node.left, indent + "  ")
        print_ast(node.right, indent + "  ")
    elif isinstance(node, Number):
        print(indent + f"Number ({node.value})")
    elif isinstance(node, Identifier):
        print(indent + f"Identifier ({node.name})")
