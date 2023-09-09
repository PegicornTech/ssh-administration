import telnetlib
import getpass
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", help="Remote host IP address")
    parser.add_argument("--user", "-u", help="Telnet username")
    parser.add_argument("--password", "-p", help="Telnet password")
    parser.add_argument("--script", "-s", help="Path to the Bash script")
    args = parser.parse_args()

    target = args.target
    user = args.user
    password = args.password
    script_path = args.script

    try:
        # Create a Telnet connection
        tn = telnetlib.Telnet(target)
        tn.read_until(b"login: ")
        tn.write(user.encode("utf-8") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode("utf-8") + b"\n")

        # Wait for the shell prompt
        tn.read_until(b"$ ")

        # Run sudo -i and wait for the root prompt
        tn.write(b"sudo -i\n")
        tn.read_until(b"Password for", timeout=10)  # Wait for sudo password prompt
        tn.write(password.encode("utf-8") + b"\n")
        tn.read_until(b"root@", timeout=10)  # Wait for root prompt

        # Execute the Bash script with nohup and redirect output
        command = f'nohup sh -c "{script_path}" > output.log 2>&1 &\n'
        tn.write(command.encode("utf-8"))

        # Wait for the script to start (you can adjust the timeout as needed)
        tn.read_until(b"$ ", timeout=10)

        # Exit the Telnet session
        tn.write(b"exit\n")

        print("Script execution completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tn.close()

if __name__ == "__main__":
    main()

