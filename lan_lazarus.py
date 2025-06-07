#!/usr/bin/env python3

import os
import sys
import time
import logging
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
import platform
import subprocess
import psutil
from datetime import datetime
import socket
import re

# Configure logging
logging.basicConfig(
    filename=f'lan_lazarus_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LANLazarus:
    def __init__(self):
        self.console = Console()
        self.is_windows = platform.system().lower() == "windows"
        self.seance_mode = False

    def log_action(self, message, level=logging.INFO):
        """Log actions if séance mode is enabled"""
        if self.seance_mode:
            logging.log(level, message)

    def show_banner(self):
        banner = """
 _      _    _   _    _        _    ____    _    ____  _   _ ____  
| |    / \  | \ | |  | |      / \  |__  |  / \  |  _ \| | | / ___| 
| |   / _ \ |  \| |  | |     / _ \   / /  / _ \ | |_) | | | \___ \\ 
| |__/ ___ \| |\  |  | |___ / ___ \ / /_ / ___ \|  _ <| |_| |___) |
|____/_/   \_\_| \_|  |_____/_/   \_/____/_/   \_\_| \_\\\\___/|____/ 
        """
        self.console.print(Panel(banner, title="[bold green]LAN Lazarus[/]", 
                               subtitle="[bold red]Dead Network Revival Toolkit[/]"))

    def check_privileges(self):
        """Check if script is running with admin privileges"""
        try:
            if self.is_windows:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False

    def get_network_interfaces(self):
        """Get list of network interfaces using platform-native commands"""
        interfaces = []
        try:
            if self.is_windows:
                output = subprocess.run(['netsh', 'interface', 'show', 'interface'], 
                                     capture_output=True, text=True).stdout
                for line in output.split('\n')[3:]:  # Skip header lines
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            interface = parts[-1]
                            if not interface.lower().startswith(('loopback', 'vethernet')):
                                interfaces.append(interface)
            else:
                output = subprocess.run(['ip', 'link', 'show'], 
                                     capture_output=True, text=True).stdout
                for line in output.split('\n'):
                    if ':' in line and not line.startswith(' '):
                        iface = line.split(':')[1].strip()
                        if not iface.startswith(('lo', 'veth')):
                            interfaces.append(iface)
        except Exception as e:
            self.log_action(f"Error getting network interfaces: {str(e)}", logging.ERROR)
        
        return interfaces

    def resurrect_dhcp(self):
        """Restart DHCP services and verify IP assignment"""
        if not self.check_privileges():
            self.console.print("[bold red]⚠️ This feature requires administrative privileges![/]")
            return

        self.console.print("[bold yellow]🔄 Attempting DHCP resurrection...[/]")
        self.log_action("Starting DHCP resurrection")
        
        try:
            if self.is_windows:
                subprocess.run(['net', 'stop', 'dhcp'], capture_output=True)
                time.sleep(2)
                subprocess.run(['net', 'start', 'dhcp'], capture_output=True)
                # Release and renew IP for all adapters
                subprocess.run(['ipconfig', '/release'], capture_output=True)
                time.sleep(2)
                subprocess.run(['ipconfig', '/renew'], capture_output=True)
            else:
                subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'], capture_output=True)
                # Release and renew IP for all adapters
                for iface in self.get_network_interfaces():
                    subprocess.run(['sudo', 'dhclient', '-r', iface], capture_output=True)
                    time.sleep(1)
                    subprocess.run(['sudo', 'dhclient', iface], capture_output=True)
            
            time.sleep(5)  # Wait for service to restart
            
            # Verify IP assignment
            if self.is_windows:
                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
            else:
                result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            
            if ("DHCP" in result.stdout) or ("dynamic" in result.stdout.lower()):
                self.console.print("[bold green]✔ DHCP service successfully resurrected![/]")
                self.log_action("DHCP resurrection successful")
            else:
                self.console.print("[bold red]❌ DHCP resurrection failed[/]")
                self.log_action("DHCP resurrection failed", logging.ERROR)
        
        except Exception as e:
            self.console.print(f"[bold red]Error during DHCP resurrection: {str(e)}[/]")
            self.log_action(f"DHCP resurrection error: {str(e)}", logging.ERROR)

    def ghost_bust_arp(self):
        """Detect and resolve IP conflicts"""
        if not self.check_privileges():
            self.console.print("[bold red]⚠️ This feature requires administrative privileges![/]")
            return

        self.console.print("[bold yellow]👻 Running ARP Ghostbuster...[/]")
        self.log_action("Starting ARP conflict detection")
        
        try:
            if self.is_windows:
                arp_result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            else:
                arp_result = subprocess.run(['arp', '-n'], capture_output=True, text=True)
            
            # Parse ARP table and look for duplicates
            arp_table = {}
            for line in arp_result.stdout.split('\n'):
                if 'dynamic' in line.lower() or 'ether' in line.lower():
                    parts = line.split()
                    if len(parts) >= 3:
                        ip = parts[0]
                        mac = parts[1] if self.is_windows else parts[2]
                        if mac in arp_table:
                            self.console.print(f"[bold red]⚠ IP conflict detected![/]")
                            self.console.print(f"MAC {mac} is used by multiple IPs: {ip}, {arp_table[mac]}")
                            self.log_action(f"IP conflict: MAC {mac} used by {ip} and {arp_table[mac]}")
                        arp_table[mac] = ip
            
            if not arp_table:
                self.console.print("[bold green]✔ No IP conflicts detected[/]")
                self.log_action("No IP conflicts found")
        
        except Exception as e:
            self.console.print(f"[bold red]Error during ARP ghost busting: {str(e)}[/]")
            self.log_action(f"ARP ghost busting error: {str(e)}", logging.ERROR)

    def detect_cable_poltergeist(self):
        """Test network interfaces and cable connections"""
        if not self.check_privileges():
            self.console.print("[bold red]⚠️ This feature requires administrative privileges![/]")
            return

        self.console.print("[bold yellow]🔌 Running Cable Poltergeist Detection...[/]")
        self.log_action("Starting cable and interface diagnostics")
        
        try:
            interfaces = self.get_network_interfaces()
            
            if not interfaces:
                self.console.print("[bold red]No network interfaces found![/]")
                return
                
            self.console.print(f"[bold blue]Found {len(interfaces)} network interfaces[/]")
            
            for iface in interfaces:
                self.console.print(f"\n[bold blue]Testing interface {iface}[/]")
                
                # Check if interface is up
                if self.is_windows:
                    status = subprocess.run(['netsh', 'interface', 'show', 'interface', iface], 
                                         capture_output=True, text=True)
                    media_status = subprocess.run(['netsh', 'interface', 'show', 'interface', iface], 
                                               capture_output=True, text=True)
                else:
                    status = subprocess.run(['ip', 'link', 'show', iface], 
                                         capture_output=True, text=True)
                    media_status = subprocess.run(['ethtool', iface], 
                                               capture_output=True, text=True)
                
                # Check interface status
                if ("enabled" in status.stdout.lower()) or ("UP" in status.stdout):
                    self.console.print(f"[green]✔ Interface {iface} is UP[/]")
                    
                    # Test connectivity
                    try:
                        if self.is_windows:
                            test_ip = "127.0.0.1" if "Loopback" in iface else "8.8.8.8"
                            ping_result = subprocess.run(['ping', '-n', '1', '-w', '1000', test_ip], 
                                                      capture_output=True)
                        else:
                            test_ip = "127.0.0.1" if "lo" in iface else "8.8.8.8"
                            ping_result = subprocess.run(['ping', '-c', '1', '-W', '1', test_ip], 
                                                      capture_output=True)
                        
                        if ping_result.returncode == 0:
                            self.console.print(f"[green]✔ Interface {iface} has connectivity[/]")
                        else:
                            self.console.print(f"[red]❌ Interface {iface} has no connectivity[/]")
                    except Exception as e:
                        self.console.print(f"[red]❌ Could not test connectivity on {iface}: {str(e)}[/]")
                else:
                    self.console.print(f"[red]❌ Interface {iface} is DOWN[/]")
                
                self.log_action(f"Interface {iface} status checked")
        
        except Exception as e:
            self.console.print(f"[bold red]Error during cable detection: {str(e)}[/]")
            self.log_action(f"Cable detection error: {str(e)}", logging.ERROR)

    def sniff_packets(self, duration=30):
        """Capture and analyze local network traffic"""
        if not self.check_privileges():
            self.console.print("[bold red]⚠️ This feature requires administrative privileges![/]")
            return

        self.console.print(f"[bold yellow]📡 Starting Offline Packet Sniffer (Duration: {duration}s)...[/]")
        self.log_action("Starting packet capture")
        
        try:
            capture_file = "lan_lazarus_capture.etl" if self.is_windows else "lan_lazarus_capture.pcap"
            
            # Check if previous capture file exists and delete it
            if os.path.exists(capture_file):
                os.remove(capture_file)
                self.console.print(f"[yellow]Removed previous capture file: {capture_file}[/]")
            
            if self.is_windows:
                # Start capture using netsh trace
                start_cmd = f"netsh trace start capture=yes tracefile={capture_file}"
                result = subprocess.run(start_cmd.split(), capture_output=True, text=True)
                if "started" not in result.stdout.lower():
                    self.console.print("[bold red]Failed to start packet capture![/]")
                    return
            else:
                # Start capture using tcpdump
                capture_cmd = f"tcpdump -w {capture_file} -G {duration}"
                process = subprocess.Popen(capture_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Show progress
            with self.console.status("[bold green]Capturing packets...") as status:
                for i in range(duration):
                    time.sleep(1)
                    self.console.print(f"Captured for {i+1}/{duration} seconds")
            
            # Stop capture
            if self.is_windows:
                stop_result = subprocess.run("netsh trace stop".split(), capture_output=True, text=True)
                if "completed" not in stop_result.stdout.lower():
                    self.console.print("[bold red]Warning: Packet capture may not have stopped properly[/]")
            else:
                process.terminate()
            
            # Verify capture file
            if os.path.exists(capture_file):
                file_size = os.path.getsize(capture_file)
                self.console.print(f"[bold green]✔ Packet capture complete! Saved to {capture_file} (Size: {file_size/1024:.2f} KB)[/]")
                self.log_action(f"Packet capture completed and saved to {capture_file} (Size: {file_size} bytes)")
            else:
                self.console.print("[bold red]❌ Error: Capture file was not created![/]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error during packet sniffing: {str(e)}[/]")
            self.log_action(f"Packet sniffing error: {str(e)}", logging.ERROR)

    def main_menu(self):
        """Display and handle the main menu"""
        while True:
            self.console.clear()
            self.show_banner()
            
            menu = Table(show_header=False, box=None)
            menu.add_row("[1] 🔄 Auto-DHCP Resurrector")
            menu.add_row("[2] 👻 ARP Ghostbuster")
            menu.add_row("[3] 🔌 Cable Poltergeist Detector")
            menu.add_row("[4] 📡 Offline Packet Sniffer")
            menu.add_row("[5] 📝 Toggle Séance Mode (Logging)")
            menu.add_row("[6] 🚪 Exit")
            
            self.console.print(menu)
            
            choice = input("\nChoose your ritual (1-6): ")
            
            if choice == '1':
                self.resurrect_dhcp()
            elif choice == '2':
                self.ghost_bust_arp()
            elif choice == '3':
                self.detect_cable_poltergeist()
            elif choice == '4':
                self.sniff_packets()
            elif choice == '5':
                self.seance_mode = not self.seance_mode
                status = "enabled" if self.seance_mode else "disabled"
                self.console.print(f"[bold purple]Séance Mode {status}[/]")
            elif choice == '6':
                self.console.print("[bold green]Exiting LAN Lazarus... May your network rest in peace ⚰️[/]")
                break
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        lazarus = LANLazarus()
        lazarus.main_menu()
    except KeyboardInterrupt:
        print("\nExiting LAN Lazarus... May your network rest in peace ⚰️")
        sys.exit(0) 