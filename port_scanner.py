import socket
import time
import sys
import threading
TIMEOUT = 0.1
USAGE = (
    "Usage  : py ex.py <target> <start_port> <end_port>\n"
    "Example: py ex.py google.com 20 100"
)
results=[]
threads=[]

ports_scanned=0


def validate_port(port):
    return port > 0 and port < 65536


if len(sys.argv)==4:
    ip=sys.argv[1]

    try:
        start =(int(sys.argv[2]))
        end =(int(sys.argv[3]))

    except ValueError:
        print("Invalid Port Number,needs to be an integer")
        sys.exit()
    print("Processing")
    start_valid = validate_port(start)
    end_valid = validate_port(end)    
    if start > end:
        print("Error: The starting port must be smaller than the ending port.")
        sys.exit()
    if not start_valid:
        print("Invalid Start Port, ports should be between 1 and 65535")
        sys.exit()
    if not end_valid:
        print("Invalid End Port, ports should be between 1 and 65535")
        sys.exit()
elif len(sys.argv)>4:
    print("too many arguments")
    print(USAGE)
    sys.exit()
elif len(sys.argv)<4:
    print("not enough arguments")
    print(USAGE)
    sys.exit()



try:
    resolved_ip = socket.gethostbyname(ip)
except socket.gaierror:
    print("Unable to resolve hostname.")
    sys.exit()




def scan_port(ip,port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    scanner.settimeout(TIMEOUT)
    try:
        scanner.connect((ip, port))
        print(f"Connected to {port}")
        try:
            service=socket.getservbyport(port)
        except Exception:
            service = "Unknown"
        results.append((port, service))
    except Exception :
        pass
    finally:
        scanner.close()
print("-" * 50)
print(f"Scanning Target: {ip} ({resolved_ip})")
print(f"Port Range: {start} to {end}")
print("-" * 50)
start_time=time.time()
print(start, end)

for i in range(start, end + 1):
    print("Scanning", i)
    ports_scanned += 1
    worker = threading.Thread(target=scan_port, args=(resolved_ip, i))
    worker.start()
    threads.append(worker)
    
for thread in threads:
    thread.join()
results.sort()
for result in results:
    print(result[0], "is open:", result[1]) 
print("Total Ports Scanned:", ports_scanned)
print("Total Open Ports:", len(results))
end_time = time.time()
print("Time taken:", round(end_time - start_time, 2), "seconds")
print("\n Scan complete!")
print("-" * 50)
sys.exit()