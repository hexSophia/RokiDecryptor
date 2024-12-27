import subprocess
import os
import netifaces
import ipaddress
import concurrent.futures
import shutil
import time
import shlex

def get_local_ip_and_subnet():
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    ip_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
    ip_address = ip_info['addr']
    netmask = ip_info['netmask']
    return ip_address, netmask

def can_connect_with_password(ip, admpass):
    path_to_check = f"\\\\{ip}\\c$"
    cmd = ["net", "use", path_to_check, admpass, "/user:Administrator", "/Y"]
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        if result.returncode == 0:
            print(f"Successfully connected to {ip}")
            return True
        else:
            print(f"Failed to connect to {ip}")
            return False
    except subprocess.TimeoutExpired:
        print(f"Connection to {ip} timed out")
        return False

def is_reachable(ip, timeout=1000):
    try:
        result = subprocess.run(
            ["ping", str(ip), "-n", "1", "-w", str(timeout)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return "TTL=" in result.stdout
    except subprocess.TimeoutExpired:
        print(f"Ping to {ip} timed out")
        return False

def multi_threaded_ping_scan(admpass):
    local_ip, netmask = get_local_ip_and_subnet()
    network = ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
    
    print(f"Local IP: {local_ip}")
    print(f"Subnet Mask: {netmask}")
    print(f"Scanning network range: {network}")
    
    reachable_ips = []
    connectable_ips = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(is_reachable, ip): ip for ip in network.hosts() if str(ip) != local_ip}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    print(f"{ip} is reachable")
                    reachable_ips.append(str(ip))
                else:
                    print(f"{ip} is not reachable")
            except Exception as e:
                print(f"Error pinging {ip}: {e}")
    
    subprocess.run(["net", "use", "*", "/delete", "/Y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {executor.submit(can_connect_with_password, ip, admpass): ip for ip in reachable_ips}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    connectable_ips.append(str(ip))
                else:
                    print(f"Cannot connect to {ip}")
            except Exception as e:
                print(f"Error connecting to {ip}: {e}")
    
    print("\nScan completed.")
    print("Connectable IPs (excluding local):", connectable_ips)
    return connectable_ips

def copy_to_ip(ip, source_folder, dest_folder):
    dest_path = f"\\\\{ip}\\{dest_folder}"
    cmd = ["robocopy", source_folder, dest_path, "/njh", "/njs", "/b", "/r:0", "/w:5"]
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        if result.returncode <= 7:
            print(f"Files copied successfully to {ip}")
        else:
            print(f"Failed to copy files to {ip}")
    except subprocess.TimeoutExpired:
        print(f"Copy operation to {ip} timed out")

def execute_remote_command(ip, processtostart, param, admpass):
    params = shlex.split(param)
    cmd = [".\\PsExec\\PsExec.exe", f"\\\\{ip}", "-nobanner", "-accepteula", "-u", "Administrator", "-p", admpass, "-sdi", processtostart] + params
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    admpass = input("Administrator Password: ")
    reachable_ips = multi_threaded_ping_scan(admpass)

    tmp_tag = "C:\\tag"
    tmp_command = "C:\\command"

    tags_list = ["Shutdown", "Reboot", "QWRB", "ape", "atmp", "achd", "WRB", "mtmp", "mdmadmshow", "mdmhide", 
                 "mdmRemoteExe", "mdmRemoteUpdate", "mdmRemoteUpdateTest", "CopyRokiSetting", "Openfw", "Closefw", 
                 "MakeMacList", "addVeyon", "addVeyon2", "addVeyonN", "addVeyonN2"]

    print("Available Tags:", ", ".join(tags_list))

    while True:
        for folder in [tmp_tag, tmp_command]:
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            os.mkdir(folder)
        
        tag = input("Enter tag (or 'RCE' for Remote Command Execution): ").strip()
        
        if tag == "RCE":
            processtostart = input("Process to start: ").strip()
            if processtostart == "chrome":
                processtostart = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                param = input("URL: ")
            else:
                param = input("Parameters: ").strip()
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(execute_remote_command, ip, processtostart, param, admpass) for ip in reachable_ips]
            print("Remote command execution tasks dispatched.\n")
        elif tag in tags_list:
            open(os.path.join(tmp_tag, f"Roki_{tag}.txt"), "w").close()
            time.sleep(0.5)
            dest = "c$\\Windows\\System32\\Roki\\tag"
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(copy_to_ip, ip, tmp_tag, dest) for ip in reachable_ips]
            print("File copy tasks dispatched.\n")
        else:
            print("Invalid tag entered.")

if __name__ == "__main__":
    main()
