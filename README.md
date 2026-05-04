# Compiler-Construction---RetroCalc
“RetroCalc” is a simple high-level programming language inspired by early programmable calculators and retro computing systems. It allows users to perform arithmetic operations, store values in variables, and display results using a clean and readable syntax. The language is designed for educational purposes to demonstrate how compilers work.

# RetroCalc Python Compiler

A complete pipeline for the custom programming language "RetroCalc".
Developed for the Compiler Design course project.

## Project Structure
- `compiler.py`: Main CLI interface.
- `lexer.py`: Lexical analysis phase.
- `parser.py`: Syntax analysis (Recursive Descent).
- `semantic.py`: Symbol table & type checking.
- `ir.py`: Intermediate representation (Three-Address Code).
- `optimizer.py`: Basic constant folding optimization.
- `codegen.py`: Standalone TAC generation and Virtual Machine interpreter.
- `tests/`: 5 test files demonstrating language capabilities.

## Usage

You can use the compiler in several modes. The output target is a `.tac` intermediate representation file, which the compiler's VM can also execute.

### 1. Compile to TAC and run:
```bash
python compiler.py tests/test1.retro
```

### 2. Compile to a standalone target TAC file:
```bash
python compiler.py tests/test1.retro -o output.tac
```
*(This writes the Three-Address Code to `output.tac` and runs it).*

### 3. Debug Mode (Show All Compiler Phases):
```bash
python compiler.py tests/test2.retro --debug
```
*(Displays tokens, AST, Symbol Table, TAC, and Optimized TAC).*

### 4. Interactive Mode (REPL):
```bash
python compiler.py --interactive
```
*(Type RetroCalc code line by line to evaluate immediately).*
