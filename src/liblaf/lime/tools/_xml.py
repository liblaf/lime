def extract_between_tags(content: str, tag: str, *, strip: bool = True) -> str:
    tag_open: str = f"<{tag}>"
    tag_close: str = f"</{tag}>"
    idx_open: int = content.find(tag_open)
    if idx_open != -1:
        idx_open += len(tag_open)
        content = content[idx_open:]
    idx_close: int = content.find(tag_close)
    if idx_close != -1:
        content = content[:idx_close]
    if strip:
        content = content.strip()
    return content
