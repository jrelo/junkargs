#!/usr/bin/env python3

import subprocess
import os
import argparse
import random
import string
import binascii
import sys
import tempfile

def run_binary(binary, args, description):
    temp_files = []
    processed_args = []
    temp_file_contents = []

    for arg in args:
        if isinstance(arg, bytes):
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(arg)
            temp_files.append(temp_file.name)
            processed_args.append(temp_file.name)
            temp_file_contents.append(arg)
        else:
            processed_args.append(arg)

    # Always print verbose output
    formatted_command = [binary] + [repr(arg) for arg in processed_args]
    print(f"Generated command: {' '.join(formatted_command)}")

    for i, content in enumerate(temp_file_contents):
        print(f"Temporary file {temp_files[i]} contains: {content!r}")

    result = subprocess.run([binary] + processed_args, capture_output=True, text=True)
    print(f"Running '{binary}' with {description}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    print(f"Return Code: {result.returncode}\n")

    for temp_file in temp_files:
        os.remove(temp_file)

def generate_argument(generator, count=None):
    if generator == 'ascii':
        return 'A' * count, f"{count} ASCII characters ('A')"
    elif generator == 'nonprintable':
        junk_data = ''.join(chr(i) for i in range(1, 32))
        return junk_data[:count], f"{count} non-printable characters"
    elif generator == 'formatstrings':
        fmt = "%x" * count
        return fmt, f"'%x' format strings ({count} instances)"
    elif generator == 'randombinary':
        arg = binascii.hexlify(os.urandom(count)).decode('utf-8')
        return arg, f"random binary data (hex) ({count} bytes)"
    elif generator == 'randomascii':
        arg = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=count))
        return arg, f"random ASCII characters ({count} characters)"
    elif generator == 'structured':
        sequence = "ABCDEF" * ((count + 5) // 6)
        return sequence[:count], f"structured junk data (repeating 'ABCDEF') ({count} characters)"
    elif generator == 'unicode':
        arg = ''.join(chr(0x1F600 + i) for i in range(count))
        return arg, f"Unicode characters ({count} characters)"
    elif generator == 'sqlinjection':
        arg = "' OR '1'='1'; --"[:count]
        return arg, f"SQL injection pattern ({count} characters)"
    elif generator == 'pathtraversal':
        arg = "../../etc/passwd"[:count]
        return arg, f"Path traversal ({count} characters)"
    elif generator == 'cmdinjection':
        arg = "a; ls; #"[:count]
        return arg, f"Command injection ({count} characters)"
    elif generator == 'htmljsinjection':
        arg = "<script>alert('XSS')</script>"[:count]
        return arg, f"HTML/JavaScript injection ({count} characters)"
    elif generator == 'nullbytes':
        arg = b'\x00' * count
        return arg, f"{count} null bytes (as '\\x00')"
    elif generator == 'randomhex':
        hex_bytes = os.urandom(count)
        return hex_bytes, f"random hex data ({count} bytes)"
    elif generator.startswith('file:'):
        filename = generator.split(':')[1]
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                content = file.read()
            return content, f"file contents from {filename}"
        else:
            raise ValueError(f"File not found: {filename}")
    else:
        raise ValueError(f"Unknown generator: {generator}")

def main():
    generators_help = """
Available generators:
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
"""

    parser = argparse.ArgumentParser(
        description='Run executable with junk data as arguments.',
        epilog=generators_help,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('binary', help='Path to executable')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments to pass to the executable, including junk argument generation in the form of generator:count')

    parsed_args = parser.parse_args()

    binary = parsed_args.binary
    args = parsed_args.args

    generated_args = []
    descriptions = []

    try:
        for arg in args:
            if ':' in arg:
                generator, count = arg.split(':', 1)
                if generator == 'file':
                    generated_arg, description = generate_argument(f'{generator}:{count}')
                else:
                    count = int(count)
                    generated_arg, description = generate_argument(generator, count)
                generated_args.append(generated_arg)
                descriptions.append(description)
            else:
                generated_args.append(arg)

        full_description = ', '.join(descriptions)
        run_binary(binary, generated_args, full_description)

    except ValueError as e:
        print(e)
        parser.print_help()

if __name__ == "__main__":
    main()
