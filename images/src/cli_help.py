from typer.main import get_command
from typer.rich_utils import _get_rich_console, rich_format_help

from xplane_apt_convert.cli import app

command = get_command(app)

prog_name = "python -m xplane_apt_convert"

with command.make_context(prog_name, ["--help"], resilient_parsing=True) as ctx:
    console = _get_rich_console()
    console.width = 120
    console.record = True
    console.highlighter = None

    # console.print(" ❱ ", style="bold cyan", end="")
    console.print(" ⟫ ", style="bold cyan", end="")
    console.print(f"{prog_name} --help", style="white")

    # NOTE: requires modifying the definition of rich_format_help to support passing a Console instance
    rich_format_help(
        obj=command, ctx=ctx, markup_mode=app.rich_markup_mode, console=console
    )
    console.save_svg("cli_help.svg", title="xplane_apt_convert")
