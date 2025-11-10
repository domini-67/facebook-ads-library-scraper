thonfrom typing import Any, Dict, List, Union
import logging

LOGGER = logging.getLogger(__name__)

def _extract_snapshot(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize the snapshot/body/images subtree to the format:

    {
      "body": {
        "text": "..."
      },
      "cta_text": "...",
      "images": [{"original_image_url": "..."}]
    }
    """
    snapshot: Dict[str, Any] = raw.get("snapshot") or {}

    # Body text
    body = snapshot.get("body") or {}
    body_text = None

    if isinstance(body, dict):
        body_text = body.get("text") or body.get("message") or body.get("content")
    elif isinstance(body, str):
        body_text = body

    if body_text is None:
        # Try alternative locations
        body_text = raw.get("ad_text") or raw.get("message") or ""

    normalized_body = {"text": str(body_text)} if body_text is not None else {"text": ""}

    # CTA text
    cta_text = snapshot.get("cta_text")
    if not cta_text:
        cta = snapshot.get("cta") or raw.get("cta") or {}
        if isinstance(cta, dict):
            cta_text = cta.get("title") or cta.get("text")
        elif isinstance(cta, str):
            cta_text = cta

    # Images
    images = snapshot.get("images")
    normalized_images: List[Dict[str, Any]] = []

    if isinstance(images, list):
        for img in images:
            if isinstance(img, dict):
                url = img.get("original_image_url") or img.get("url")
                if url:
                    normalized_images.append({"original_image_url": url})
    # Try alternative fields
    if not normalized_images:
        creatives = raw.get("creatives") or []
        if isinstance(creatives, list):
            for creative in creatives:
                if not isinstance(creative, dict):
                    continue
                url = (
                    creative.get("image_url")
                    or creative.get("thumbnail_url")
                    or creative.get("media_url")
                )
                if url:
                    normalized_images.append({"original_image_url": url})

    return {
        "body": normalized_body,
        "cta_text": cta_text or "",
        "images": normalized_images,
    }

def _extract_publisher_platforms(raw: Dict[str, Any]) -> List[str]:
    platforms = raw.get("publisher_platform") or raw.get("publisher_platforms")
    if isinstance(platforms, list):
        return [str(p).upper() for p in platforms]
    if isinstance(platforms, str):
        return [platforms.upper()]

    # Some APIs nest placements
    placement = raw.get("placement") or {}
    if isinstance(placement, dict):
        platforms = placement.get("platforms") or placement.get("publisher_platform")
        if isinstance(platforms, list):
            return [str(p).upper() for p in platforms]
        if isinstance(platforms, str):
            return [platforms.upper()]

    return []

def _extract_categories(raw: Dict[str, Any]) -> List[str]:
    categories = raw.get("categories") or raw.get("ad_reached_countries") or []
    if isinstance(categories, list):
        return [str(c) for c in categories]
    if isinstance(categories, str):
        return [categories]
    return []

def normalize_ad_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a raw ad structure from an arbitrary Facebook Ads Library-like
    endpoint to the normalized shape described in the README.
    """
    ad_archive_id = (
        raw.get("ad_archive_id")
        or raw.get("id")
        or raw.get("adid")
        or raw.get("ad_id")
    )
    page = raw.get("page") or {}
    if not isinstance(page, dict):
        page = {}

    page_id = raw.get("page_id") or page.get("id")
    page_name = raw.get("page_name") or page.get("name")
    page_profile_uri = (
        raw.get("page_profile_uri")
        or page.get("page_profile_uri")
        or page.get("url")
        or page.get("link")
    )

    publisher_platform = _extract_publisher_platforms(raw)

    page_like_count = (
        raw.get("page_like_count")
        or page.get("like_count")
        or page.get("fan_count")
        or 0
    )

    # Timestamps may be integers or ISO8601 strings.
    start_date = raw.get("start_date") or raw.get("ad_delivery_start_time")
    end_date = raw.get("end_date") or raw.get("ad_delivery_stop_time")

    categories = _extract_categories(raw)
    snapshot = _extract_snapshot(raw)

    normalized = {
        "ad_archive_id": ad_archive_id,
        "page_id": page_id,
        "page_name": page_name,
        "page_profile_uri": page_profile_uri,
        "publisher_platform": publisher_platform,
        "snapshot": snapshot,
        "page_like_count": page_like_count,
        "start_date": start_date,
        "end_date": end_date,
        "categories": categories,
    }

    LOGGER.debug("Normalized ad %s", ad_archive_id)
    return normalized

def parse_ads(raw_data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Take a list of raw ad objects (or a dict containing one) and normalize
    each record, skipping malformed entries but logging them.
    """
    if isinstance(raw_data, dict):
        if "data" in raw_data and isinstance(raw_data["data"], list):
            items = raw_data["data"]
        else:
            raise ValueError("Expected 'data' key with list when passing a dict to parse_ads.")
    elif isinstance(raw_data, list):
        items = raw_data
    else:
        raise TypeError("parse_ads expects a list of dicts or a dict with 'data'.")

    normalized_ads: List[Dict[str, Any]] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            LOGGER.warning("Skipping non-dict ad record at index %d", idx)
            continue
        try:
            normalized = normalize_ad_record(item)
            normalized_ads.append(normalized)
        except Exception as err:
            LOGGER.exception("Failed to normalize ad at index %d: %s", idx, err)

    return normalized_ads