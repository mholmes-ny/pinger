# successfully tested on 9/19 using "C:\Users\mholmes\Downloads\test.xlsx" test 
# data. Test on apartment network. Pinged my phone, failed test WHLRs

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
    
    # Load the Excel file and extract columns MGMT, Primary, and Secondary
    df = pd.read_excel(file_path, usecols=['MGMT', 'Primary', 'Secondary'])
    
    # Combine IPs from the three columns and drop any NaN (empty) values
    ip_addresses = pd.concat([df['MGMT'], df['Primary'], df['Secondary']]).dropna().tolist()

    # Initialize lists to hold failed and passed IPs
    failed = []
    passed = []

    # Check each IP address
    for ip in ip_addresses:
        if ping_ip(str(ip)):  # Ensure IPs are strings
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
