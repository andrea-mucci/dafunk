"""Console script for dafunk_core_library."""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def build():
    """Console script for dafunk_core_library."""
    console.print("this is a build command")


@app.command()
def new():
    """Console script for dafunk_core_library."""
    console.print("this is a new command")
