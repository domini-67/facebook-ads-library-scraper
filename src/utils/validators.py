thonfrom typing import Any, Dict, List
import logging

LOGGER = logging.getLogger(__name__)

def _ensure_list_of_strings(value: Any, default: List[str]) -> List[str]:
    if value is None:
        return list(default)
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]

def validate_settings(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize settings loaded from JSON.

    Returns a new dictionary with safe defaults applied.
    """
    settings: Dict[str, Any] = {}

    settings["search_terms"] = _ensure_list_of_strings(
        raw.get("search_terms"), default=["salon"]
    )
    settings["countries"] = [
        c.upper() for c in _ensure_list_of_strings(raw.get("countries"), default=["PK"])
    ]

    # Max items to retrieve
    try:
        max_items = int(raw.get("max_items", raw.get("maxItems", 50)))
    except (TypeError, ValueError):
        LOGGER.warning("Invalid max_items in settings; falling back to 50.")
        max_items = 50
    settings["max_items"] = max(1, max_items)

    # Output path (relative paths will be resolved in main.py)
    output_path = raw.get("output_path") or raw.get("output") or "data/output.sample.json"
    settings["output_path"] = str(output_path)

    # Offline input file with raw data
    offline_input_path = raw.get("offline_input_path") or raw.get("input") or "data/input.sample.json"
    settings["offline_input_path"] = str(offline_input_path)

    # Media download config
    settings["download_media"] = bool(raw.get("download_media", False))
    settings["media_download_dir"] = str(
        raw.get("media_download_dir", "data/media")
    )

    # Live scraping mode
    settings["live_mode"] = bool(raw.get("live_mode", False))

    # HTTP API endpoint
    settings["api_url"] = str(raw.get("api_url", ""))
    if settings["live_mode"] and not settings["api_url"]:
        LOGGER.warning(
            "live_mode is enabled but no api_url is configured. "
            "Live scraping will fail until api_url is set."
        )

    LOGGER.debug("Validated settings: %s", settings)
    return settings