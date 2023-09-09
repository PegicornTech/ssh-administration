#!/usr/bin/python
import paramiko
import argparse

def run_remote_script(host, username, password, script_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        command = f"sudo -i sh -c '{script_path} > script_output.log 2>&1'"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        print("Script execution started...")
        
        # Wait for the command to complete
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print("Script execution completed successfully.")
        else:
            print(f"Script execution failed with exit code: {exit_status}")
        
        ssh.close()
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print(f"SSH error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute remote script via SSH")
    parser.add_argument("--host", required=True, help="SSH server host")
    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    parser.add_argument("--script-path", required=True, help="Path to the script on the remote server")
    
    args = parser.parse_args()
    
    host = args.host
    username = args.username
    password = args.password
    script_path = args.script_path
    
    run_remote_script(host, username, password, script_path)

