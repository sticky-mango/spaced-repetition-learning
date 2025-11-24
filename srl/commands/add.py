from rich.console import Console
from srl.utils import today
import srl.storage as storage


def add_subparser(subparsers):
    add = subparsers.add_parser("add", help="Add or update a problem attempt")
    add.add_argument("name", type=str, help="Name of the LeetCode problem")
    add.add_argument("rating", type=int, choices=range(1, 6), help="Rating from 1-5")
    add.set_defaults(handler=handle)
    return add


def handle(args, console: Console):
    name: str = args.name
    rating: int = args.rating

    data = storage.load_json(storage.PROGRESS_FILE)

    entry = data.get(name, {"history": []})
    entry["history"].append(
        {
            "rating": rating,
            "date": today().isoformat(),
        }
    )

    # Mastery check: last two ratings are 5
    history = entry["history"]
    if len(history) >= 2 and history[-1]["rating"] == 5 and history[-2]["rating"] == 5:
        mastered = storage.load_json(storage.MASTERED_FILE)
        if name in mastered:
            mastered[name]["history"].extend(history)
        else:
            mastered[name] = entry
        storage.save_json(storage.MASTERED_FILE, mastered)
        if name in data:
            del data[name]
        console.print(
            f"[bold green]{name}[/bold green] moved to [cyan]mastered[/cyan]!"
        )
    else:
        data[name] = entry
        console.print(
            f"Added rating [yellow]{rating}[/yellow] for '[cyan]{name}[/cyan]'"
        )

    storage.save_json(storage.PROGRESS_FILE, data)

    # Remove from next up if it exists there
    next_up = storage.load_json(storage.NEXT_UP_FILE)
    if name in next_up:
        del next_up[name]
        storage.save_json(storage.NEXT_UP_FILE, next_up)
