#!/usr/bin/python
import telnetlib
import getpass
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", help="Remote host IP address")
    parser.add_argument("--user", "-u", help="Telnet username")
    parser.add_argument("--password", "-p", help="Telnet password")
    parser.add_argument("--command", "-c", help="Command to execute")
    args = parser.parse_args()

    target = args.target
    user = args.user
    password = args.password
    command = args.command

    try:
        # Create a Telnet connection
        tn = telnetlib.Telnet(target)
        tn.read_until(b"login: ")
        tn.write(user.encode("utf-8") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode("utf-8") + b"\n")

        # Wait for the shell prompt
        tn.read_until(b"$ ")

        # Execute the provided command with nohup and redirect output
        command = f'nohup {command} > output.log 2>&1 &\n'
        tn.write(command.encode("utf-8"))

        # Wait for the command to start (you can adjust the timeout as needed)
        tn.read_until(b"$ ", timeout=10)

        # Exit the Telnet session
        tn.write(b"exit\n")

        print("Command execution completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tn.close()

if __name__ == "__main__":
    main()

