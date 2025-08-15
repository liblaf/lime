import attrs
from rich._loop import loop_last
from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.segment import Segment
from rich.text import Text


@attrs.define
class Tail:
    """.

    References:
        1. [`rich.live_render.LiveRender`](https://github.com/Textualize/rich/blob/master/rich/live_render.py)
    """

    renderable: RenderableType
    margin: int = 0

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        lines: list[list[Segment]] = console.render_lines(
            self.renderable, options, pad=False
        )
        height: int
        _, height = Segment.get_shape(lines)
        if height + self.margin > options.size.height:
            lines = lines[-(options.size.height - self.margin - 1) :]
            overflow_text = Text(
                "...", style="live.ellipsis", justify="center", overflow="crop", end=""
            )
            lines.insert(0, list(console.render(overflow_text)))
        newline: Segment = Segment.line()
        for last, line in loop_last(lines):
            yield from line
            if not last:
                yield newline
