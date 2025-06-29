import ast
import json
import sys

path = sys.argv[1]
with open(path, 'r') as f:
    tree = ast.parse(f.read(), filename=path)
widgets = []
for node in tree.body:
    value = None
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == '__all__':
                value = node.value
                break
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id == '__all__':
            value = node.value
    if value is not None:
        try:
            widgets = ast.literal_eval(value)
        except Exception:
            widgets = []
        break
if not isinstance(widgets, list):
    widgets = []
widgets = [str(x) for x in widgets]
print(json.dumps(widgets))

