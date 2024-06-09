# junkargs

Run executable with junk data as arguments

## Usage

```bash
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

- ascii: Generates a specified number of ASCII characters ('A')
- nonprintable: Generates a specified number of non-printable characters
- formatstrings: Generates a specified number of '%x' format strings
- randombinary: Generates a specified number of random binary data (hex)
- randomascii: Generates a specified number of random ASCII characters
- structured: Generates structured junk data by repeating 'ABCDEF'
- unicode: Generates a specified number of Unicode characters
- sqlinjection: Generates a specified number of characters from a SQL injection pattern
- pathtraversal: Generates a specified number of characters for a path traversal attempt
- cmdinjection: Generates a specified number of characters for a command injection attempt
- htmljsinjection: Generates a specified number of characters for an HTML/JavaScript injection attempt
- nullbytes: Generates a specified number of null bytes (as '\\x00')
- randomhex: Generates a specified number of random hex bytes
- file:filename: Inserts the contents of the specified file
