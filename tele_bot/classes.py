from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: int
    is_admin: int = 0
    config_path: str | None = None
