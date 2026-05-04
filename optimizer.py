from ir import TACInstruction
from typing import List, Dict

class Optimizer:
    def __init__(self, instructions: List[TACInstruction]):
        self.instructions = instructions

    def optimize(self) -> List[TACInstruction]:
        # Apply optimizations in passes
        optimized = self.constant_folding(self.instructions)
        # We can add more passes here like dead code elimination
        return optimized

    def constant_folding(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        optimized = []
        constants: Dict[str, float] = {}

        for instr in instructions:
            if instr.op == "ASSIGN":
                # Check if we are assigning a constant
                try:
                    val = float(instr.arg1)
                    constants[instr.result] = val
                    optimized.append(instr)
                except ValueError:
                    if instr.arg1 in constants:
                        # Propagate constant
                        optimized.append(TACInstruction("ASSIGN", str(constants[instr.arg1]), "", instr.result))
                        constants[instr.result] = constants[instr.arg1]
                    else:
                        if instr.result in constants:
                            del constants[instr.result]
                        optimized.append(instr)

            elif instr.op in ("+", "-", "*", "÷", ">", "<", ">=", "<=", "==", "!="):
                # Check if both arguments are constants or known constants
                arg1_val = None
                arg2_val = None

                try: arg1_val = float(instr.arg1)
                except ValueError: arg1_val = constants.get(instr.arg1)

                try: arg2_val = float(instr.arg2)
                except ValueError: arg2_val = constants.get(instr.arg2)

                if arg1_val is not None and arg2_val is not None:
                    # Can fold
                    result_val = 0
                    if instr.op == "+": result_val = arg1_val + arg2_val
                    elif instr.op == "-": result_val = arg1_val - arg2_val
                    elif instr.op == "*": result_val = arg1_val * arg2_val
                    elif instr.op == "÷": result_val = arg1_val / arg2_val if arg2_val != 0 else 0
                    elif instr.op == ">": result_val = 1 if arg1_val > arg2_val else 0
                    elif instr.op == "<": result_val = 1 if arg1_val < arg2_val else 0
                    elif instr.op == ">=": result_val = 1 if arg1_val >= arg2_val else 0
                    elif instr.op == "<=": result_val = 1 if arg1_val <= arg2_val else 0
                    elif instr.op == "==": result_val = 1 if arg1_val == arg2_val else 0
                    elif instr.op == "!=": result_val = 1 if arg1_val != arg2_val else 0

                    constants[instr.result] = result_val
                    optimized.append(TACInstruction("ASSIGN", str(result_val), "", instr.result))
                else:
                    # Can't fold, but maybe we can propagate constants to arguments
                    new_arg1 = str(arg1_val) if arg1_val is not None else instr.arg1
                    new_arg2 = str(arg2_val) if arg2_val is not None else instr.arg2
                    
                    if instr.result in constants:
                        del constants[instr.result]
                    
                    optimized.append(TACInstruction(instr.op, new_arg1, new_arg2, instr.result))

            elif instr.op == "PRINT":
                # Propagate constant to print
                val = constants.get(instr.arg1)
                if val is not None:
                    optimized.append(TACInstruction("PRINT", str(val)))
                else:
                    optimized.append(instr)
            else:
                # Other instructions (labels, conditionals) - don't track constants across basic blocks for simplicity
                if instr.op == "LABEL":
                    constants.clear() # Simple basic block isolation
                optimized.append(instr)

        return optimized
