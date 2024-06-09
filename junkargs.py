import subprocess
import os
import argparse
import random
import string
import binascii
import sys

def run_binary(binary, args, description, verbose):
    command = [binary] + args
    if verbose:
        print(f"Generated command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Running '{binary}' with {description}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    print(f"Return Code: {result.returncode}\n")

def generate_argument(method, count):
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
        sequence = "ABCD" * ((count + 3) // 4)  # Ensure at least count characters are generated
        return sequence[:count], f"structured junk data (repeating 'ABCD') ({count} characters)"
    elif method == 'unicode':
        arg = ''.join(chr(0x1F600 + i) for i in range(count))  # Unicode emoticons
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
    else:
        raise ValueError(f"Unknown method: {method}")

def main():
    parser = argparse.ArgumentParser(description='Run executable with junk data arguments')
    parser.add_argument('binary', help='Path to executable')
    parser.add_argument('--args', nargs='+', metavar='method:count', help='Methods to use for generating arguments along with the count, e.g., ascii:24 nonprintable:10')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print the full commandline generated')

    parser.add_argument('-m', '--method-help', action='store_true', help='Show available methods')

    args, unknown = parser.parse_known_args()

    if args.method_help:
        print("Available methods:")
        print("- ascii: Generates ASCII characters ('A')")
        print("- nonprintable: Generates non-printable characters")
        print("- formatstrings: Generates '%x' format strings")
        print("- randombinary: Generates random binary data (hex)")
        print("- randomascii: Generates random ASCII characters")
        print("- structured: Generates repeating 'ABCD'")
        print("- unicode: Generates Unicode characters")
        print("- sqlinjection: Generates SQL injection pattern")
        print("- pathtraversal: Generates path traversal attempt")
        print("- cmdinjection: Generates command injection attempt")
        print("- htmljsinjection: Generates HTML/JavaScript injection attempt")
        exit()

    if unknown:
        parser.print_help()
        exit()

    if args.binary and args.args:
        generated_args = []
        descriptions = []

        try:
            for arg in args.args:
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
