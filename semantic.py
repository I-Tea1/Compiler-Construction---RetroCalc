from parser import Program, Assignment, Display, IfStatement, BinaryOp, Number, Identifier, ASTNode
from typing import Dict, Set

class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, str] = {} # var_name -> type (e.g., 'NUMBER')

    def declare(self, name: str, var_type: str = 'NUMBER'):
        if name not in self.symbols:
            self.symbols[name] = var_type

    def lookup(self, name: str) -> bool:
        return name in self.symbols

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast: Program):
        self.visit(ast)

    def visit(self, node: ASTNode):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.visit(stmt)
                
        elif isinstance(node, Assignment):
            self.visit(node.expression)
            self.symbol_table.declare(node.identifier)
            
        elif isinstance(node, Display):
            self.visit(node.expression)
            
        elif isinstance(node, IfStatement):
            self.visit(node.condition)
            for stmt in node.statements:
                self.visit(stmt)
                
        elif isinstance(node, BinaryOp):
            self.visit(node.left)
            self.visit(node.right)
            
        elif isinstance(node, Identifier):
            if not self.symbol_table.lookup(node.name):
                raise SemanticError(f"Semantic Error: Variable '{node.name}' used before assignment.")
                
        elif isinstance(node, Number):
            pass # Numbers are always valid
