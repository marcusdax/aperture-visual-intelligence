# Upstream ecosystem register

All upstream links are official project repositories. APERTURE maintains its own adapters/configuration and does not fork or redistribute upstream code, weights, or datasets by default. Status `catalogued` means only that the project has an APERTURE registry entry; it does not claim an operational adapter.

| Project | Official source | Planned boundary | License/usage gate |
|---|---|---|---|
| RF-DETR | [roboflow/rf-detr](https://github.com/roboflow/rf-detr) | Local model adapter | Upstream distinguishes Apache-2.0 code from model-weight terms. Check the exact model family and weight license before deployment. |
| Supervision | [roboflow/supervision](https://github.com/roboflow/supervision) | Detection/annotation data conversion | Verify the pinned release license and API before adding a dependency. |
| PaddleOCR | [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | OCR adapter | Code is Apache-2.0; verify the selected model and Paddle runtime/platform compatibility. |
| SAM 2 | [facebookresearch/sam2](https://github.com/facebookresearch/sam2) | Prompted segmentation adapter | Repository states Apache-2.0 for code and checkpoints; GPU memory and runtime depend on checkpoint, image/video size, and batching. |
| SamGeo | [opengeos/segment-geospatial](https://github.com/opengeos/segment-geospatial) | Geospatial segmentation orchestration | Verify project and model licenses independently; hardware follows the selected segmentation model. |
| GlobalMLBuildingFootprints | [microsoft/GlobalMLBuildingFootprints](https://github.com/microsoft/GlobalMLBuildingFootprints) | Optional external reference dataset | Dataset is CDLA-Permissive-2.0. Coverage and imagery vintage vary; large regional downloads require storage and network planning. |
| TiTiler | [developmentseed/titiler](https://github.com/developmentseed/titiler) | HTTP raster tile service | Pin and verify the server release/license; deployment needs compatible rasterio/GDAL and object-store access for the chosen source. |
| TorchGeo | [torchgeo/torchgeo](https://github.com/torchgeo/torchgeo) | Geospatial dataset/model utilities | Verify release and each dataset/model license; PyTorch accelerator requirements depend on workload. |
| PySTAC | [stac-utils/pystac](https://github.com/stac-utils/pystac) | STAC catalog and item parsing | Verify pinned release license; core catalog parsing does not require a GPU. |
| CVAT | [cvat-ai/cvat](https://github.com/cvat-ai/cvat) | Annotation service API | Community code is MIT; account for separately licensed bundled components and deployment requirements. |
| FiftyOne | [voxel51/fiftyone](https://github.com/voxel51/fiftyone) | Dataset inspection/export | Verify current package license and optional plugin/model terms; GPU is only relevant to optional model workloads. |
| Roboflow Inference | [roboflow/inference](https://github.com/roboflow/inference) | Self-hosted inference HTTP service | Core is Apache-2.0; model licenses vary, enterprise components are separately licensed, and cloud features require account/API credentials. |
| rembg | [danielgatis/rembg](https://github.com/danielgatis/rembg) | Background removal adapter | Code is MIT; model weights have individual terms (some restrict commercial use). Verify the selected model before use. |

No upstream package, checkpoint, data, external service, or hardware capability is enabled by this catalog. Before enabling one, record pinned version, API contract, license for code and weights/data, supported runtime, hardware floor, and a reproducible smoke test. Hardware requirements are deliberately not generalized where upstream workloads vary by model, resolution, batch size, or deployment mode.
