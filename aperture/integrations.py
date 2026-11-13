"""Small, dependency-free contracts for APERTURE external integrations."""

from dataclasses import dataclass
import json
from urllib.parse import urlsplit
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Integration:
    key: str
    name: str
    upstream_url: str
    category: str
    mode: str
    status: str = "catalogued"


CATALOG = {
    item.key: item
    for item in (
        Integration("rf_detr", "RF-DETR", "https://github.com/roboflow/rf-detr", "detection", "local-model"),
        Integration("supervision", "Supervision", "https://github.com/roboflow/supervision", "vision-utilities", "python-library"),
        Integration("paddleocr", "PaddleOCR", "https://github.com/PaddlePaddle/PaddleOCR", "ocr", "local-model"),
        Integration("sam2", "SAM 2", "https://github.com/facebookresearch/sam2", "segmentation", "local-model"),
        Integration("samgeo", "SamGeo", "https://github.com/opengeos/segment-geospatial", "geospatial-segmentation", "python-library"),
        Integration("building_footprints", "GlobalMLBuildingFootprints", "https://github.com/microsoft/GlobalMLBuildingFootprints", "reference-data", "remote-dataset"),
        Integration("titiler", "TiTiler", "https://github.com/developmentseed/titiler", "raster-serving", "http-service"),
        Integration("torchgeo", "TorchGeo", "https://github.com/torchgeo/torchgeo", "geospatial-ml", "python-library"),
        Integration("pystac", "PySTAC", "https://github.com/stac-utils/pystac", "catalog", "python-library"),
        Integration("cvat", "CVAT", "https://github.com/cvat-ai/cvat", "annotation", "http-service"),
        Integration("fiftyone", "FiftyOne", "https://github.com/voxel51/fiftyone", "dataset-inspection", "python-library"),
        Integration("roboflow_inference", "Roboflow Inference", "https://github.com/roboflow/inference", "inference", "http-service"),
        Integration("rembg", "rembg", "https://github.com/danielgatis/rembg", "background-removal", "python-library"),
    )
}


def validate_endpoint(url: str, service: str) -> str:
    """Validate and normalize a service base URL without making a network call.

    Only HTTP(S) URLs with a hostname are accepted. Credentials and fragments are
    rejected to keep secrets out of endpoint configuration and logs.
    """
    if service not in {"stac", "titiler", "cvat", "roboflow_inference"}:
        raise ValueError(f"Unsupported HTTP service: {service}")
    parts = urlsplit(url.strip())
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError("Endpoint must be an absolute HTTP(S) URL with a hostname")
    if parts.username or parts.password or parts.fragment:
        raise ValueError("Endpoint must not include credentials or a URL fragment")
    return url.rstrip("/")


class StacApiClient:
    """Minimal STAC API Item Search client (POST /search, GeoJSON response)."""

    def __init__(self, endpoint: str, timeout: float = 20.0):
        self.endpoint = validate_endpoint(endpoint, "stac")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.timeout = timeout

    def search(self, *, collections: list[str] | None = None, bbox: list[float] | None = None,
               datetime: str | None = None, limit: int = 100) -> dict:
        if not 1 <= limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")
        if bbox is not None and (len(bbox) != 4 or bbox[0] > bbox[2] or bbox[1] > bbox[3]):
            raise ValueError("bbox must be [west, south, east, north] with ordered bounds")
        payload = {"limit": limit}
        if collections:
            payload["collections"] = collections
        if bbox is not None:
            payload["bbox"] = bbox
        if datetime:
            payload["datetime"] = datetime
        request = Request(
            f"{self.endpoint}/search", data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/geo+json, application/json"},
            method="POST",
        )
        with urlopen(request, timeout=self.timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
        if not isinstance(result, dict) or result.get("type") != "FeatureCollection" or not isinstance(result.get("features"), list):
            raise ValueError("STAC search response is not a GeoJSON FeatureCollection")
        return result


def titiler_cog_tilejson_url(endpoint: str, cog_url: str, *, tile_matrix_set: str = "WebMercatorQuad") -> str:
    """Build TiTiler's documented COG TileJSON URL; does not fetch the resource."""
    base = validate_endpoint(endpoint, "titiler")
    source = urlsplit(cog_url)
    if source.scheme not in {"http", "https", "s3", "gs", "az"} or not source.netloc:
        raise ValueError("COG URL must be an absolute http(s), s3, gs, or az URL")
    if not tile_matrix_set or any(ch in tile_matrix_set for ch in "/?#"):
        raise ValueError("tile_matrix_set must be a non-empty path segment")
    return f"{base}/cog/{tile_matrix_set}/tilejson.json?{urlencode({'url': cog_url})}"
