import typer_di

from liblaf import lime

from . import commit, repo

app = typer_di.TyperDI(name="lime", no_args_is_help=True)
lime.add_command(app, repo.app)
lime.add_command(app, commit.app)
