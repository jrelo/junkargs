# JunkArgs

## Usage
```bash
junkargs.py <binary> [arguments...]
Run executable with junk data as arguments.

Positional Arguments
binary: Path to the executable.
Options
-h, --help: Show this help message and exit.
```
Description
Run a binary with arguments generated on various criteria, intermixed with user-defined arguments.

Available Generators
ascii: Generates a specified number of ASCII characters ('A').
nonprintable: Generates a specified number of non-printable characters.
formatstrings: Generates a specified number of '%x' format strings.
randombinary: Generates a specified number of random binary data (hex).
randomascii: Generates a specified number of random ASCII characters.
structured: Generates structured junk data by repeating 'ABCDEF'.
unicode: Generates a specified number of Unicode characters.
sqlinjection: Generates a specified number of characters from a SQL injection pattern.
pathtraversal: Generates a specified number of characters for a path traversal attempt.
cmdinjection: Generates a specified number of characters for a command injection attempt.
htmljsinjection: Generates a specified number of characters for an HTML/JavaScript injection attempt.
nullbytes: Generates a specified number of null bytes (as '\x00').
randomhex: Generates a specified number of random hex bytes.
file:filename: Inserts the contents of the specified file.

Example:
```
└─# ./junkargs.py ./argv ascii:10 file:wat.txt randomascii:9
Generated command: ./argv 'AAAAAAAAAA' '/tmp/tmp4y1auujy' ':az]lEs"d'
Temporary file /tmp/tmp4y1auujy contains: b'killengn\n'
Running './argv' with 10 ASCII characters ('A'), file contents from wat.txt, random ASCII characters (9 characters)
Output: Number of arguments: 4
Argument 0: ./argv
Argument 1: AAAAAAAAAA
Argument 2: /tmp/tmp4y1auujy
Argument 3: :az]lEs"d

Error: 
Return Code: 0
```
