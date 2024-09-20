# same as pinger but includs netbox names

import subprocess
import platform
import pandas as pd

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
    # Path to the Excel file
    file_path = r'C:\Users\mholmes\Downloads\test.xlsx'
    
    # Load the Excel file and extract columns MGMT, Primary, Secondary, and Netbox Name
    df = pd.read_excel(file_path, usecols=['Netbox Name', 'MGMT', 'Primary', 'Secondary'])
    
    # Initialize a list to store the IPs along with their corresponding Netbox Name
    ip_name_pairs = []

    # Collect (IP, Netbox Name) pairs for each column
    for col in ['MGMT', 'Primary', 'Secondary']:
        ip_name_pairs.extend(list(zip(df['Netbox Name'], df[col].dropna())))

    # Initialize lists to hold failed and passed IPs
    failed = []
    passed = []

    # Check each IP address
    for name, ip in ip_name_pairs:
        if ping_ip(str(ip)):  # Ensure IPs are strings
            failed.append((name, ip))
        else:
            passed.append((name, ip))

    # Output the lists of IPs with Netbox Name
    print("Failed IPs (timed out or 100% packet loss):")
    for name, ip in failed:
        print(f"Netbox Name: {name}, IP: {ip}")

    print("\nPassed IPs (replied):")
    for name, ip in passed:
        print(f"Netbox Name: {name}, IP: {ip}")

if __name__ == "__main__":
    main()
