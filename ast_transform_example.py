#!/usr/bin/env python3
'''
Example of transforming an ast
Take any lambdas we run into and print out got called before executing them
'''

import ast

def title(message,pad=3):
    p_message = '{pad} {message} {pad}'.format(pad='~'*pad, message=message)
    if pad > 10:
        surround = '#'*len(p_message)
        newlines = '\n'*1
    else:
        surround = '~'*len(p_message)
        newlines = '\n'
    print('{newlines}{surround}\n{message}\n{surround}'.format(message=p_message,
                                                               surround=surround,
                                                               newlines=newlines))

ORIG = '''def logit(func, *args, **kwargs):
    print('Got Called')
    return func
res = map(lambda x: x, [1,2,3])
for x in res:
    print(x)'''

EXPECTED = '''
def logit(func, *args, **kwargs):
    print('Got Called')
    return func
res = map(lambda x: logit(str(x)), [1,2,3])
for x in res:
    print(x)
'''

orig = ast.parse(ORIG)
expected = ast.parse(EXPECTED)

class LambdaLogger(ast.NodeTransformer):
    def visit_Lambda(self, node):
        body = node.body
        call_logit = ast.Call(func=ast.Name(id='logit', ctx=ast.Load()), args=[body], keywords=[])
        node.body = call_logit
        return node

orig_ast = ast.dump(orig)
new = LambdaLogger().visit(orig)
ast.fix_missing_locations(new)
new_ast = ast.dump(new)

expected_ast = ast.dump(expected)

original_exec = compile(ORIG, filename="<ast>", mode="exec")
altered_exec = compile(new, filename="<ast>", mode="exec")
expected_exec = compile(expected, filename="<ast>", mode="exec")


title('Original Code', pad=20)
print(ORIG)

title('AST Dumps',pad=20)
title('Original')
print(orig_ast)

title('Expected')
print(expected_ast)

title('New')
print(new_ast)

title('Results', pad=20)
title('Original')
exec(original_exec)

title('Expected')
exec(expected_exec)

title('New')
exec(altered_exec)
