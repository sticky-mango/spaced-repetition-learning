from srl.cli import build_parser
from srl.storage import set_data_dir
from srl.storage import ensure_data_dir
from srl.banner import banner
from rich.console import Console


def main():
    console = Console()
    set_data_dir(console)
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args, console)
    else:
        banner(console)
        parser.print_help()
