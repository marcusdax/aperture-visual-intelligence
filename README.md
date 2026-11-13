# APERTURE — Visual Intelligence

APERTURE is an integration layer for geospatial and visual intelligence workflows. It connects upstream tools through APERTURE-owned adapters and configuration; it does not vendor or fork upstream projects.

## Repository status

This repository was empty when inspected on 2026-11-12: it had no commits, branches, issues, pull requests, or source files. The referenced prior chat preview did not include sprint requirements. This initial implementation establishes a tested integration registry and endpoint configuration contract. It does not claim model inference or production integrations yet.

## Quick start

Python 3.11+; no runtime dependencies are required for the registry/configuration layer.

```python
from aperture.integrations import CATALOG, validate_endpoint

print(CATALOG["pystac"].upstream_url)
validate_endpoint("https://example.org/stac", "stac")

# Read-only STAC API search and TiTiler COG URL generation
from aperture.integrations import StacApiClient, titiler_cog_tilejson_url
items = StacApiClient("https://earth-search.aws.element84.com/v1").search(limit=5)
tilejson = titiler_cog_tilejson_url("https://tiles.example.org", "https://data.example/scene.tif")
```

`StacApiClient.search` sends a GeoJSON-compatible POST to `/search` and validates the FeatureCollection response. `titiler_cog_tilejson_url` constructs TiTiler's documented COG TileJSON endpoint URL; it does not request the tile service or fetch imagery.

Run checks with `python -m unittest discover -s tests`.

See [the ecosystem register](docs/ecosystem.md), [roadmap](docs/roadmap.md), and [sprint report](docs/sprints/2026-11-12.md).
