from rich.console import Console
from rich.panel import Panel
import srl.storage as storage


def add_subparser(subparsers):
    parser = subparsers.add_parser("hint", help="Display the hint for a problem")
    parser.add_argument("name", type=str, nargs='?', help="Name of the problem")
    parser.add_argument("-all", action="store_true", help="Show hints for all problems")
    parser.set_defaults(handler=handle)
    return parser


def handle(args, console: Console):
    # Load data from both files
    data = storage.load_json(storage.PROGRESS_FILE)
    mastered = storage.load_json(storage.MASTERED_FILE)
    
    if args.name and args.all:
        console.print("[red]Incorrect usage. Please provide just a problem name or use -all flag[/red]")
        return
    
    # If -all flag is used, show all hints
    if args.all:
        hints = []

        # Collect hints from in-progress problems
        for name, problem in data.items():
            if "message" in problem:
                hints.append(f"• [cyan]{name}[/cyan]: {problem['message']}")

        # Collect hints from mastered problems
        for name, problem in mastered.items():
            if "message" in problem:
                hints.append(f"• [cyan]{name}[/cyan]: {problem['message']}")

        if not hints:
            console.print("[yellow]No hints found in database[/yellow]")
        else:
            console.print(
                Panel.fit(
                    "\n".join(hints),
                    title=f"[bold cyan]Problem Hints ({len(hints)})[/bold cyan]",
                    border_style="cyan",
                    title_align="left",
                )
            )
        return

    # Original behavior: show hint for specific problem
    name: str = args.name

    if not name:
        console.print("[yellow]Please provide a problem name or use -all flag[/yellow]")
        return

    # Check in-progress first
    if name in data and "message" in data[name]:
        console.print(f"[cyan]{name}[/cyan]: {data[name]['message']}")
        return

    # Check mastered
    if name in mastered and "message" in mastered[name]:
        console.print(f"[cyan]{name}[/cyan]: {mastered[name]['message']}")
        return

    console.print(
        f"[yellow]No hint found for[/yellow] '[cyan]{name}[/cyan]'"
    )
