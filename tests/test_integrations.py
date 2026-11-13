import unittest
from io import BytesIO
from unittest.mock import patch

from aperture.integrations import CATALOG, StacApiClient, titiler_cog_tilejson_url, validate_endpoint


class IntegrationCatalogTests(unittest.TestCase):
    def test_requested_upstreams_are_catalogued(self):
        self.assertEqual(13, len(CATALOG))
        self.assertTrue(all(item.upstream_url.startswith("https://") for item in CATALOG.values()))

    def test_accepts_http_service_endpoint(self):
        self.assertEqual("https://tiles.example.org", validate_endpoint("https://tiles.example.org/", "titiler"))

    def test_rejects_unsafe_or_malformed_endpoint(self):
        for value in ("file:///tmp/a", "relative/path", "https://user:pass@example.org", "https://example.org/#token"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_endpoint(value, "stac")

    def test_rejects_unknown_service(self):
        with self.assertRaises(ValueError):
            validate_endpoint("https://example.org", "unknown")

    def test_titiler_cog_tilejson_url_encodes_source(self):
        url = titiler_cog_tilejson_url("https://tiles.example.org/", "https://data.example/a b.tif")
        self.assertEqual(
            "https://tiles.example.org/cog/WebMercatorQuad/tilejson.json?url=https%3A%2F%2Fdata.example%2Fa+b.tif",
            url,
        )

    def test_stac_search_posts_spec_fields_and_accepts_feature_collection(self):
        body = b'{"type":"FeatureCollection","features":[]}'
        with patch("aperture.integrations.urlopen", return_value=BytesIO(body)) as mocked:
            response = StacApiClient("https://catalog.example").search(
                collections=["sentinel"], bbox=[-10, 20, 10, 40], datetime="2025-01-01/2025-01-31", limit=7
            )
        self.assertEqual([], response["features"])
        request = mocked.call_args.args[0]
        self.assertEqual("https://catalog.example/search", request.full_url)
        self.assertEqual("POST", request.get_method())
        self.assertEqual(
            {"collections": ["sentinel"], "bbox": [-10, 20, 10, 40], "datetime": "2025-01-01/2025-01-31", "limit": 7},
            __import__("json").loads(request.data),
        )

    def test_stac_search_validates_bbox_and_response(self):
        with self.assertRaises(ValueError):
            StacApiClient("https://catalog.example").search(bbox=[5, 0, 1, 1])
        with patch("aperture.integrations.urlopen", return_value=BytesIO(b'{"type":"Feature"}')):
            with self.assertRaises(ValueError):
                StacApiClient("https://catalog.example").search()


if __name__ == "__main__":
    unittest.main()
