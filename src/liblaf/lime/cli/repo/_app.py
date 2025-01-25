import typer_di

from liblaf import lime

from . import description, topics

app = typer_di.TyperDI(name="repo", no_args_is_help=True)
lime.add_command(app, topics.app)
lime.add_command(app, description.app)
