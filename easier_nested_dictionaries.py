#!/usr/bin/python2                                                                                              
"""                                                                                                             
Example of using a fold to make it easier to deal with dictionaries within dictionaries                         
                                                                                                                
                                                                                                                
Example:                                                                                                        
>>> nested = {'some': 'output', 'with': {'lots':{'of':{'nested':'keys'}}}}                                      
>>> nested['some']                                                                                              
'output'                                                                                                        
>>> nested['with']                                                                                              
{'lots': {'of': {'nested': 'keys'}}}                                                                            
>>> nested['with']['lots']                                                                                      
{'of': {'nested': 'keys'}}                                                                                      
>>> nested['with']['lots']['of']                                                                                
{'nested': 'keys'}                                                                                              
>>> nested['with']['lots']['of']['nested']                                                                      
'keys'                                                                                                          
>>>                                                                                                             
"""



nested = {'some': 'output', 'with': {'lots':{'of':{'nested':'keys'}}}}
path = ['with','lots','of','nested']

print "\nSource Items:"
print "  * Original Dict (nested):\t{}".format(nested)
print "  * Dictionary Path (path):\t{}".format(path)
print "\n"
print 'Use a list of keys to get a value from a nested dictionary:\n  >>> reduce(lambda k,v: k.get(v), path, ne\
sted)'
val = reduce(lambda k,v: k.get(v), path, nested)
print "  {}".format(repr(val))
print
