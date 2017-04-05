"""
An example of a way to take a list of functions and apply them to an arguement from right to left.

This is incredibly /not/ pythonic, but I don't really care. I find it to be a much cleaner way to write quick code.

I prefer it to having a long string of functions calling eachother like
funcb(funca("Hello World")

Obviously this will break in various situations, but it can have some extremely handy uses, especially when combined with functools.partial
"""

import functools

funca = lambda x: x+" from funca"
funcb = lambda x: x+" and funcb"
func_list = [funcb, funca]
execlist=lambda funcs, args: functools.reduce(lambda l,r: r(l), reversed(funcs), args)

execlist(func_list, "Hello World")


# Using partial to generalize our use of our chained functions
greetings_by=functools.partial(execlist, func_list)
greetings_by("Hello World")
