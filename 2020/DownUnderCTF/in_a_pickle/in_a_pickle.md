# In a pickle

## Problem description
We managed to intercept communication between und3rm4t3r and his hacker friends.
However it is obfuscated using something. We just can't figure out what it is.
Maybe you can help us find the flag?

[data](https://play.duc.tf/files/5f85a352ae3eaf93f5adf9cb06074ea0/data?token=eyJ1c2VyX2lkIjoyNDc4LCJ0ZWFtX2lkIjoxMDI2LCJmaWxlX2lkIjozM30.X2dFng.hYWA6IafRlMg4Q5kKhue7CHKnik)

Category: misc. Points: 200. Tag: easy.

### data
``
(dp0
I1
S'D'
p1
sI2
S'UCTF'
p2
sI3
S'{'
p3
sI4
I112
sI5
I49
sI6
I99
sI7
I107
sI8
I108
sI9
I51
sI10
I95
sI11
I121
sI12
I48
sI13
I117
sI14
I82
sI15
I95
sI16
I109
sI17
I51
sI18
I53
sI19
I53
sI20
I52
sI21
I103
sI22
I51
sI23
S'}'
p4
sI24
S"I know that the intelligence agency's are onto me so now i'm using ways to evade them: I am just glad that you know how to use pickle. Anyway the flag is "
p5
s.
``

## Concepts
* [Pickle](https://docs.python.org/3/library/pickle.html)
* [ASCII table](https://www.cs.cmu.edu/~pattis/15-1XX/common/handouts/ascii.html)


## Solving the challenge
The `data` file contains a pickled (serialized) Python object. Pickling converts a
Python object hierarchy into a byte stream, while unpickling is the reverse process.
To solve the challenge we need to unpickle (deserialize) the object, using the
`pickle.load(file, *, fix_imports=True, encoding='ASCII', errors='strict')`
method.

Unpickle `data` file into a variable `content`:

```
import pickle

with open('./data', 'rb') as pickle_file:
    content = pickle.load(pickle_file)
```

Examining the `content` variable:
```
>>> print(content)
{1: 'D', 2: 'UCTF', 3: '{', 4: 112, 5: 49, 6: 99, 7: 107, 8: 108, 9: 51, 10: 95,
 11: 121, 12: 48, 13: 117, 14: 82, 15: 95, 16: 109, 17: 51, 18: 53, 19: 53, 20: 52,
 21: 103, 22: 51, 23: '}', 24: "I know that the intelligence agency's are onto
 me so now i'm using ways to evade them: I am just glad that you know how to use
 pickle. Anyway the flag is "}

>>> type(content)
<class 'dict'>
```

The `content` variable is a `dict`. Looking at the values, we can identify that all values belonging to key 4-22 are stored as ASCII decimal. Thus, we need to convert the
ASCII decimals to character. In this case (since there are no other integer
values in the dict), we can convert all int values to their corresponding character
using the `chr(i)` function.

Storing the flag in a `flag` variable:
```
flag = ""
for key in sorted(content)[:-1]: # Sorting dict to ensure correct ordering. Omitting the (string) value from the last key (24)
    val = content[key]
    if isinstance(val, int):
        val = chr(val)  # Transforming ASCII decimal to character
    flag += val
```

Now we can output the flag:
```
>>> print(flag)
DUCTF{p1ckl3_y0uR_m3554g3}
```
