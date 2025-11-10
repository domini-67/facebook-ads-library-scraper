thonimport argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.helpers import (
    http_get_json,
    load_json_file,
    save_json_file,
    setup_logging,
)
from utils.validators import validate_settings
from extractors.ad_parser import parse_ads
from extractors.media_handler import download_media_assets

LOGGER = logging.getLogger(__name__)

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Facebook Ads Library Scraper - extract structured ad data."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to JSON settings file (default: src/config/settings.example.json).",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=None,
        help="Override maxItems from config.",
    )
    parser.add_argument(
        "--search-term",
        type=str,
        default=None,
        help="Override first search term from config.",
    )
    parser.add_argument(
        "--country",
        type=str,
        default=None,
        help="Override first country from config (e.g. US, PK).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Override output JSON path.",
    )
    parser.add_argument(
        "--offline-input",
        type=str,
        default=None,
        help="Path to a local JSON file to use instead of live scraping.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Force live scraping mode (if API is configured).",
    )
    parser.add_argument(
        "--download-media",
        action="store_true",
        help="Download image assets for each ad.",
    )
    return parser.parse_args(argv)

def load_settings(config_path: Optional[str], project_root: Path) -> Dict[str, Any]:
    if config_path is None:
        config_path = project_root / "src" / "config" / "settings.example.json"
    else:
        config_path = Path(config_path)

    try:
        raw = load_json_file(config_path)
        LOGGER.info("Loaded settings from %s", config_path)
    except FileNotFoundError:
        LOGGER.warning(
            "Settings file %s not found; falling back to internal defaults.", config_path
        )
        raw = {}

    settings = validate_settings(raw)

    # Resolve file system paths relative to project root
    def resolve_path(p: str) -> str:
        path = Path(p)
        if not path.is_absolute():
            path = project_root / path
        return str(path)

    settings["output_path"] = resolve_path(settings["output_path"])
    settings["offline_input_path"] = resolve_path(settings["offline_input_path"])
    settings["media_download_dir"] = resolve_path(settings["media_download_dir"])

    return settings

def apply_cli_overrides(settings: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    if args.max_items is not None:
        settings["max_items"] = max(1, int(args.max_items))
    if args.search_term:
        # Keep override as a single-term list
        settings["search_terms"] = [args.search_term]
    if args.country:
        settings["countries"] = [args.country.upper()]
    if args.output:
        settings["output_path"] = str(Path(args.output))
    if args.offline_input:
        settings["offline_input_path"] = str(Path(args.offline_input))
    if args.live:
        settings["live_mode"] = True
    if args.download_media:
        settings["download_media"] = True

    return settings

def build_query_params(settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build query parameters for a generic HTTP-based ads endpoint.

    This is intentionally generic so you can point it at your own proxy or
    scraping backend which exposes a Facebook Ads Library compatible interface.
    """
    search_term = settings["search_terms"][0] if settings["search_terms"] else ""
    country = settings["countries"][0] if settings["countries"] else ""

    params: Dict[str, Any] = {
        "q": search_term,
        "country": country,
        "limit": settings["max_items"],
    }
    # Additional params for custom backends can be added here
    return params

def fetch_ads_live(settings: Dict[str, Any]) -> List[Dict[str, Any]]:
    api_url = settings["api_url"]
    if not api_url:
        raise RuntimeError(
            "No 'api_url' configured for live mode. "
            "Update your settings file with a reachable backend URL."
        )

    params = build_query_params(settings)
    LOGGER.info("Fetching ads from live API: %s", api_url)
    response_data = http_get_json(api_url, params=params)

    # Accept either a top-level list or an object with 'data'
    if isinstance(response_data, list):
        return response_data
    if isinstance(response_data, dict) and "data" in response_data:
        data = response_data["data"]
        if isinstance(data, list):
            return data
        raise ValueError("Expected 'data' to be a list in live API response.")
    raise ValueError("Unexpected data format from live API.")

def fetch_ads_offline(settings: Dict[str, Any]) -> List[Dict[str, Any]]:
    input_path = Path(settings["offline_input_path"])
    LOGGER.info("Loading offline input data from %s", input_path)
    raw = load_json_file(input_path)

    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and "data" in raw and isinstance(raw["data"], list):
        return raw["data"]

    raise ValueError(
        f"Offline input file {input_path} did not contain a list or an object with 'data'."
    )

def run() -> int:
    project_root = Path(__file__).resolve().parents[1]
    setup_logging()

    args = parse_args()
    LOGGER.debug("CLI arguments: %s", args)

    settings = load_settings(args.config, project_root)
    settings = apply_cli_overrides(settings, args)

    LOGGER.info("Effective settings: max_items=%d, live_mode=%s",
                settings["max_items"], settings["live_mode"])

    # Load raw ads either from live API or offline file
    try:
        if settings["live_mode"]:
            try:
                raw_ads = fetch_ads_live(settings)
            except Exception as live_err:
                LOGGER.error(
                    "Live scraping failed: %s. Falling back to offline input.",
                    live_err,
                )
                raw_ads = fetch_ads_offline(settings)
        else:
            raw_ads = fetch_ads_offline(settings)
    except Exception as err:
        LOGGER.exception("Failed to load raw ads data: %s", err)
        return 1

    LOGGER.info("Loaded %d raw ad records.", len(raw_ads))

    # Normalize and parse ads
    try:
        parsed_ads = parse_ads(raw_ads)
    except Exception as err:
        LOGGER.exception("Failed to parse ads: %s", err)
        return 1

    LOGGER.info("Parsed %d ads into normalized structure.", len(parsed_ads))

    output_path = Path(settings["output_path"])
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_json_file(output_path, parsed_ads)
    except Exception as err:
        LOGGER.exception("Failed to write output file %s: %s", output_path, err)
        return 1

    LOGGER.info("Wrote normalized ads to %s", output_path)

    # Optionally download image media
    if settings.get("download_media"):
        media_dir = Path(settings["media_download_dir"])
        try:
            download_media_assets(parsed_ads, media_dir)
        except Exception as err:
            LOGGER.exception("Media download encountered an error: %s", err)

    LOGGER.info("Facebook Ads Library scraping flow completed successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(run())