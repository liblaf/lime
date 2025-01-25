import typer_di

from liblaf import lime

from . import description, features

app = typer_di.TyperDI(name="readme", no_args_is_help=True)
lime.add_command(app, description.app)
lime.add_command(app, features.app)
