import sqlite3
import paramiko
import sys

# Function to perform SSH keyscan and return the gathered information
def perform_ssh_keyscan(host_ip):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Perform SSH keyscan
        client.connect(host_ip, port=22, timeout=5)
        keyscan_output = client.exec_command("ssh-keyscan -t rsa localhost")

        # Extract SSH key information
        public_key_fingerprint = keyscan_output[1].read().decode("utf-8").split()[-1]
        ssh_protocol_version = keyscan_output[0].read().decode("utf-8").split()[0]

        return public_key_fingerprint, ssh_protocol_version
    except Exception as e:
        return None, None

# Function to create SQLite3 database and save SSH information
def create_and_save_database(host_ip, username, password, public_key_fingerprint, ssh_protocol_version):
    try:
        conn = sqlite3.connect("ssh_info.db")
        cursor = conn.cursor()

        # Create a table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS ssh_info
                          (host_ip TEXT PRIMARY KEY, username TEXT, password TEXT, 
                           public_key_fingerprint TEXT, ssh_protocol_version TEXT)''')

        # Insert or update SSH information
        cursor.execute('''INSERT OR REPLACE INTO ssh_info 
                          (host_ip, username, password, public_key_fingerprint, ssh_protocol_version)
                          VALUES (?, ?, ?, ?, ?)''', (host_ip, username, password,
                                                     public_key_fingerprint, ssh_protocol_version))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python ssh_info.py <host_ip> <username> <password> <public_key_fingerprint>")
        sys.exit(1)

    host_ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    public_key_fingerprint = sys.argv[4]

    ssh_protocol_version = None  # Initialize to None since it's not provided by user input

    create_and_save_database(host_ip, username, password, public_key_fingerprint, ssh_protocol_version)
    print("SSH information saved to the database for host IP:", host_ip)

