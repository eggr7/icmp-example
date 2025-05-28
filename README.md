# ICMP Ping Tool in Python

This Python project demonstrates how to perform a "ping" operation (send an ICMP Echo Request packet) to a specific host using the operating system's `ping` command. It's a straightforward way to check network connectivity with a remote host. The project includes both a command-line script and a graphical user interface built with PyQt5.

## 📋 Description

The project consists of two main implementations:

1. **Command-line script** (`main.py` - original version): Defines a function `hacer_ping(host_destino)` that takes an IP address or a domain name as input, executes the appropriate `ping` command, and reports whether a reply was received.

2. **PyQt5 GUI application** (`main.py` - current version): Provides a graphical interface for the same functionality, allowing users to input hosts, select from predefined options, and view ping results in a user-friendly format.

The main goal is to illustrate a practical application of the ICMP protocol without the complexity of crafting raw ICMP packets from scratch, which would require elevated permissions and more extensive code.

## 🚀 Features

### Common Features (Both Versions)
* **Cross-platform:** Automatically adjusts `ping` command parameters for Windows, Linux, and macOS.
* **Single Packet:** Sends only one ICMP Echo Request packet for a quick test.
* **Configured Timeout:** Sets a timeout for the ping response to avoid indefinite blocking.
* **Basic Error Handling:** Catches common exceptions like `TimeoutExpired` (if the host doesn't respond in time) or `FileNotFoundError` (if the `ping` command isn't available).
* **Clear Output:** Provides informative messages about the ping status for each tested host.

### PyQt5 GUI Version Additional Features
* **User-friendly Interface:** Easy-to-use graphical interface for entering hosts and viewing results.
* **Predefined Host Options:** Quick selection of common hosts (Google DNS, local network, Google domain).
* **Non-blocking Operation:** Executes ping commands in a separate thread to keep the UI responsive.
* **Color-coded Results:** Green for successful pings, red for failures.
* **Detailed Output:** Displays the complete output from the ping command.

## 🛠️ Prerequisites

* Python 3.x installed.
* The `ping` command must be installed and accessible in the system's PATH (standard in most modern operating systems).
* For the GUI version: PyQt5 library (`pip install PyQt5`).

## ⚙️ Usage

### Command-line Version (Original)
1. Save the original code to a file, for example, `simple_ping.py`.
2. Run the script from your terminal:
   ```bash
   python simple_ping.py
   ```
3. The script will attempt to ping three hosts defined in the code:
    * `8.8.8.8` (Google's public DNS, usually responds)
    * An example IP on a private local network that will likely not respond (`192.168.10.250` - you can change this).
    * `www.google.com` (a common domain name).

You can modify the `host_existente`, `host_inexistente`, and `host_dominio` variables in the `--- Ejemplos de Uso ---` (--- Usage Examples ---) section of the script to test with different destinations.

## 📄 Expected Output Example

--- Haciendo ping a 8.8.8.8 ---
Respuesta recibida de 8.8.8.8

--- Haciendo ping a 192.168.10.250 ---
No se recibió respuesta de 192.168.10.250 o hubo un error.

--- Haciendo ping a www.google.com ---
Respuesta recibida de www.google.com

*(The exact output, especially for `www.google.com`, may vary slightly depending on network configuration and DNS resolution).*

## 💡 How It Works

The script uses the `platform` module to detect the operating system and thus use the correct parameters for the `ping` command (`-n 1` for Windows, `-c 1` for Linux/macOS, to send a single packet).

The `subprocess` module is responsible for executing the system's `ping` command. The `subprocess.run()` function:
* Executes the command.
* Captures standard output (`stdout`) and standard error (`stderr`).
* Checks the `returncode` of the process. A return code of `0` usually indicates that the `ping` command was successful and a response was received.

This approach abstracts the complexity of raw socket creation and manual ICMP packet construction, providing a simple way to achieve ping functionality.

## 🧑‍💻 Contributions

This is a simple script for didactic purposes. If you have suggestions to improve it or make it more robust (while maintaining simplicity), feel free to propose changes!