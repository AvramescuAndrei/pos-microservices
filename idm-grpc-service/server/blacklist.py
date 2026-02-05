blacklisted_tokens = set()


def add(token: str):
    blacklisted_tokens.add(token)


def contains(token: str) -> bool:
    return token in blacklisted_tokens
