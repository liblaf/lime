import typer


def add_command(app: typer.Typer, cmd: typer.Typer) -> None:
    if len(cmd.registered_commands) == 1:
        registered_command: typer.models.CommandInfo = cmd.registered_commands[0]
        assert registered_command.callback is not None
        app.command(cmd.info.name)(registered_command.callback)
    else:
        app.add_typer(cmd)
