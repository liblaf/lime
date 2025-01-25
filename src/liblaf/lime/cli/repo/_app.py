import typer_di

from liblaf import lime

from . import topics

app = typer_di.TyperDI(name="repo", no_args_is_help=True)
lime.add_command(app, topics.app)
