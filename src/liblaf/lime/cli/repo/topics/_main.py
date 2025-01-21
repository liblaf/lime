from liblaf import lime


async def main() -> None:
    instruction: str = lime.prompt("topics")
    prompt: str = await lime.plugin.repomix(instruction)
    await lime.live(prompt)
