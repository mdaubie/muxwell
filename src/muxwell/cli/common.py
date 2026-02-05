import typer

QuietOption = typer.Option(False, "-q", "--quiet", help="Silence non-error output.")
RecursiveOption = typer.Option(
    False, "--recursive", "-r", help="Recursively process directories."
)
