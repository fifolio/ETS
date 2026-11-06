def build_display_name(name: str) -> str:
    """First name plus the initial of the last name, for example "Firas D."."""
    parts = name.split()
    if not parts:
        return "Anonymous"
    first = parts[0][:1].upper() + parts[0][1:]
    if len(parts) == 1:
        return first
    return f"{first} {parts[-1][:1].upper()}."
