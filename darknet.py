import os
from rich.console import Console

console = Console()

banner = r"""
 ▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀ ███▄    █ ▓█████▄▄▄█████▓
▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒  ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒
░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░ ▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░
░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄ ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ 
░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄▒██░   ▓██░░▒████▒ ▒██▒ ░ 
 ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░   
 ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░░ ░░   ░ ▒░ ░ ░  ░   ░    
 ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░    ░   ░ ░    ░    ░      
   ░          ░  ░   ░     ░  ░            ░    ░  ░        
 ░                                                          
                [ HELLENIC DARKNET ]
                Made by: 0xBL4CKH4T
"""

menu = """
[1] SQL Injection Scanner
[2] XSS Scanner
[3] Directory Brute Forcer
[4] CMS Vulnerability Scanner
[5] DDoS Test Tool
[0] Exit
"""

def main():
    os.system("clear")
    console.print(f"[bold red]{banner}[/bold red]")
    console.print(f"[bold blue]{menu}[/bold blue]")
    choice = input("Select Option: ")

    if choice == "1":
        os.system("python3 modules/sqli_scanner.py")
    elif choice == "2":
        os.system("python3 modules/xss_scanner.py")
    elif choice == "3":
        os.system("python3 modules/dir_brute.py")
    elif choice == "4":
        os.system("python3 modules/cms_scanner.py")
    elif choice == "5":
        os.system("python3 modules/ddos_advanced.py")
    elif choice == "6":
        os.system("python3 modules/bypass_fuzzer.py")
    elif choice == "0":
        exit()
    else:
        print("Invalid option.")
        main()

if __name__ == "__main__":
    main()
