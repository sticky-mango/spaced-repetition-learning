from rich.console import Console
import srl.storage as storage

def add_subparser(subparsers):
    parser = subparsers.add_parser("remove", help="Remove a problem from in-progress")
    parser.add_argument("name", type=str, help="Name of the problem to remove")
    parser.set_defaults(handler=handle)
    return parser


def handle(args, console: Console):
    name: str = args.name

    data = storage.load_json(storage.PROGRESS_FILE)
    if name in data:
        del data[name]
        storage.save_json(storage.PROGRESS_FILE, data)
        console.print(
            f"[green]Removed[/green] '[cyan]{name}[/cyan]' [green]from in-progress.[/green]"
        )
    else:
        console.print(
            f"[red]Problem[/red] '[cyan]{name}[/cyan]' [red]not found in in-progress.[/red]"
        )
