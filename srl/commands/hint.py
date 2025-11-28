from rich.console import Console
import srl.storage as storage


def add_subparser(subparsers):
    parser = subparsers.add_parser("hint", help="Display the hint for a problem")
    parser.add_argument("name", type=str, help="Name of the problem")
    parser.set_defaults(handler=handle)
    return parser


def handle(args, console: Console):
    name: str = args.name

    # Check in-progress first
    data = storage.load_json(storage.PROGRESS_FILE)
    if name in data and "message" in data[name]:
        console.print(f"[cyan]{name}[/cyan]: {data[name]['message']}")
        return

    # Check mastered
    mastered = storage.load_json(storage.MASTERED_FILE)
    if name in mastered and "message" in mastered[name]:
        console.print(f"[cyan]{name}[/cyan]: {mastered[name]['message']}")
        return

    console.print(
        f"[yellow]No hint found for[/yellow] '[cyan]{name}[/cyan]'"
    )
