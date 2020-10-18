import re

the_line = ""
with open("../shallowgraveu.sql") as f:
    for i, line in enumerate(f):
        if i == 389:
            the_line = line  # i is 0-indexed so we start at line 0 instead of 1
            break

match = re.findall("199[0-9]{1}-10-[0-9]{2}", the_line)
print(match)
print(len(match))
