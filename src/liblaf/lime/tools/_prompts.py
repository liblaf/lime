import jinja2


def prompt_templates() -> jinja2.Environment:
    return jinja2.Environment(
        line_statement_prefix="%%",
        line_comment_prefix="%%%",
        undefined=jinja2.StrictUndefined,
        autoescape=jinja2.select_autoescape(),
        loader=jinja2.PackageLoader("liblaf.lime", "prompts"),
    )
