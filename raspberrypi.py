import paramiko
import time
import argparse

def ssh_and_update(host, username, password):
    # Connect to the remote host
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=username, password=password)
        print(f"Connected to {host} and added to known hosts.")
        
        # Open a shell
        ssh_shell = ssh.invoke_shell()
        
        # Send sudo -i command
        ssh_shell.send("sudo -i\n")
        time.sleep(1)  # Wait for the prompt
        
        # Send password for sudo
        ssh_shell.send(password + "\n")
        time.sleep(1)  # Wait for the password to be processed
        
        # Send apt-get update command
        ssh_shell.send("apt-get update -y\n")
        time.sleep(1)  # Wait for the update to complete
        
        # Receive and print the output
        output = ssh_shell.recv(4096).decode()
        print(output)
        
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print(f"SSH error: {str(e)}")
    finally:
        ssh.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH and update script")
    parser.add_argument("--host", required=True, help="Target host IP address")
    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    
    args = parser.parse_args()
    
    host = args.host
    username = args.username
    password = args.password
    
    ssh_and_update(host, username, password)
