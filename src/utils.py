
def vprint(text: str, config: dict) -> None:
    if config.get('verbose'):
        print(text)