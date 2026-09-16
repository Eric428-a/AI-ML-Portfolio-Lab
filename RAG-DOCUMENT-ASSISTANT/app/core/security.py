import secrets


def generate_id(length: int = 16) -> str:
    return secrets.token_urlsafe(length)


def safe_filename(filename: str) -> str:
    filename = filename.replace("\\", "/")
    filename = filename.split("/")[-1]

    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "._-"
    )

    return "".join(
        character
        for character in filename
        if character in allowed
    ) or "document"