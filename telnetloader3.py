import sys
import telnetlib
import argparse
import logging

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", "-i", help="path to file on local machine")
    parser.add_argument("--outfile", "-o", help="path to file remote machine")
    parser.add_argument("--target", "-t", help="remote host IP address")
    parser.add_argument("--user", "-u", help="telnet username")
    parser.add_argument("--password", "-p", help="telnet password")
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    target = args.target
    user = args.user
    password = args.password

    try:
        # Create a Telnet connection
        tn = telnetlib.Telnet(target)
        tn.read_until(b"login: ")
        tn.write(user.encode("utf-8") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode("utf-8") + b"\n")
        tn.write(b"vt100\n")

        # Transfer the file contents
        with open(infile, "r") as local_file:
            for line in local_file:
                escaped_line = escape_line(line.strip())
                command = f'echo {escaped_line} >> {outfile}\n'
                tn.write(command.encode("utf-8"))

        print(tn.read_all().decode("utf-8"))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        try:
            # Close the Telnet connection
            tn.close()
        except Exception as e:
            logging.error(f"Error while closing Telnet connection: {e}")

def escape_line(line):
    # Escape characters that might cause issues
    return line.replace('"', '\\"').replace("'", "\\'")

if __name__ == "__main__":
    main()

