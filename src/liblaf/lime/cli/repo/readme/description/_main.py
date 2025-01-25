from liblaf import lime


async def main() -> None:
    instruction: lime.Prompt = lime.get_prompt("readme/description")
    prompt: str = await lime.plugin.repomix(instruction.prompt)
    await lime.live([{"role": "user", "content": prompt}])
