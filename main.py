import psutil
import platform
import socket
import subprocess
import sys

def get_system_info():
    # Get system information
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    
    # Get CPU information
    brand = None
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if "vendor_id" in line:
                if "GenuineIntel" in line:
                    brand = "Intel"
                elif "AuthenticAMD" in line:
                    brand = "AMD"
                break
    if brand:
        print("CPU Brand:", brand)
        
    # Get GPU information
    try:
        lspci = subprocess.check_output(["lspci"], universal_newlines=True)
        if "VGA compatible controller" in lspci:
            print("GPU Support: Yes")
    except:
        pass

import subprocess

def get_network_info():
    # Get network information
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Hostname:", hostname)
    print("IP Address:", IPAddr)

    # Measure latency with ping
    try:
        ping_output = subprocess.check_output(["ping", "-c", "10", "-i", "0.2", "google.com"], universal_newlines=True)
        ping_lines = ping_output.strip().split("\n")
        rtt_lines = [line for line in ping_lines if "rtt min/avg/max/mdev" in line]
        if len(rtt_lines) > 0:
            rtt_parts = rtt_lines[0].split("=")[1].split("/")
            min_rtt, avg_rtt, max_rtt, mdev_rtt = rtt_parts
            print(f"Min RTT: {min_rtt} ms")
            print(f"Avg RTT: {avg_rtt} ms")
            print(f"Max RTT: {max_rtt} ms")
            print(f"Mdev RTT: {mdev_rtt} ms")
    except:
        pass

    # Measure bandwidth with curl
    try:
        curl_output = subprocess.check_output(["curl", "-s", "https://speed.cloudflare.com/__down"], universal_newlines=True)
        curl_lines = curl_output.strip().split("\n")
        speed_lines = [line for line in curl_lines if "Your download speed is" in line and "Your upload speed is" in line]
        if len(speed_lines) > 0:
            download_speed_parts = speed_lines[0].split("Your download speed is ")[1].split(" ")[0].split(".")
            download_speed = float(download_speed_parts[0]) if len(download_speed_parts) == 1 else float(download_speed_parts[0] + "." + download_speed_parts[1])
            upload_speed_parts = speed_lines[0].split("Your upload speed is ")[1].split(" ")[0].split(".")
            upload_speed = float(upload_speed_parts[0]) if len(upload_speed_parts) == 1 else float(upload_speed_parts[0] + "." + upload_speed_parts[1])
            print(f"Download speed: {download_speed:.2f} Mbps")
            print(f"Upload speed: {upload_speed:.2f} Mbps")
    except:
        pass

def get_cpu_info():
    # Get CPU information
    print("CPU Cores:", psutil.cpu_count())
    print("CPU Frequency:", psutil.cpu_freq().current, "MHz")
    print("CPU Usage:", psutil.cpu_percent(interval=1), "%")

def get_memory_info():
    # Get memory information
    svmem = psutil.virtual_memory()
    print("Total Memory:", svmem.total // (1024*1024), "MB")
    print("Available Memory:", svmem.available // (1024*1024), "MB")
    print("Memory Usage:", svmem.percent, "%")

def get_disk_info():
    # Get disk information
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"Partition Device: {partition.device}")
        print(f"Partition Mount Point: {partition.mountpoint}")
        print(f"File System Type: {partition.fstype}")
        partition_usage = psutil.disk_usage(partition.mountpoint)
        print(f"Partition Total Size: {partition_usage.total // (2**30)} GB")
        print(f"Partition Used: {partition_usage.used // (2**30)} GB")
        print(f"Partition Free: {partition_usage.free // (2**30)} GB")
        print(f"Partition Usage: {partition_usage.percent} %")

def eva():
    print("Welcome to Eva (Efficiency Virtual Assistant)")
    while True:
        command = input("Enter a command (system, network, cpu, memory, disk, or exit): ")
        if command == "system":
            get_system_info()
        elif command == "network":
            get_network_info()
        elif command == "cpu":
            get_cpu_info()
        elif command == "memory":
            get_memory_info()
        elif command == "disk":
            get_disk_info()
        elif command == "exit":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    eva()

