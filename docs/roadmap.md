# Roadmap

## Sprint 0 — repository bootstrap (2026-11-12)

- [x] Inspect exact repository state and record empty baseline.
- [x] Establish a dependency-free APERTURE integration catalog and URL validation contract.
- [x] Add automated tests and an upstream/license review register.
- [ ] Obtain the omitted previous sprint acceptance criteria from the referenced conversation.

## Sprint 1 — first operational adapters

1. [x] Implement a read-only STAC API search adapter with fixture-backed tests.
2. [x] Implement TiTiler COG TileJSON URL generation against its documented API.
3. Add service health/capability probes for CVAT and Roboflow Inference without logging credentials.
4. Pin dependencies and verify supported Python/GDAL/PyTorch/CUDA combinations against upstream release notes.
5. Add one end-to-end demo over public sample imagery; state data/model terms alongside the demo.

## Later

- Add local model adapters (RF-DETR, PaddleOCR, SAM 2, rembg) after model-weight and hardware gates are explicit.
- Add dataset/annotation flows for Supervision, SamGeo, TorchGeo, FiftyOne, CVAT, and GlobalMLBuildingFootprints.
- Add CI, containerized service profiles, observability, and deployment documentation after runtime choices are confirmed.
