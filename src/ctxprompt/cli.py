import typer

app = typer.Typer()


@app.command()
def main(
    path: str = typer.Argument(".", help="Path to project root"),
):
    print(f"ctxprompt running on: {path}")


if __name__ == "__main__":
    app()