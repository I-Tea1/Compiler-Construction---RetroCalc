import argparse
import sys
from lexer import Lexer, LexerError
from parser import Parser, ParserError, print_ast
from semantic import SemanticAnalyzer, SemanticError
from ir import IRGenerator
from optimizer import Optimizer
from codegen import CodeGenerator, VirtualMachine

def process_source(source_code: str, debug: bool = False, semantic: SemanticAnalyzer = None) -> list:
    # 1. Lexical Analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    if debug:
        print("=== Lexical Analysis ===")
        lexer.print_tokens()
        print()

    # 2. Syntax Analysis
    parser = Parser(tokens)
    ast = parser.parse()

    if debug:
        print("=== Syntax Analysis ===")
        print_ast(ast)
        print()

    # 3. Semantic Analysis
    if semantic is None:
        semantic = SemanticAnalyzer()
    
    semantic.analyze(ast)

    if debug:
        print("=== Semantic Analysis ===")
        print("Symbol Table:", semantic.symbol_table.symbols)
        print()

    # 4. IR Generation
    ir_gen = IRGenerator()
    tac = ir_gen.generate(ast)

    if debug:
        print("=== Intermediate Representation (TAC) ===")
        for instr in tac:
            print(instr)
        print()

    # 5. Optimization
    optimizer = Optimizer(tac)
    optimized_tac = optimizer.optimize()

    if debug:
        print("=== Optimized TAC ===")
        for instr in optimized_tac:
            print(instr)
        print()

    return optimized_tac

def main():
    argparser = argparse.ArgumentParser(description="RetroCalc Compiler")
    argparser.add_argument("input", nargs="?", help="Input source file (.retro)")
    argparser.add_argument("-o", "--output", help="Output file for compiled TAC")
    argparser.add_argument("--debug", action="store_true", help="Show intermediate representations")
    argparser.add_argument("--interactive", action="store_true", help="Run in interactive REPL mode")
    argparser.add_argument("--run", action="store_true", help="Run the generated TAC in the Virtual Machine")

    args = argparser.parse_args()

    if args.interactive:
        print("RetroCalc REPL - Type 'exit' to quit")
        vm_memory = {}
        repl_semantic = SemanticAnalyzer()
        while True:
            try:
                line = input(">> ")
                if line.strip().lower() == 'exit':
                    break
                if not line.strip():
                    continue
                
                tac = process_source(line, debug=args.debug, semantic=repl_semantic)
                vm = VirtualMachine(tac)
                vm.memory = vm_memory # Persist memory across REPL lines
                vm.run()
                vm_memory = vm.memory
            except (LexerError, ParserError, SemanticError) as e:
                print(e)
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")
        return

    if not args.input:
        argparser.print_help()
        sys.exit(1)

    with open(args.input, 'r') as f:
        source_code = f.read()

    tac = process_source(source_code, debug=args.debug)

    if args.output:
        codegen = CodeGenerator(tac)
        codegen.generate_file(args.output)
        if args.debug:
            print(f"TAC written to {args.output}")

    if args.run or not args.output:
        if args.debug:
            print("=== Execution Output ===")
        vm = VirtualMachine(tac)
        vm.run()

if __name__ == "__main__":
    main()
