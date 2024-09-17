import sys
import argparse
import subprocess
from enum import Enum
from pathlib import Path


# Expected to be at the script root
PINS_FILE: str = "pins"


class Command(Enum):
    # Command {{{
    Run = "run"
    Add = "add"
    List = "list"
    Clear = "clear"
    Delete = "delete"
    # }}}


def main() -> None:
    # main {{{
    args = _configure_args()
    command = (Command)(args.command.lower())

    match command:
        case Command.Add:
            _handle_add(args)
        case Command.List:
            _handle_list(args)
        case Command.Delete:
            _handle_delete(args)
        case Command.Run:
            _handle_run(args)
        case Command.Clear:
            try:
                _write_pins({})
            except Exception as e:
                print(f"Failed to write pins file {e}")
                sys.exit(1)
    # }}}


def _configure_args() -> dict:
    # _configure_args {{{
    parser = argparse.ArgumentParser(
        description="Application to tag CLI commands for easy recall"
    )

    parser.add_argument(
        "command",
        help="The command to invoke: Add, Run, List, Delete, or Clear"
    )

    parser.add_argument(
        "-t", "--tag",
        help="The tag of the pin to interact with"
    )

    parser.add_argument(
        "-i", "--invoke",
        help="The CLI command to invoke"
    )

    args = parser.parse_args()
    return args
    # }}}


def _handle_add(args: dict) -> None:
    # _handle_add {{{
    assert args.tag is not None, "--tag required for add command"
    assert args.invoke is not None, "--invoke required for add command"

    tag = args.tag
    invocation = args.invoke

    try:
        pins = _read_pins()
        pins[tag] = invocation
    except Exception as e:
        print(f"Failed to read pins file {e}")
        sys.exit(1)

    try:
        _write_pins(pins)
    except Exception as e:
        print(f"Failed to write pins file {e}")
        sys.exit(1)
    # }}}


def _handle_delete(args: dict) -> None:
    # _handle_delete {{{
    assert args.tag is not None, "--tag required for add command"

    tag = args.tag

    try:
        pins = _read_pins()
    except Exception as e:
        print(f"Failed to read pins file {e}")
        sys.exit(1)

    pins.pop(tag)

    try:
        _write_pins(pins)
    except Exception as e:
        print(f"Failed to write pins file {e}")
        sys.exit(1)
    # }}}


def _handle_list(args: dict) -> None:
    # _handle_list {{{
    try:
        pins = _read_pins()
    except Exception as e:
        print(f"Failed to read pins file {e}")
        sys.exit(1)

    print("[tag] => [invocation]")
    print("=" * 40)
    for tag, invocation in pins.items():
        print(f"{tag} => {invocation}")
    # }}}


def _handle_run(args: dict) -> None:
    # _handle_run {{{
    assert args.tag is not None, "--tag required for add command"

    tag = args.tag

    try:
        pins = _read_pins()
    except Exception as e:
        print(f"Failed to read pins file {e}")
        sys.exit(1)

    shell = True if sys.platform == "win32" else False
    process = subprocess.run(
        pins[tag], capture_output=True, check=True, shell=shell
    )

    if process.stderr:
        for line in process.stderr.decode("utf-8").splitlines():
            print(line)

    for line in process.stdout.decode("utf-8").splitlines():
        print(line)
    # }}}


def _read_pins() -> dict:
    # _read_pins {{{
    pins = {}

    scriptdir = Path(__file__).parent
    pinsfile = Path(scriptdir, PINS_FILE)

    with open(pinsfile, "r") as file:
        content = file.readlines()
        for index in range(0, len(content), 2):
            if content[index].rstrip() != "":
                tag = content[index].rstrip()
                invocation = content[index + 1].rstrip()
                pins[tag] = invocation

    return pins
    # }}}


def _write_pins(pins: dict) -> None:
    # _write_pins {{{
    scriptdir = Path(__file__).parent
    pinsfile = Path(scriptdir, PINS_FILE)

    with open(pinsfile, "w") as file:
        for tag, invocation in pins.items():
            file.write(f"{tag}\n")
            file.write(f"{invocation}\n")
    # }}}


if __name__ == "__main__":
    main()
