# Lexical Analyzer & Parser GUI

## Description
This Python project implements a lexical analyzer and top-down parser for a simple arithmetic grammar. It also maintains a symbol table and generates a textual parse tree. A Tkinter GUI allows interactive input and output.

## Usage
1. Run `gui.py`.
2. Enter an expression in the input field.
3. Click "Analyze" to see:
   - Tokens & Lexemes
   - Symbol Table
   - Parse Tree
   - Acceptance / Rejection message

## Grammar
```
E 	→ 	TE´
E´	→ 	+TE´ | Ɛ
T 	→ 	FT´
T´	→ 	\*FT´ | Ɛ
F 	→ 	(E) | id
id 	→ 	0-9, a-z, A-Z
```