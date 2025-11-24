from rich.console import Console
import srl.storage as storage

def add_subparser(subparsers):
    parser = subparsers.add_parser("config", help="Update configuration values")
    parser.add_argument(
        "--audit-probability", type=float, help="Set audit probability (0-1)"
    )
    parser.add_argument(
        "--get", action="store_true", help="Display current configuration"
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args, console: Console):
    if args.get:
        config = storage.load_json(storage.CONFIG_FILE)
        console.print_json(data=config)
    else:
        probability: float | None = args.audit_probability

        if probability is None or probability < 0:
            console.print("[yellow]Invalid configuration option provided.[/yellow]")
            return

        config = storage.load_json(storage.CONFIG_FILE)
        config["audit_probability"] = probability
        storage.save_json(storage.CONFIG_FILE, config)
        console.print(f"Audit probability set to [cyan]{probability}[/cyan]")
