#!/usr/bin/python
import paramiko
import argparse

def upload_file(host, username, password, local_file_path, remote_dir):
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        
        sftp = paramiko.SFTPClient.from_transport(transport)
        remote_file_path = remote_dir + '/' + local_file_path.split('/')[-1]
        
        sftp.put(local_file_path, remote_file_path)
        print(f"Uploaded {local_file_path} to {remote_file_path}")
        
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a file via SFTP")
    parser.add_argument("--host", required=True, help="SSH server host")
    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    parser.add_argument("--local-file-path", required=True, help="Local file path")
    parser.add_argument("--remote-dir", required=True, help="Remote directory path")
    
    args = parser.parse_args()
    
    host = args.host
    username = args.username
    password = args.password
    local_file_path = args.local_file_path
    remote_dir = args.remote_dir
    
    upload_file(host, username, password, local_file_path, remote_dir)

