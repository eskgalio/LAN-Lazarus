# LAN Lazarus - Dead Network Revival Toolkit 🧟‍♂️

> LAN Lazarus is a powerful diagnostic and revival toolkit for local networks, designed to troubleshoot and fix network issues when Internet connectivity is unavailable. With its spooky-themed interface and robust feature set, it helps network administrators and IT professionals diagnose and resolve common network problems quickly and efficiently.

```ascii
 _      _    _   _    _        _    ____    _    ____  _   _ ____  
| |    / \  | \ | |  | |      / \  |__  |  / \  |  _ \| | | / ___| 
| |   / _ \ |  \| |  | |     / _ \   / /  / _ \ | |_) | | | \___ \ 
| |__/ ___ \| |\  |  | |___ / ___ \ / /_ / ___ \|  _ <| |_| |___) |
|____/_/   \_\_| \_|  |_____/_/   \_/____/_/   \_\_| \_\\___/|____/ 
```

## 🌟 Features

### 1. Auto-DHCP Resurrector 🔄
- Automatically diagnoses DHCP service issues
- Restarts DHCP services safely
- Releases and renews IP addresses
- Verifies successful IP assignment

### 2. ARP Ghostbuster 👻
- Detects IP address conflicts in real-time
- Identifies duplicate MAC addresses
- Maps network device relationships
- Suggests resolution steps for conflicts

### 3. Cable Poltergeist Detector 🔌
- Tests network interface status
- Verifies physical connections
- Performs connectivity tests
- Diagnoses cable and NIC issues

### 4. Offline Packet Sniffer 📡
- Captures local network traffic
- Saves packet data for analysis
- Works without Internet connectivity
- Supports both Windows and Linux packet capture formats

### 5. Séance Mode 📝
- Comprehensive logging system
- Detailed diagnostic trail
- Step-by-step operation records
- Export logs for documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Administrative privileges
- Windows 10/11 or Linux (Ubuntu/Debian/CentOS)

### Required System Tools
#### Windows
- ipconfig
- arp
- netsh
- ping

#### Linux
- ip
- arp
- ethtool
- tcpdump
- dhclient

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lan-lazarus.git
cd lan-lazarus
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. For Linux systems, make the script executable:
```bash
chmod +x lan_lazarus.py
```

## 💻 Usage

### Windows
Run PowerShell as Administrator and execute:
```powershell
python lan_lazarus.py
```

### Linux
Run with sudo:
```bash
sudo python3 lan_lazarus.py
```

## 🎯 Feature Usage Guide

### DHCP Resurrection
1. Select option [1] from the main menu
2. Wait for the service restart process
3. Check the results of IP renewal

### ARP Conflict Detection
1. Select option [2] from the main menu
2. Review any detected IP conflicts
3. Follow suggested resolution steps

### Cable Diagnostics
1. Select option [3] from the main menu
2. Wait for interface scanning
3. Review connection status for each interface

### Packet Capture
1. Select option [4] from the main menu
2. Wait for the 30-second capture
3. Find the capture file in the script directory

### Logging (Séance Mode)
1. Select option [5] to toggle logging
2. Perform your diagnostics
3. Check the log file in the script directory

## 🔧 Troubleshooting

### Common Issues

#### Permission Denied
- Ensure you're running with administrative privileges
- Check system tool availability
- Verify file permissions

#### Network Tool Errors
- Confirm required system tools are installed
- Check network adapter status
- Verify Windows/Linux compatibility

#### Packet Capture Issues
- Ensure no other capture tools are running
- Check disk space for capture files
- Verify network adapter permissions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool requires administrative privileges to function properly. Use with caution and understanding of network operations. The authors are not responsible for any network disruptions or issues that may arise from using this tool.

## 🙏 Acknowledgments

- Network diagnostic tool communities
- Python networking library contributors
- Open source network utility developers

## 📞 Support

For support, please:
1. Check the [Issues](https://github.com/yourusername/lan-lazarus/issues) page
2. Review existing documentation
3. Open a new issue if needed

---

Made with 💀 by Network Necromancers 