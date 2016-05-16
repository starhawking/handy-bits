#!/usr/bin/env python
# -*- coding: utf-8 -*
# Collin M. 2016-05-16
# ziggit@starhawking.com

'''
I was giving a colleague a rundown on how to read python stacktraces the other day, and to make it clear where things were breaking in my hypothetical scenario,
I would use fuckshitup.py to indicate what function was raising the error. It seemed like it would be fun to have an actual fuckshitup.py that would
show a fun emoji and raise an exception. And thus, here we are!
'''

import random

TABLE_FLIPS=[u'(╯°□°）╯︵ ┻━┻',u'(┛◉Д◉)┛彡┻━┻',u'(ﾉ≧∇≦)ﾉ ﾐ ┸━┸',u'(ノಠ益ಠ)ノ彡┻━┻',u'(╯ರ ~ ರ）╯︵ ┻━┻',u'(┛ಸ_ಸ)┛彡┻━┻',u'(ﾉ´･ω･)ﾉ ﾐ ┸━┸',u'(ノಥ,_｣ಥ)ノ彡┻━┻',u'(┛✧Д✧))┛彡┻━┻']

class AngryError(Exception):
    def __str__(self):
        return repr("Something got Angry")

def main(angry_stuffs):
    angry_choice=random.randint(0,len(angry_stuffs)-1)
    
    print '\n%s\n' % (angry_stuffs[angry_choice])

    raise AngryError()

if __name__ == "__main__":
    main(TABLE_FLIPS)
