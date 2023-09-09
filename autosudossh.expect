#!/usr/bin/expect

set host [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set local_script_path [lindex $argv 3]
set remote_script_name [lindex $argv 4]

spawn python3 -c "
import paramiko
import time

def upload_and_execute_script(host, username, password, local_script_path, remote_script_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=username, password=password)
        print(f'Connected to {host}')
        
        sftp = ssh.open_sftp()
        sftp.put(local_script_path, f'/home/{username}/{remote_script_name}')
        sftp.close()
        
        print(f'Uploaded {local_script_path} to /home/{username}/{remote_script_name}')
        
        ssh_shell = ssh.invoke_shell()
        
        ssh_shell.send('sudo -i\\n')
        time.sleep(1)
        
        ssh_shell.send(password + '\\n')
        time.sleep(1)
        
        ssh_shell.send(f'nohup sh -c \\'/home/{username}/{remote_script_name}\\' > script_output.log 2>&1 &\\n')
        time.sleep(1)
        
        output = ssh_shell.recv(4096).decode()
        print(output)
        
    except paramiko.AuthenticationException:
        print('Authentication failed.')
    except paramiko.SSHException as e:
        print(f'SSH error: {str(e)}')
    finally:
        ssh.close()

if __name__ == '__main__':
    host = '{host}'
    username = '{username}'
    password = '{password}'
    local_script_path = '{local_script_path}'
    remote_script_name = '{remote_script_name}'
    
    upload_and_execute_script(host, username, password, local_script_path, remote_script_name)
"

expect ".*assword:"
send "$password\r"

expect {
    "(yes/no)?" {
        send "yes\r"
        exp_continue
    }
    eof
}
