import re

def normalize_text(text: str) -> str:
    if not text:
        return ""

    # Replace multiple spaces/newlines with clean single spacing
    text = text.replace("\xa0", " ")  # non-breaking spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove vertical tabs and other noise control characters
    text = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]", "", text)

    # Remove emojis and decorative icons
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # dingbats
        "\U0001f926-\U0001f937"  # gestures
        "\U00010000-\U0010ffff"  # other unicode
        "\u2640-\u2642"  # gender symbols
        "\u2600-\u2B55"  # misc symbols
        "\u200d"  # zero width joiner
        "\u23cf"  # eject symbol
        "\u23e9"  # fast forward
        "\u231a"  # watch
        "\ufe0f"  # variation selector
        "\u3030"  # wavy dash
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)

    # Remove common footer noise
    text = re.sub(r"© \d{4} McGraw-Hill Education$", "", text, flags=re.MULTILINE)
    text = re.sub(r"© \d{4} McGraw-Hill Education\.?$", "", text, flags=re.MULTILINE)

    return text.strip()
