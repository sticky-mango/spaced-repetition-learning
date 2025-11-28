from rich.console import Console
from srl.utils import today
from srl.storage import load_json, save_json
import srl.storage as storage


def add_subparser(subparsers):
    add = subparsers.add_parser("add", help="Add or update a problem attempt")
    add.add_argument("name", type=str, help="Name of the LeetCode problem")
    add.add_argument(
        "rating",
        type=int,
        choices=range(1, 6),
        help="Rating from 1-5: "
        "1=Couldn't solve/needed solution,"
        "2=Solved with significant struggle,"
        "3=Solved with minor struggle,"
        "4=Solved smoothly with few gaps,"
        "5=Solved perfectly, confidently",
    )
    add.add_argument("-m", type=str, help="Optional message/note about the attempt")
    add.set_defaults(handler=handle)
    return add


def handle(args, console: Console):
    name: str = args.name
    rating: int = args.rating
    message: str = args.m

    data = load_json(storage.PROGRESS_FILE)

    entry = data.get(name, {"history": []})
    entry["history"].append(
        {
            "rating": rating,
            "date": today().isoformat(),
        }
    )
    if message:
        entry["message"] = message

    # Mastery check: last two ratings are 5
    history = entry["history"]
    if len(history) >= 2 and history[-1]["rating"] == 5 and history[-2]["rating"] == 5:
        mastered = load_json(storage.MASTERED_FILE)
        if name in mastered:
            mastered[name]["history"].extend(history)
        else:
            mastered[name] = entry
        save_json(storage.MASTERED_FILE, mastered)
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

    save_json(storage.PROGRESS_FILE, data)

    # Remove from next up if it exists there
    next_up = load_json(storage.NEXT_UP_FILE)
    if name in next_up:
        del next_up[name]
        save_json(storage.NEXT_UP_FILE, next_up)
