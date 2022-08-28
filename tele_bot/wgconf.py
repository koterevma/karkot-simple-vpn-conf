import logging
from pathlib import Path


logger = logging.getLogger(__name__)


wg_configs_dir = Path("./wireguard")


def _get_unoccupied_configs() -> list[Path]:
    unoccupied_configs: list[Path] = []
    if not wg_configs_dir.is_dir():
        logger.exception("Dir not found")

    for conf_dir in wg_configs_dir.glob("peer*"):
        if not (conf_dir / "occupied").is_file():
            unoccupied_configs.append(conf_dir)

    return unoccupied_configs


def get_new_config() -> Path:
    unoccupied_configs = _get_unoccupied_configs()
    if not unoccupied_configs:
        raise RuntimeError("No available peers to give")

    occupied_dir = unoccupied_configs[0]
    occupied_file = occupied_dir / "occupied"
    occupied_file.touch(0o600)

    logging.info(f"Occupied {occupied_dir.name}, "
                 "remaining {len(unoccupied_configs) - 1}")

    return occupied_dir


def get_unoccupied_count():
    return len(_get_unoccupied_configs())
