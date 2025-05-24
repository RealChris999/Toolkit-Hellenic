import requests
from rich.console import Console
from datetime import datetime
import os

console = Console()

console.print("[bold red]\n[ HELLENIC DARKNET CMS SCANNER ][/bold red]")
console.print("[green]Made by: 0xBL4CKH4T[/green]\n")

if not os.path.exists("logs"):
    os.makedirs("logs")

def check_wordpress(url):
    try:
        r = requests.get(url + "/wp-login.php", timeout=7)
        if r.status_code == 200 and "wordpress" in r.text.lower():
            return True
    except:
        return False
    return False

def check_joomla(url):
    try:
        r = requests.get(url + "/administrator/", timeout=7)
        if r.status_code == 200 and ("joomla" in r.text.lower() or "joomla" in r.headers.get("X-Generator", "").lower()):
            return True
    except:
        return False
    return False

def check_drupal(url):
    try:
        r = requests.get(url + "/user/login", timeout=7)
        if r.status_code == 200 and "drupal" in r.text.lower():
            return True
    except:
        return False
    return False

def check_prestashop(url):
    try:
        r = requests.get(url + "/admin-dev", timeout=7)
        if r.status_code == 200 and "prestashop" in r.text.lower():
            return True
    except:
        return False
    return False

def main():
    url = input("Enter target URL (http://site.com): ").strip().rstrip("/")
    results = []

    if check_wordpress(url):
        results.append("WordPress detected")
    if check_joomla(url):
        results.append("Joomla detected")
    if check_drupal(url):
        results.append("Drupal detected")
    if check_prestashop(url):
        results.append("PrestaShop detected")

    console.print("\n[bold yellow]Scan Results:[/bold yellow]")
    if results:
        for res in results:
            console.print(f"[bold green]+ {res}[/bold green]")
    else:
        console.print("[red]No known CMS detected.[/red]")

    with open("logs/cms_scan.txt", "a") as f:
        f.write(f"[{datetime.now()}] {url} - {', '.join(results) if results else 'No CMS detected'}\n")

if __name__ == "__main__":
    main()
