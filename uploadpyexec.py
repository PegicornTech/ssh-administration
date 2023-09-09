import paramiko
import time
import argparse

def upload_and_execute_script(host, username, password, local_script_path, remote_script_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=username, password=password)
        print(f"Connected to {host}")
        
        sftp = ssh.open_sftp()
        sftp.put(local_script_path, f"/home/{username}/{remote_script_name}")
        sftp.close()
        
        print(f"Uploaded {local_script_path} to /home/{username}/{remote_script_name}")
        
        ssh_shell = ssh.invoke_shell()
        
        ssh_shell.send("sudo -i\n")
        time.sleep(1)
        
        ssh_shell.send(password + "\n")
        time.sleep(1)
        
        ssh_shell.send(f"nohup python3 /home/{username}/{remote_script_name} > script_output.log 2>&1 &\n")
        time.sleep(1)
        
        output = ssh_shell.recv(4096).decode()
        print(output)
        
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print(f"SSH error: {str(e)}")
    finally:
        ssh.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload and execute Python script via SSH")
    parser.add_argument("--host", required=True, help="Target host IP address")
    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    parser.add_argument("--local-script", required=True, help="Local path to the Python script")
    parser.add_argument("--remote-script-name", required=True, help="Name of the remote Python script")
    
    args = parser.parse_args()
    
    host = args.host
    username = args.username
    password = args.password
    local_script_path = args.local_script
    remote_script_name = args.remote_script_name
    
    upload_and_execute_script(host, username, password, local_script_path, remote_script_name)

