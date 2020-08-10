# Infected

## Problem description
We intercepted a message that was trying to leak from our infrastructure with a secret flag. Ransomware was found on one of our computers, it uses zip archives as an encryption mechanism. It selectively changes two bytes in the structure, in the place that is responsible for crc32, to those that the control server will send. The archive password was hardcored in ransomd - "infected".

A team gets an additional 100 points if they describe in ls @ hexadec1mal a way to solve a task without using brute force.

Link to zip: https://mega.nz/file/f1sUAaLB#mpfkfCzWNh7AWMxoT08YincX1xW3cdfjxEWuN4ykido

## Personal note
To do this problem I decided to use Python. My attempt was based on brute force. I had not worked on a similar problem before, and finished just after the competition closed. Still, it was an interesting exercise, and a good learning experience.

## Concepts
### Zip headers
Literature:
[The structure of a PKZip file](https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html)

### Change bytes in a file using python
https://docs.python.org/3/library/mmap.html

## Commands

### Check for errors in a password protected zip file
We can use the following command in bash:  \
```$ 7z l -slt $FILE```

This command returns 0 if no errors.

(I also tried to use `$ unzip -t $FILE`, however this did not work for password protected zip files.)

## Solution
First I tried to unzip the file, but the specified password was not accepted.

Reading about zip file structure, I found that the CRC was located in byte 14-17 of the local file header. Since two bytes in this section have been altered, we need to restore the correct byte values (thus correcting the zip file error). 

I looked for a command to check for errors in the zip file (so that I would know when the error was corrected) and played around with changing the CRC in hexeditor.

Finally, I made the script, which would systematically go through two bytes at a time in the CRC and make alterations, checking if the zip file still has errors. It ensures that all possible byte values are tried in any two bytes in the CRC. When the zip file no longer has errors, the script exits, having stored a corrected version of the zip file.

```
import mmap
import subprocess
from itertools import combinations

def changeFile(file, fromRange, toRange):
    # Store the exhaustive list of any two byte values of the CRC
    comb = combinations(list(range(fromRange, toRange)), 2)
    with open(file, 'a+') as f:
        data = f.read()
        # m lets us access the individual bits of the file
        m = mmap.mmap(f.fileno(), 0)

        # Go through the exhaustive list of any two byte values of the CRC
        for i in list(comb):
            # Storing the byte indexes
            firstByte = i[0]
            secondByte = i[1]

            #Storing the original byte values (as they need to be restored later)
            origFirstByte = m[firstByte]
            origSecondByte = m[secondByte]

            # Loop to systematically change the byte values: i contains the value we will
            # set the first byte to, j contains the values of the second byte  
            for i in range(0, 256):
                for j in range(0, 256):
                    m[firstByte] = i
                    m[secondByte] = j
                    m.flush()  # Write changes to file
                    # Check if the zip file still errors, calling 7zip as a subroutine (suppressing output)
                    code = subprocess.run(["7z", "l", "-slt", file], stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL).returncode
                    if code == 0:
                        print("The right CRC sequence is:", m[fromRange:toRange])
                        m.close()
                        f.close()
                        exit(0)
            # Resetting byte values
            m[secondByte] = origSecondByte
            m[firstByte] = origFirstByte
        m.close()
        f.close()

# Call the function
changeFile('REALLY FLAG IS HERE.zip', 14, 18)
```

When the code finishes executing, we get the following output:  \
The right CRC sequence is: b'\x8a\xfaL\x0b'

Now we can get the flag:  \
`$ unzip "REALLY FLAG IS HERE.zip"` (insert password: infected)  \
`$ cat "REALLY FLAG IS HERE.txt"`  
unictf{n4ughty_crc_h4sh}
