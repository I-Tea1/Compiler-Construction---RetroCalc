from parser import Program, Assignment, Display, IfStatement, BinaryOp, Number, Identifier, ASTNode
from typing import List, Tuple

class TACInstruction:
    def __init__(self, op: str, arg1: str = "", arg2: str = "", result: str = ""):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        if self.op == "ASSIGN":
            return f"{self.result} = {self.arg1}"
        elif self.op in ("+", "-", "*", "÷", ">", "<", ">=", "<=", "==", "!="):
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.op == "PRINT":
            return f"PRINT {self.arg1}"
        elif self.op == "IFFALSE":
            return f"IFFALSE {self.arg1} GOTO {self.result}"
        elif self.op == "LABEL":
            return f"{self.result}:"
        elif self.op == "GOTO":
            return f"GOTO {self.result}"
        return f"{self.op} {self.arg1} {self.arg2} {self.result}"

class IRGenerator:
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self) -> str:
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self) -> str:
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, ast: Program) -> List[TACInstruction]:
        self.visit(ast)
        return self.instructions

    def visit(self, node: ASTNode) -> str:
        if isinstance(node, Program):
            for stmt in node.statements:
                self.visit(stmt)
            return ""
            
        elif isinstance(node, Assignment):
            expr_result = self.visit(node.expression)
            self.instructions.append(TACInstruction("ASSIGN", expr_result, "", node.identifier))
            return node.identifier
            
        elif isinstance(node, Display):
            expr_result = self.visit(node.expression)
            self.instructions.append(TACInstruction("PRINT", expr_result))
            return ""
            
        elif isinstance(node, IfStatement):
            cond_result = self.visit(node.condition)
            end_label = self.new_label()
            self.instructions.append(TACInstruction("IFFALSE", cond_result, "", end_label))
            
            for stmt in node.statements:
                self.visit(stmt)
                
            self.instructions.append(TACInstruction("LABEL", "", "", end_label))
            return ""
            
        elif isinstance(node, BinaryOp):
            left_result = self.visit(node.left)
            right_result = self.visit(node.right)
            temp_var = self.new_temp()
            self.instructions.append(TACInstruction(node.operator, left_result, right_result, temp_var))
            return temp_var
            
        elif isinstance(node, Number):
            return str(node.value)
            
        elif isinstance(node, Identifier):
            return node.name
            
        return ""
