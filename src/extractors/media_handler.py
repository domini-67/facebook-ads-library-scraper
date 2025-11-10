thonfrom pathlib import Path
from typing import Any, Dict, Iterable, List
import logging
import os
import uuid

import requests

LOGGER = logging.getLogger(__name__)

def extract_image_urls_from_ad(ad: Dict[str, Any]) -> List[str]:
    """
    Extract image URLs from a normalized ad structure.
    """
    urls: List[str] = []
    snapshot = ad.get("snapshot") or {}
    if isinstance(snapshot, dict):
        images = snapshot.get("images") or []
        if isinstance(images, list):
            for img in images:
                if not isinstance(img, dict):
                    continue
                url = img.get("original_image_url") or img.get("url")
                if url:
                    urls.append(str(url))

    return urls

def download_media_assets(
    ads: Iterable[Dict[str, Any]],
    download_dir: Path,
    timeout: int = 15,
) -> None:
    """
    Download image assets for each ad to the given directory.

    - Skips invalid URLs.
    - Avoids overwriting files by using UUIDs when necessary.
    """
    download_dir = Path(download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)
    LOGGER.info("Downloading media assets to %s", download_dir)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "facebook-ads-library-scraper/1.0 (+https://bitbash.dev)",
        }
    )

    count = 0
    for ad in ads:
        ad_id = ad.get("ad_archive_id") or "unknown"
        urls = extract_image_urls_from_ad(ad)
        if not urls:
            continue

        for url in urls:
            try:
                filename = _derive_filename(url, ad_id)
                filepath = download_dir / filename

                if filepath.exists():
                    LOGGER.debug("File already exists, skipping: %s", filepath)
                    continue

                LOGGER.debug("Downloading %s for ad %s", url, ad_id)
                resp = session.get(url, stream=True, timeout=timeout)
                resp.raise_for_status()

                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                count += 1
            except Exception as err:
                LOGGER.warning("Failed to download image for ad %s from %s: %s", ad_id, url, err)

    LOGGER.info("Finished downloading %d media files.", count)

def _derive_filename(url: str, ad_id: str) -> str:
    """
    Build a safe filename based on the URL and ad ID.
    """
    basename = os.path.basename(url.split("?", 1)[0]) or "image"
    if "." in basename:
        name, ext = basename.rsplit(".", 1)
        ext = "." + ext
    else:
        name, ext = basename, ".jpg"

    safe_name = f"{ad_id}_{name}".replace("/", "_").replace("\\", "_")
    unique_suffix = uuid.uuid4().hex[:8]
    return f"{safe_name}_{unique_suffix}{ext}"