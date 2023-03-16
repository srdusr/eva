import psutil
import platform
import socket
import subprocess
import sys
import speedtest

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

def get_network_info():
    # Get network information
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Hostname:", hostname)
    print("IP Address:", IPAddr)
    
    # Get network speed
    st = speedtest.Speedtest()
    latency = st.results.ping
    download = st.download() / (1024*1024)
    upload = st.upload() / (1024*1024)
    print("Latency:", latency, "ms")
    print("Download:", download, "Mbps")
    print("Upload:", upload, "Mbps")
    
    # Get network jitter
    server = st.get_best_server()
    jitter = st.results.ping - server["latency"] if server else None

    print("Jitter:", jitter, "ms")
    
    # Get network stats
    st.get_servers()
    st.get_best_server()
    stats = st.results.dict()
    print("Network Stats:")
    print("  - Average:", stats["ping"], "ms")
    print("  - Minimum:", stats["ping"]["min"], "ms")
    print("  - Maximum:", stats["ping"]["max"], "ms")

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

