import attrs


@attrs.define
class RepomixArgs:
    # Repomix Output Options
    compress: bool = False
    files: bool = True
    truncate_base64: bool = True
    # File Selection Options
    default_ignore: bool = True
    ignore: list[str] = attrs.field(
        converter=attrs.converters.default_if_none(factory=list), factory=list
    )
    ignore_generated: bool = True
