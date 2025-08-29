import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
from lexer import lex
from parser_mod import Parser
from symboltable import format_symbol_table
from treeviz import render_tree

class ExprGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lexical Analyzer & Parser")
        self.geometry("800x600")
        self.configure(bg="#1e1e2f")
        self.resizable(True, True)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', background="#1e1e2f", foreground="#ffffff", font=("Helvetica", 12, "bold"))
        self.style.configure('Header.TLabel', font=("Helvetica", 16, "bold"))
        self.style.configure('Section.TLabel', font=("Helvetica", 12, "bold"))
        self.style.configure('TButton', font=("Helvetica", 12, "bold"), padding=10)
        self.style.configure('Green.TButton', background="#4caf50", foreground="white")
        self.style.configure('Red.TButton', background="#f44336", foreground="white")
        self.style.map('Green.TButton', background=[('active', '#45a049')])
        self.style.map('Red.TButton', background=[('active', '#e53935')])
        self.style.configure('TEntry', fieldbackground="#292b36", foreground="#ffffff", insertcolor="#ffffff")
        self.style.configure('TFrame', background="#1e1e2f")

        self.text_font = font.Font(family="Courier", size=10)

        # Title Label
        ttk.Label(self, text="Lexical Analyzer & Top-Down Parser", style='Header.TLabel').pack(pady=15)

        # Main content frame
        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Input Frame
        input_frame = ttk.Frame(main_frame, style='TFrame')
        input_frame.pack(fill="x", pady=5)
        input_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(input_frame, text="Enter Expression:", style='Section.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.input_entry = ttk.Entry(input_frame, font=self.text_font)
        self.input_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        # Buttons Frame
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill="x", pady=5)
        analyze_btn = ttk.Button(btn_frame, text="Analyze", command=self.analyze, style='Green.TButton', width=15)
        analyze_btn.pack(side="left", padx=10)
        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_all, style='Red.TButton', width=15)
        clear_btn.pack(side="left", padx=10)

        # Status Label
        self.status_label = ttk.Label(main_frame, text="", style='TLabel')
        self.status_label.pack(pady=5)

        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill="x", pady=5)

        # Output Notebook (Tabs for better organization)
        output_notebook = ttk.Notebook(main_frame)
        output_notebook.pack(fill="both", expand=True)

        # Tokens Tab
        tokens_frame = ttk.Frame(output_notebook, style='TFrame')
        output_notebook.add(tokens_frame, text="Tokens & Lexemes")
        self.tokens_text = scrolledtext.ScrolledText(tokens_frame, height=10, font=self.text_font, bg="#292b36", fg="#ffffff", insertbackground="#ffffff", borderwidth=1, relief="solid")
        self.tokens_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Symbol Table Tab
        symbol_frame = ttk.Frame(output_notebook, style='TFrame')
        output_notebook.add(symbol_frame, text="Symbol Table")
        self.symbol_text = scrolledtext.ScrolledText(symbol_frame, height=10, font=self.text_font, bg="#292b36", fg="#ffffff", insertbackground="#ffffff", borderwidth=1, relief="solid")
        self.symbol_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Parse Tree Tab
        tree_frame = ttk.Frame(output_notebook, style='TFrame')
        output_notebook.add(tree_frame, text="Parse Tree")
        self.tree_text = scrolledtext.ScrolledText(tree_frame, height=10, font=self.text_font, bg="#292b36", fg="#ffffff", insertbackground="#ffffff", wrap=tk.NONE, borderwidth=1, relief="solid")
        self.tree_text.pack(fill="both", expand=True, padx=10, pady=10)

        # About Tab
        about_frame = ttk.Frame(output_notebook, style='TFrame')
        output_notebook.add(about_frame, text="About")
        about_text_content = """This is a Lexical Analyzer & Top-Down Parser for expressions based on the following grammar:

    • E  →  TE´ 
    • E´ →  +TE´|Ɛ 
    • T  →  FT´ 
    • T´ →  *FT´|Ɛ 
    • F  →  (E)|id 
    • id →  0|1|2|3|4|5|6|7|8|9| a … z | A … Z 

Developed by:

Group N
    • Hasith Fernando 
    • Rumesha Harshan
    • Harshana Bandara
    • Dinesh Pethiyagoda"""
        self.about_text = scrolledtext.ScrolledText(about_frame, height=10, font=self.text_font, bg="#292b36", fg="#ffffff", insertbackground="#ffffff", wrap=tk.WORD, borderwidth=1, relief="solid")
        self.about_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.about_text.insert(tk.END, about_text_content)
        self.about_text.configure(state='disabled')

        # Make text areas read-only by default
        self.tokens_text.configure(state='disabled')
        self.symbol_text.configure(state='disabled')
        self.tree_text.configure(state='disabled')

    def clear_all(self):
        self.input_entry.delete(0, tk.END)
        self._clear_text(self.tokens_text)
        self._clear_text(self.symbol_text)
        self._clear_text(self.tree_text)
        self.status_label.config(text="")

    def _clear_text(self, text_widget):
        text_widget.configure(state='normal')
        text_widget.delete("1.0", tk.END)
        text_widget.configure(state='disabled')

    def analyze(self):
        expr = self.input_entry.get()
        self._clear_text(self.tokens_text)
        self._clear_text(self.symbol_text)
        self._clear_text(self.tree_text)
        self.status_label.config(text="")
        try:
            tokens, symbol_table = lex(expr)
            # Tokens & Lexemes
            self._insert_text(self.tokens_text, "\n".join(f"{t[0]} -> {t[1]}" for t in tokens))
            # Symbol Table
            self._insert_text(self.symbol_text, format_symbol_table(symbol_table))
            # Parse Tree
            parser = Parser(tokens)
            parse_tree = parser.parse()
            self._insert_text(self.tree_text, render_tree(parse_tree))
            self.status_label.config(text="Expression Accepted ✅", foreground="green")
        except Exception as e:
            self.status_label.config(text=f"Expression Rejected ❌\n{str(e)}", foreground="red")

    def _insert_text(self, text_widget, content):
        text_widget.configure(state='normal')
        text_widget.insert(tk.END, content)
        text_widget.configure(state='disabled')


if __name__ == "__main__":
    app = ExprGUI()
    app.mainloop()

    