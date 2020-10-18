# 90s Kids
Author: syyntax &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 150 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Category: SQL

## Problem description

According to conversations found in Ghost Town, r34p3r despises 90s kids and tends to target them in his attacks. How many users in the Shallow Grave SQL dump were born in October in the 1990s?

Submit the flag as flag{#}.

Use the [file](https://tinyurl.com/yxv5qbla) from Address Book.

Max attempts: 10

## Concepts
* [Regular expression](https://en.wikipedia.org/wiki/Regular_expression)
* [Python3 regex](https://docs.python.org/3/howto/regex.html)

## Solution

We are given a database dump containing the database schema and instances.
The challenge category suggests solving the task using SQL, but I thought it would
be pretty straightforward to use regex on the database dump to get the number
of users that were born in October in the 1990s.

Examining the database dump (with line numbers), we see that users are stored in the
`users` table:

```
363 CREATE TABLE `users` (
364   `user_id` int NOT NULL AUTO_INCREMENT,
365   `username` varchar(52) NOT NULL,
366   `first` varchar(52) NOT NULL,
367   `last` varchar(52) NOT NULL,
368   `middle` varchar(24) DEFAULT NULL,
369   `email` varchar(52) NOT NULL,
370   `street` varchar(52) NOT NULL,
371   `city` varchar(52) NOT NULL,
372   `state_id` int NOT NULL,
373   `zip` varchar(10) NOT NULL,
374   `gender` varchar(8) NOT NULL,
375   `dob` date NOT NULL,
(...)
```

The instances of this table are in the format:
```
390 INSERT INTO `users` VALUES (1,'housing.petty','EDWARDO','RETTA','U','housing.petty@avagor.com','4129 Pocan Rd','Camas',56,'98607','m','2001-10-01'),
(2,'ess4yste4k','COLLENE','KOEPER','T','ess4yste4k@s peedeemail.com','2306 Gahnite Ave','Navarre',41,'44662','f','2000-10-18')
(...)
```

Looking at the user instances, we see that the date of birth is stored in the
`dob` attribute. This attribute is the only one that uses a `date` format, so
it should be easy to make a regex that matches only for users born in
October in the 90s.

Considering the `dob` format `'yyyy-mm-dd'`, the regex needs to match
`'199y-10-dd'`

We can use python to solve the challenge. Python has the `re` library for regex.
The `re.findall` function will be useful:

```
>>> import re
>>> help(re.findall)
Help on function findall in module re:

findall(pattern, string, flags=0)
    Return a list of all non-overlapping matches in the string.

    If one or more capturing groups are present in the pattern, return
    a list of groups (...)
```

The following python code will help us to find the flag:

First, we import the `re` library, and read database dump line 390 into a variable, `the_line`:
```
>>> import re
>>>
>>> the_line = ""
>>> with open("../shallowgraveu.sql") as f:
...     for i, line in enumerate(f):
...         if i == 389:  # i is 0-indexed so we start at line 0 instead of 1
...             the_line = line
...             break
```

Next, we can use `re.findall` to match our regex against `the_line`.
The match variable will be a list, containing the `dob` for all users born in October
in the 1990s.

```
>>> match = re.findall("199[0-9]{1}-10-[0-9]{2}", the_line)
>>> print(match)
['1994-10-05', '1994-10-23', '1997-10-12', '1995-10-05', '1992-10-02', '1994-10-14', '1994-10-15',
 '1990-10-13', '1996-10-02', '1991-10-06', '1992-10-27', '1998-10-17', '1994-10-27', '1999-10-05',
 '1995-10-20', '1990-10-21', '1998-10-25', '1998-10-04', '1992-10-27', '1994-10-07', '1993-10-14',
 '1999-10-07', '1996-10-21', '1996-10-02', '1996-10-08', '1995-10-07', '1999-10-06', '1990-10-19',
 '1992-10-08', '1995-10-04', '1999-10-15', '1994-10-22']
```

Now, we can print the number of matching `dob`.

```
>>> print(len(match))
32
```

So now we know that 32 users were born in October in the 1990s.

Thus, according to the flag format, given in the description, the flag is \
`flag{32}`.
