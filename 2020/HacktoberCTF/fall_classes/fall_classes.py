import re

the_line = ""
with open("../shallowgraveu.sql") as f:
    for i, line in enumerate(f):
        if i == 323:
            the_line=line
            break

match = re.findall("\([0-9]{1,4},([0-9]{1,4},2),[0-9]{1,4}\)", the_line)

print(len(set(match))) # Printing matches, without duplicates
