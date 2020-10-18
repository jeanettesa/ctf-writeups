# Fall Classes
Author: syyntax &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 100 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Category: SQL

## Problem description

Without counting duplicates, how many courses are being offered in the FALL2020
term at Shallow Grave University? \
Submit the flag in the following format:
flag{#}

Use the [file](https://tinyurl.com/yxv5qbla) from Address Book.

Max attempts: 10

## Concepts
* [Regular expression](https://en.wikipedia.org/wiki/Regular_expression)
* [Python3 regex](https://docs.python.org/3/howto/regex.html)

## Solution

We are given a database dump containing the database schema and instances.
The challenge category suggests solving the task using SQL, but I thought it would
be pretty straightforward to use regex on the database dump to get the number of courses
offered in the FALL2020 semester.

Examining the database dump (with line numbers), we see that courses and terms are stored in the
`term_courses` table:

```
303 CREATE TABLE `term_courses` (
304   `term_crs_id` int NOT NULL AUTO_INCREMENT,
305   `course_id` int NOT NULL,
306   `term_id` int NOT NULL,
307   `instructor` int NOT NULL,
(...)
```

The instances of this table are in the format:
```
324 INSERT INTO `term_courses` VALUES (1,6547,1,130),(2,6804,1,491),(3,6233,2,171)
(...)
```

To find courses offered in the FALL2020 term, we need to find out the `term_id`
of `FALL2020`.

```
$ grep "FALL2020" shallowgraveu.sql
INSERT INTO `terms` VALUES (1,'SPRING2020','2020-04-06','2020-07-20','Spring semester 2020'),
(2,'FALL2020','2020-08-03','2020-11-20','Fall semester 2020');
```

So FALL2020 has `term_id=2`.

Now we can make a regex that matches against the instances of `term_courses` added
in line 324.

As a reminder, `term_courses` instances are in the format: \
`(term_crs_id,course_id,term_id,instructor)`

Therefore, the regex should match the following format: \
`(Num,num,2,num)`

However, we should only extract pairs matching `course_id,term_id` (for this
purpose we will add a capture group to the regex).

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

First, we import the `re` library, and read database dump line 324 into a variable, `the_line`:
```
>>> import re
>>>
>>> the_line=""
>>> with open("../shallowgraveu.sql") as f:
...     for i, line in enumerate(f):
...         if i == 323:  # i is 0-indexed so we start at line 0 instead of 1
...             the_line=line
...             break
```

Next, we can use `re.findall` to match our regex against `the_line`.
Due to embedding course_id and term_id in parentheses in the regex (thus using a capture group),
the match variable will be a list, containing all matching `'course_id,term_id'` pairs.
```
>>> match = re.findall("\([0-9]{1,4},([0-9]{1,4},2),[0-9]{1,4}\)", the_line)
>>> print(match)
['6233,2', '6468,2', '6157,2', '6469,2', '6187,2', '5936,2', '6243,2', (...), ]
```

To remove duplicate pairs in the `match` variable, we transform it from a list to a set,
before printing the number of matching 'course_id,term_id' instances.

```
>>> len(set(match))
401
```

So now we know that 401 courses were offered in the FALL2020 semester.

Thus, according to the flag format, given in the description, the flag is \
`flag{401}`
