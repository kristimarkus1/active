# TinyScanner - Simple Port Scanner

TinyScanner is a lightweight command-line port scanner that allows you to check whether a specific port (or range of ports) is open or closed on a target host. It supports both **TCP** and **UDP** scans.

## 📌 Requirements
- Python 3.x

## 🔧 Installation
1. **Clone the repository**
   ```bash
   git clone https://01.kood.tech/git/kmarkus/active
   cd active
   ```
2. **Ensure Python is installed**
   ```bash
   python3 --version
   ```

## 🚀 How to Run TinyScanner

### ✅ **Basic Usage**
Run a TCP scan on a specific port:
```bash
python3 main.py -t <host> -p <port>
```
Example:
```bash
python3 main.py -t 127.0.0.1 -p 80
```
Output:
```
Port 80 (http) is closed
```

### ✅ **Scanning a Range of Ports**
```bash
python3 main.py -t 192.168.1.1 -p 20-25
```
Output:
```
Port 21 (ftp) is open
Port 22 (ssh) is closed
Port 23 (telnet) is closed
```

### ✅ **UDP Scanning**
```bash
python3 main.py -u 192.168.1.1 -p 53
```
Output:
```
Port 53 (domain) is open
```

### ✅ **Verbose Mode (Debugging)**
If you want more details, use the `-v` flag:
```bash
python3 main.py -t 192.168.1.1 -p 80 -v
```
This will print real-time scanning progress.

### ✅ **Test if the Ports Are Open Manually**
To confirm the scanner results, you can manually check ports:

🔹 **Check TCP Port:**
```bash
nc -zv 127.0.0.1 80
```

🔹 **Check UDP Port:**
```bash
nc -zvu 192.168.1.1 53
```

🔹 **Check Running Services on Your Machine:**
```bash
sudo lsof -i -P -n | grep LISTEN
```

