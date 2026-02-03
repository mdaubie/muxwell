import typer

from muxwell import __version__

from .apply import apply
from .info import info

app = typer.Typer(
    name="muxwell",
    help="A command-line tool for managing MKV files and subtitles with batch operations support.",
    no_args_is_help=True,
)


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", callback=version_callback, help="Show version and exit."
    ),
):
    """Muxwell: A command-line tool for managing MKV files and subtitles with batch operations support."""
    pass


app.command(help="Show info about video file(s).")(info)
app.command(help="Apply changes to video file(s).", no_args_is_help=True)(apply)
