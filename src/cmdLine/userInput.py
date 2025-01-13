import argparse

from rich.console import Console

from rich.progress import Progress

import pyfiglet



parser =  argparse.ArgumentParser(description="Web Crawler")

parser.add_argument("--target",help="Target domain",action = "store")

parser.add_argument("--scan", help="Scan for links on domain", action="store_true") #flag

parser.add_argument("--depth", help="depth of domain to scan", action="store")  # Flag



args = parser.parse_args()
console = Console()

banner1 = pyfiglet.figlet_format("Venom Security",font="slant")
console.print(f"[green]]{banner1}[/green]")



if args.scan:
    console.print(f"[bold green]Scanning started for {args.target}...[/bold green]")
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=100)
        for i in range(100):
            progress.update(task, advance=1)






