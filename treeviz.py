# treeviz.py

def render_tree(node, prefix="", is_last=True):
    """Recursively render the parse tree with ├─ and └─ branches."""
    if node is None:
        return ""
    
    # Choose the branch symbol
    branch = "└─ " if is_last else "├─ "
    tree_str = f"{prefix}{branch}{node.name}\n"
    
    # Prepare prefix for children
    if is_last:
        new_prefix = prefix + "   "
    else:
        new_prefix = prefix + "│  "
    
    # Render all children
    for i, child in enumerate(node.children):
        is_last_child = (i == len(node.children) - 1)
        tree_str += render_tree(child, new_prefix, is_last_child)
    
    return tree_str
