import litellm
import pytest

from liblaf.lime.llm import LLM, LLMArgs

MOCK_RESPONSE: str = "Hi! My name is Claude."


@pytest.mark.asyncio
async def test_llm() -> None:
    llm: LLM = LLM.from_args(LLMArgs())
    stream: litellm.CustomStreamWrapper = await llm.acompletion(
        [{"role": "user", "content": "Hello, world!"}],
        model="gemini-2.5-flash",
        mock_response=MOCK_RESPONSE,
    )
    chunks: list[litellm.ModelResponseStream | None] = [chunk async for chunk in stream]
    response: litellm.ModelResponse = litellm.stream_chunk_builder(chunks)  # pyright: ignore[reportAssignmentType]
    message: litellm.Message = response.choices[0].message  # pyright: ignore[reportAttributeAccessIssue]
    assert message.content == MOCK_RESPONSE
