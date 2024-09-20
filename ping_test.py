import subprocess
import platform
import re

def ping_ip(ip):
    # Determine the command based on the operating system
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]  # Ping once

    # Execute the ping command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check for "Request timed out" or 100% packet loss in the output
    if platform.system().lower() == 'windows':
        return "Request timed out." in result.stdout or "100% loss" in result.stdout
    else:
        return "100% packet loss" in result.stdout or "Destination Host Unreachable" in result.stdout

def main():
    # List of IP addresses
    ip_addresses = ["10.247.88.148", "0", "192.168.1.172"]

    # Initialize lists to hold failed and passed IPs
    failed = []
    passed = []

    # Check each IP address
    for ip in ip_addresses:
        if ping_ip(ip):
            failed.append(ip)
        else:
            passed.append(ip)

    # Output the lists of IPs
    print("Failed IPs (timed out or 100% packet loss):")
    for ip in failed:
        print(ip)

    print("\nPassed IPs (replied):")
    for ip in passed:
        print(ip)

if __name__ == "__main__":
    main()
