# junkargs
Run executable with junk data as arguments

usage: junk_args.py [-h] [--args method:count [method:count ...]] [-v] [-m] binary

Run executable with junk data as arguments.

positional arguments:
  binary                Path to executable

options:
  -h, --help            show this help message and exit
  --args method:count [method:count ...]
                        Methods to use for generating arguments along with the count, e.g., ascii:24 nonprintable:10
  -v, --verbose         Print the full commandline generated
  -m, --method-help     Show help for available methods

=======================================>

Available methods:
- ascii: Generates ASCII characters ('A')
- nonprintable: Generates non-printable characters
- formatstrings: Generates '%x' format strings
- randombinary: Generates random binary data (hex)
- randomascii: Generates random ASCII characters
- structured: Generates repeating 'ABCD'
- unicode: Generates Unicode characters
- sqlinjection: Generates SQL injection pattern
- pathtraversal: Generates path traversal attempt
- cmdinjection: Generates command injection attempt
- htmljsinjection: Generates HTML/JavaScript injection attempt
