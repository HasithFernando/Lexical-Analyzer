# symboltable.py

def format_symbol_table(symbol_table):
    formatted = "Symbol Table:\n"
    formatted += "{:<10} {:<10}\n".format("Lexeme", "Token")
    formatted += "-"*20 + "\n"
    for entry in symbol_table:
        formatted += "{:<10} {:<10}\n".format(entry['lexeme'], entry['token'])
    return formatted
