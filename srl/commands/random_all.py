from rich.console import Console
import random
import srl.storage as storage

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "random_all", help="Pick a random problem from all problems (progress, mastered, next up)"
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args, console: Console):
    progress = storage.load_json(storage.PROGRESS_FILE)
    mastered = storage.load_json(storage.MASTERED_FILE)
    next_up = storage.load_json(storage.NEXT_UP_FILE)

    names = set()
    if isinstance(progress, dict):
        names.update(progress.keys())
    if isinstance(mastered, dict):
        names.update(mastered.keys())
    if isinstance(next_up, dict):
        names.update(next_up.keys())

    names = list(names)
    if not names:
        console.print("[bold green]No problems available to pick from.[/bold green]")
        return

    choice = random.choice(names)
    console.print(f"[bold blue]Random problem (all):[/bold blue] [cyan]{choice}[/cyan]")
