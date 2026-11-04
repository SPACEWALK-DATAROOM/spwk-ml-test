# Local tests

Run `python3 -m unittest discover -s tests -v` from the repository root.
Tests exercise the production `PolygonFillEnv` placement, overlap, range,
conversion, and reset behavior using local Shapely geometries.

The installed Shapely 2 release removed the `geometry.asPolygon` alias used by
this snapshot. Tests restore the historical alias to `geometry.Polygon` so the
production behavior can run without changing the repository or installing a
global package. Rendering and applicant training are not run.

Phase 2 additionally checks that selecting sample outlines changes placement validity and that a polygon hole rejects a central patch while allowing one in remaining interior space:

```sh
python3 -m unittest discover -s tests -p 'test_phase2_space_geometry.py' -v
```
