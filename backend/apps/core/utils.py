def get_text_preview(text, words_count):
    text_parts = text.split()
    text_preview_parts = text_parts[:words_count]
    if len(text_preview_parts) < len(text_parts):
        text_preview_parts[-1] += "..."

    return " ".join(text_preview_parts)
