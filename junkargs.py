import subprocess
import os
import argparse
import random
import string
import binascii
import sys
import tempfile

def run_binary(binary, args, description, verbose):
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

    if verbose:
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

def generate_argument(method, count=None):
    if method == 'ascii':
        return 'A' * count, f"{count} ASCII characters ('A')"
    elif method == 'nonprintable':
        junk_data = ''.join(chr(i) for i in range(1, 32))
        return junk_data[:count], f"{count} non-printable characters"
    elif method == 'formatstrings':
        fmt = "%x" * count
        return fmt, f"'%x' format strings ({count} instances)"
    elif method == 'randombinary':
        arg = binascii.hexlify(os.urandom(count)).decode('utf-8')
        return arg, f"random binary data (hex) ({count} bytes)"
    elif method == 'randomascii':
        arg = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=count))
        return arg, f"random ASCII characters ({count} characters)"
    elif method == 'structured':
        sequence = "ABCDEF" * ((count + 5) // 6)
        return sequence[:count], f"structured junk data (repeating 'ABCDEF') ({count} characters)"
    elif method == 'unicode':
        arg = ''.join(chr(0x1F600 + i) for i in range(count))
        return arg, f"Unicode characters ({count} characters)"
    elif method == 'sqlinjection':
        arg = "' OR '1'='1'; --"[:count]
        return arg, f"SQL injection pattern ({count} characters)"
    elif method == 'pathtraversal':
        arg = "../../etc/passwd"[:count]
        return arg, f"Path traversal ({count} characters)"
    elif method == 'cmdinjection':
        arg = "a; ls; #"[:count]
        return arg, f"Command injection ({count} characters)"
    elif method == 'htmljsinjection':
        arg = "<script>alert('XSS')</script>"[:count]
        return arg, f"HTML/JavaScript injection ({count} characters)"
    elif method == 'nullbytes':
        arg = b'\x00' * count
        return arg, f"{count} null bytes (as '\\x00')"
    elif method == 'randomhex':
        hex_bytes = os.urandom(count)
        return hex_bytes, f"random hex data ({count} bytes)"
    elif method.startswith('file:'):
        filename = method.split(':')[1]
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                content = file.read()
            return content, f"file contents from {filename}"
        else:
            raise ValueError(f"File not found: {filename}")
    else:
        raise ValueError(f"Unknown method: {method}")

def main():
    parser = argparse.ArgumentParser(description='Run executable with junk data as arguments.')
    parser.add_argument('binary', help='Path to executable')
    parser.add_argument('--args', nargs='+', metavar='method:count', help='Methods to use for generating arguments along with the count, e.g., ascii:24 nonprintable:10')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print the full commandline generated')
    parser.add_argument('-m', '--method-help', action='store_true', help='Show help for available methods')

    args = parser.parse_args()

    if args.method_help:
        print("Available methods:")
        print("- ascii: Generates a specified number of ASCII characters ('A')")
        print("- nonprintable: Generates a specified number of non-printable characters")
        print("- formatstrings: Generates a specified number of '%x' format strings")
        print("- randombinary: Generates a specified number of random binary data (hex)")
        print("- randomascii: Generates a specified number of random ASCII characters")
        print("- structured: Generates structured junk data by repeating 'ABCDEF'")
        print("- unicode: Generates a specified number of Unicode characters")
        print("- sqlinjection: Generates a specified number of characters from a SQL injection pattern")
        print("- pathtraversal: Generates a specified number of characters for a path traversal attempt")
        print("- cmdinjection: Generates a specified number of characters for a command injection attempt")
        print("- htmljsinjection: Generates a specified number of characters for an HTML/JavaScript injection attempt")
        print("- nullbytes: Generates a specified number of null bytes (as '\\x00')")
        print("- randomhex: Generates a specified number of random hex bytes")
        print("- file:filename: Inserts the contents of the specified file")
        return

    if args.binary and args.args:
        generated_args = []
        descriptions = []

        try:
            for arg in args.args:
                if 'file:' in arg:
                    method = arg
                    count = None
                else:
                    method, count = arg.split(':')
                    count = int(count)
                
                generated_arg, description = generate_argument(method, count)
                generated_args.append(generated_arg)
                descriptions.append(description)

            full_description = ', '.join(descriptions)
            run_binary(args.binary, generated_args, full_description, args.verbose)

        except ValueError as e:
            print(e)
            parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
