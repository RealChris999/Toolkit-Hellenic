#!/usr/bin/env python3

import requests
from rich.console import Console
from datetime import datetime
import os

console = Console()

console.print("[bold red]\n[ HELLENIC DARKNET DIR BRUTE ][/bold red]")
console.print("[green]Made by: 0xBL4CKH4T[/green]\n")

if not os.path.exists("logs"):
    os.makedirs("logs")

def brute_dirs(url, wordlist_path):
    try:
        with open(wordlist_path, "r") as f:
            words = f.read().splitlines()
    except:
        console.print("[red]Wordlist not found![/red]")
        return

    for word in words:
        full_url = url.rstrip("/") + "/" + word
        try:
            r = requests.get(full_url, timeout=5)
            status = r.status_code
            length = len(r.text)

            if status in [200, 301, 403]:
                console.print(f"[bold green][+] {full_url} - {status} ({length} bytes)[/bold green]")
                with open("logs/dir_found.txt", "a") as log:
                    log.write(f"[{datetime.now()}] {full_url} - {status} ({length} bytes)\n")
            else:
                console.print(f"[blue][-] {full_url} - {status}[/blue]")

        except Exception as e:
            console.print(f"[yellow][!] Error: {e}[/yellow]")

def main():
    target = input("Enter target URL (e.g. http://site.com): ").strip()
    wordlist = "payloads/dir.txt"
    brute_dirs(target, wordlist)

if __name__ == "__main__":
    main()
