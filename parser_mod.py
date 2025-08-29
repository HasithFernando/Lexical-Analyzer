# parser_mod.py

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        if node:
            self.children.append(node)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            token_node = Node(f"{token_type}:{self.current_token[1]}")
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return token_node
        else:
            expected = token_type
            found = self.current_token[0] if self.current_token else 'EOF'
            raise SyntaxError(f'Expected {expected} but found {found}')

    def parse(self):
        tree = self.E()
        if self.current_token is not None:
            raise SyntaxError(f'Unexpected token {self.current_token}')
        return tree

    # E → T E´
    def E(self):
        node = Node('E')
        node.add_child(self.T())
        node.add_child(self.E_prime())
        return node

    # E´ → + T E´ | ε
    def E_prime(self):
        node = Node("E'")
        while self.current_token and self.current_token[0] == 'PLUS':
            node.add_child(self.eat('PLUS'))
            node.add_child(self.T())
        return node

    # T → F T´
    def T(self):
        node = Node('T')
        node.add_child(self.F())
        node.add_child(self.T_prime())
        return node

    # T´ → * F T´ | ε
    def T_prime(self):
        node = Node("T'")
        while self.current_token and self.current_token[0] == 'MULT':
            node.add_child(self.eat('MULT'))
            node.add_child(self.F())
        return node

    # F → (E) | id
    def F(self):
        node = Node('F')
        if self.current_token[0] == 'LPAREN':
            node.add_child(self.eat('LPAREN'))
            node.add_child(self.E())
            node.add_child(self.eat('RPAREN'))
        elif self.current_token[0] == 'ID':
            node.add_child(self.eat('ID'))
        else:
            raise SyntaxError(f'Unexpected token {self.current_token}')
        return node
