thonimport json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests

LOGGER = logging.getLogger(__name__)

def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure root logger with a simple, readable format.
    """
    if logging.getLogger().handlers:
        # Already configured
        return

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

def load_json_file(path: Path) -> Any:
    """
    Load JSON from a file, raising FileNotFoundError or json.JSONDecodeError
    if something goes wrong.
    """
    path = Path(path)
    LOGGER.debug("Loading JSON from %s", path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_json_file(path: Path, data: Any, pretty: bool = True) -> None:
    """
    Save Python data as JSON to a file.
    """
    path = Path(path)
    LOGGER.debug("Saving JSON to %s", path)
    indent = 2 if pretty else None
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def http_get_json(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 15,
) -> Any:
    """
    Perform an HTTP GET and decode the response as JSON.

    Raises requests.RequestException for network errors and json.JSONDecodeError
    if the response cannot be parsed.
    """
    LOGGER.debug("HTTP GET %s params=%s", url, params)
    try:
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as err:
        LOGGER.error("HTTP GET failed for %s: %s", url, err)
        raise

    try:
        return resp.json()
    except ValueError as err:
        LOGGER.error("Failed to decode JSON from %s: %s", url, err)
        raise