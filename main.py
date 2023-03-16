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

    # Run speed test
    st = speedtest.Speedtest()
    st.get_best_server()

    # Print network stats
    download_speed = round(st.download() / 1e6, 2)
    upload_speed = round(st.upload() / 1e6, 2)
    results_dict = st.results.dict()
    ping = round(results_dict['ping'], 2)
    jitter = round(results_dict['jitter'], 2)
    latency_avg = round(results_dict['server']['latency'], 2)
    latency_min = round(results_dict['server']['latency_min'], 2)
    latency_max = round(results_dict['server']['latency_max'], 2)

    print("Download Speed:", download_speed, "Mbps")
    print("Upload Speed:", upload_speed, "Mbps")
    print("Ping:", ping, "ms")
    print("Jitter:", jitter, "ms")
    print("Latency (avg):", latency_avg, "ms")
    print("Latency (min):", latency_min, "ms")
    print("Latency (max):", latency_max, "ms")

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

