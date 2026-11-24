import sys
from pathlib import Path
from CLI.commands import format_save
from app import build_app


def parse_options(argv):
    data_dir = None
    rest = []
    for arg in argv:
        if arg.startswith("--data-dir="):
            data_dir = Path(arg.split("=", 1)[1]).expanduser()
        else:
            rest.append(arg)
    return data_dir, rest


def main():
    data_dir, argv = parse_options(sys.argv[1:])
    ctx = build_app(data_dir)
    for message in ctx.messages:
        print(message)

    if argv:
        ctx.cli.exec_command(" ".join(argv))
        return

    ctx.cli.exec_command("help")
    latest = ctx.saves.latest()
    if latest:
        print(f"\nЗнайдено збереження {format_save(latest)}. Щоб продовжити, введіть: continue")
    while True:
        try:
            cmd = input("\n> ").strip()
            if cmd in ("exit", "quit"):
                ctx.game_strategy.autosave()
                break
            if cmd:
                ctx.cli.exec_command(cmd)
        except (KeyboardInterrupt, EOFError):
            ctx.game_strategy.autosave()
            break


if __name__ == "__main__":
    main()
