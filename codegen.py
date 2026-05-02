from ir import TACInstruction
from typing import List

class CodeGenerator:
    def __init__(self, instructions: List[TACInstruction]):
        self.instructions = instructions

    def generate_file(self, filename: str):
        with open(filename, 'w') as f:
            for instr in self.instructions:
                f.write(str(instr) + '\n')

class VirtualMachine:
    def __init__(self, instructions: List[TACInstruction]):
        self.instructions = instructions
        self.memory = {}
        self.pc = 0
        self.labels = {}
        
        # Pre-process labels
        for i, instr in enumerate(self.instructions):
            if instr.op == "LABEL":
                self.labels[instr.result] = i

    def get_val(self, arg: str) -> float:
        try:
            return float(arg)
        except ValueError:
            return self.memory.get(arg, 0.0)

    def run(self):
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            
            if instr.op == "ASSIGN":
                self.memory[instr.result] = self.get_val(instr.arg1)
            elif instr.op in ("+", "-", "*", "÷"):
                val1 = self.get_val(instr.arg1)
                val2 = self.get_val(instr.arg2)
                res = 0
                if instr.op == "+": res = val1 + val2
                elif instr.op == "-": res = val1 - val2
                elif instr.op == "*": res = val1 * val2
                elif instr.op == "÷": res = val1 / val2 if val2 != 0 else 0
                self.memory[instr.result] = res
            elif instr.op in (">", "<", ">=", "<=", "==", "!="):
                val1 = self.get_val(instr.arg1)
                val2 = self.get_val(instr.arg2)
                res = 0
                if instr.op == ">": res = 1 if val1 > val2 else 0
                elif instr.op == "<": res = 1 if val1 < val2 else 0
                elif instr.op == ">=": res = 1 if val1 >= val2 else 0
                elif instr.op == "<=": res = 1 if val1 <= val2 else 0
                elif instr.op == "==": res = 1 if val1 == val2 else 0
                elif instr.op == "!=": res = 1 if val1 != val2 else 0
                self.memory[instr.result] = res
            elif instr.op == "PRINT":
                val = self.get_val(instr.arg1)
                # Format to int if it's a whole number
                if val == int(val):
                    print(int(val))
                else:
                    print(val)
            elif instr.op == "IFFALSE":
                val = self.get_val(instr.arg1)
                if val == 0:
                    self.pc = self.labels[instr.result]
                    continue
            elif instr.op == "GOTO":
                self.pc = self.labels[instr.result]
                continue
                
            self.pc += 1
