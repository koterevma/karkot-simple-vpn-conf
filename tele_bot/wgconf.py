import logging
from pathlib import Path


logger = logging.getLogger(__name__)


wg_configs_dir = Path("./wireguard")


def get_new_config() -> Path:
    unoccupied_configs = []
    for conf_dir in wg_configs_dir.glob("peer*"):
        if not (conf_dir / "occupied").is_file():
            unoccupied_configs.append(conf_dir)

    if not unoccupied_configs:
        raise RuntimeError("No available peers to give")

    occupied_file = unoccupied_configs[0] / (unoccupied_configs[0].name + ".conf")
    occupied_file.touch(0o600, exist_ok=True)

    logging.info(f"Occupied {unoccupied_configs[0].name}, remaining {len(unoccupied_configs) - 1}")

    return unoccupied_configs[0]

