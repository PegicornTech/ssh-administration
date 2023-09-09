#!/usr/bin/python
import paramiko
import socket
import os
import argparse

def download_file(hostname, port, username, password, remote_file, local_dir):
    # Create a Paramiko SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        client.connect(hostname, port, username, password)

        # Get the remote host's IPv4 address
        remote_ip = socket.gethostbyname(hostname)

        # Convert the IPv4 address to hexadecimal representation
        hex_address = remote_ip.replace('.', '_')

        # Local file path to save the downloaded file
        local_file = os.path.join(local_dir, f"{hex_address}_report.report")

        # Download the remote file
        sftp = client.open_sftp()
        sftp.get(remote_file, local_file)
        sftp.close()

        print(f"File downloaded as {local_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        client.close()

def main():
    parser = argparse.ArgumentParser(description="Download a file from a remote SSH server.")
    parser.add_argument("--hostname", required=True, help="Remote server hostname or IP address")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    parser.add_argument("--remote-file", required=True, help="Remote file path")
    parser.add_argument("--local-dir", required=True, help="Local directory to save the file")
    args = parser.parse_args()

    download_file(args.hostname, args.port, args.username, args.password, args.remote_file, args.local_dir)

if __name__ == "__main__":
    main()

