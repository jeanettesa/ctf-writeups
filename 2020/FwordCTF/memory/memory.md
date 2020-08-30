# Memory

## Problem description
Flag is: FwordCTF{computername_user_password}

Link to zip: http://download.fword.wtf/foren.7z



**Category: Forensics**

## Personal note
This was the first time I attempted a forensics challenge. It was the first time I used *volatility*, which seemed to be a really good tool for this type of challenge. Through working on the challenge, I learned a lot about types of information we can discover by memory image analysis.

## Concepts
* [Memory forensics](https://en.wikipedia.org/wiki/Memory_forensics)
* [Windows registry](https://en.wikipedia.org/wiki/Windows_Registry)

## Tools
* [Volatility](https://www.volatilityfoundation.org/releases)

## Solution
First I downloaded the zip file and extracted it:\
`$ 7z e foren.7z`

This extracts the file called *foren.raw* .

The extracted file is 2GB.

I execute `$ file foren.raw` to look for some clues as to the file type, but it only returns the generic *data* type (gives no hint as to the type of the file).

Next step is to try `$ strings foren.raw | head -200 | less`, to look at the first printable strings in the file. There are a few strings related to VMWare and a lot of strings related to Microsoft Windows. Since this is a forensics challenge called memory, I suspect this might be some type of memory image file. The problem description suggests the type of information we want to get from the file (computername, user, password).

Googling, I find that volatility is good for analyzing memory files, so I download and install it on my machine.

### Get general information

Now volatility can be used to get some information about the file: \
`$ volatility -f foren.raw imageinfo`

Some of the information returned: \
*Volatility Foundation Volatility Framework 2.6* \
*INFO    : volatility.debug    : Determining profile based on KDBG search...* \
*Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418* \
*AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)* \
*AS Layer2 : FileAddressSpace (/home/jeanette/Downloads/foren.raw)*

So it seems to be memory from Windows 7 that has been written to the file.

Now that we know the (likely) profile, we can try to get more information needed for the flag. If we get information about the virtual address of certain windows registry hives (i.e., branches of the windows registry that are stored in files), we can use this information to solve the tasks of getting the computer name, username, and password.

To get information about the computer name, we need information about *\REGISTRY\MACHINE\SYSTEM*. \
To get username and password hashes, we need information about *\REGISTRY\MACHINE\SYSTEM* and *\SystemRoot\System32\Config\SAM*.

Command to get registry hive information: \
`$ volatility -f foren.raw --profile=Win7SP1x64 hivelist`

Selected output (own emphasis): \
Virtual&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Physical&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Name \
<em><strong>0xfffff8a000024010</strong>&nbsp;&nbsp;&nbsp;&nbsp;0x000000002d07a010&nbsp;&nbsp;&nbsp;&nbsp;\REGISTRY\MACHINE\SYSTEM</em> \
<em><strong>0xfffff8a0014da410</strong>&nbsp;&nbsp;&nbsp;&nbsp;0x00000000275c0410&nbsp;&nbsp;&nbsp;&nbsp;\SystemRoot\System32\Config\SAM</em>



### Get computer name
To get the computer name, we can use the following command (the -o argument is a reference to the virtual address of \REGISTRY\MACHINE\SYSTEM): \
`$ volatility -f foren.raw --profile=Win7SP1x64 printkey -o 0xfffff8a000024010 -K 'ControlSet001\Control\ComputerName\ComputerName'`

Selected output: \
*REG_SZ        ComputerName    : (S) FORENWARMUP*

So now we know that the computer name needed for the flag is **FORENWARMUP**.

### Get username and password
To get the username and password hashes, we can use the following command (the -y argument is a reference to the virtual address of \REGISTRY\MACHINE\SYSTEM, the -s argument is a reference to the virtual address of \SystemRoot\System32\Config\SAM): \
`$ volatility -f foren.raw --profile=Win7SP1x64 hashdump -y 0xfffff8a000024010 -s 0xfffff8a0014da410`

This command results in the following output (the username is at the start of each row, and the hash is at the end of each row [before the three last ':'-separators]): \
*Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
fwordCTF:1000:aad3b435b51404eeaad3b435b51404ee:a9fdfa038c4b75ebc76dc855dd74f0da:::
HomeGroupUser$:1002:aad3b435b51404eeaad3b435b51404ee:514fab8ac8174851bfc79d9a205a939f:::
SBA_AK:1004:aad3b435b51404eeaad3b435b51404ee:a9fdfa038c4b75ebc76dc855dd74f0da:::*

At first I thought fwordCTF was the user needed for the flag, but looking at the list of process environment variables suggests that it is another user that is using the system:

`$ volatility -f foren.raw --profile=Win7SP1x64 envars | grep 'C:\\Users'`

Selected output: \
*Pid&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Process&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Block&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Variable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Value \
2516&nbsp;&nbsp;&nbsp;chrome.exe&nbsp;&nbsp;&nbsp;0x0000000000a31320&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;USERPROFILE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;C:\Users\SBA_AK \
3992&nbsp;&nbsp;&nbsp;chrome.exe&nbsp;&nbsp;&nbsp;0x0000000000931320&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;APPDATA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;C:\Users\SBA_AK\AppData\Roaming \
3992&nbsp;&nbsp;&nbsp;chrome.exe&nbsp;&nbsp;&nbsp;0x0000000000931320&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCALAPPDATA&nbsp;&nbsp;&nbsp;C:\Users\SBA_AK\AppData\Local*

So, it seems that the user needed for the flag is **SBA_AK**.

Next, we can use the hash to get the password from the site [crackstation](https://crackstation.net/).
Crackstation uses a pre-computed lookup table to crack password hashes, storing a mapping from hash to password.
Thus, if the hash is mapped to the password in the lookup table, it is very quick to find the password.

From the crackstation website, we can enter the hash (*a9fdfa038c4b75ebc76dc855dd74f0da*), and click the 'Crack Hashes' button, and the password is found:

*Hash&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Type&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Result \
a9fdfa038c4b75ebc76dc855dd74f0da&nbsp;&nbsp;&nbsp;&nbsp;NTLM&nbsp;&nbsp;&nbsp;&nbsp;password123*

Thus, the password needed for the flag is **password123**.

### Flag

Now, we can construct the flag, following the format given in the challenge description: \
FwordCTF{computername_user_password}

Inserting the computername, user, and password, we finally know the flag:

**FwordCTF{FORENWARMUP_SBA_AK_password123}**
