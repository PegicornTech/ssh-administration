import sqlite3
import sys

# Function to retrieve username and password from the database
def retrieve_credentials(host_ip):
    try:
        conn = sqlite3.connect("ssh_info.db")
        cursor = conn.cursor()

        # Retrieve username and password based on the provided IP address
        cursor.execute("SELECT username, password FROM ssh_info WHERE host_ip=?", (host_ip,))
        result = cursor.fetchone()

        conn.close()

        return result  # Returns a tuple (username, password) or None if not found
    except sqlite3.Error as e:
        print("SQLite error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python retrieve_credentials.py <host_ip> <username> <password>")
        sys.exit(1)

    host_ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    retrieved_credentials = retrieve_credentials(host_ip)

    if retrieved_credentials:
        # Update the database with the provided username and password
        updated_username, updated_password = retrieved_credentials
        print(f"Updating credentials for host IP {host_ip}:")
        print(f"Old Username: {updated_username}, Old Password: {updated_password}")
        print(f"New Username: {username}, New Password: {password}")

        try:
            conn = sqlite3.connect("ssh_info.db")
            cursor = conn.cursor()

            cursor.execute("UPDATE ssh_info SET username=?, password=? WHERE host_ip=?", (username, password, host_ip))
            conn.commit()
            conn.close()

            print("Credentials updated successfully.")
        except sqlite3.Error as e:
            print("SQLite error:", e)
    else:
        print(f"IP address {host_ip} not found in the database.")

