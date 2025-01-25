from liblaf import lime


async def main() -> None:
    instruction: lime.Prompt = lime.get_prompt("readme/features")
    prompt: str = await lime.plugin.repomix(instruction.prompt)
    message: str = await lime.live(
        [{"role": "user", "content": prompt}], markdown=True, transient=True
    )
    print(message)
