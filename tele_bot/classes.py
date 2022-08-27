from dataclasses import dataclass

@dataclass(slots=True)
class User:
    id: int | None = None
    config_path: str | None = None
    is_admin: int | None = None


