# Workflow Documentation

## Project objective

I created a reproducible CFD-style scientific visualization workflow using ParaView and Python automation. The project demonstrates how I can load scientific data, inspect scalar and vector fields, apply visualization filters, export results, and document the workflow for technical review.

## Main visualization pipeline

```text
Load VTK dataset
  ↓
Identify scalar and vector fields
  ↓
Create scalar slice view
  ↓
Create contour or threshold view
  ↓
Create streamlines from the vector field
  ↓
Apply tube filter to streamlines
  ↓
Color outputs by scalar field
  ↓
Export screenshots
  ↓
Save ParaView state file
  ↓
Export camera-orbit frames and MP4 video
```

## Filters and tools used

| Step | ParaView filter/tool | Purpose |
|---|---|---|
| Load data | `OpenDataFile` | Load the VTK scientific dataset |
| Slice view | `Slice` | Inspect a planar cross-section of a scalar field |
| Contour / isosurface | `Contour` | Show locations where a scalar variable reaches an iso-value |
| Threshold fallback | `Threshold` | Isolate scalar ranges if contouring is not suitable |
| Streamlines | `StreamTracer` | Visualize vector-field direction and flow structure |
| Tube | `Tube` | Give streamline curves visible 3D thickness |
| Color mapping | `ColorBy` | Map scalar values to visual color |
| Screenshot export | `SaveScreenshot` | Produce portfolio-ready images |
| State saving | `SaveState` | Save a reproducible `.pvsm` project state |
| Frame export | `SaveScreenshot` in an orbit loop | Generate frames for the final MP4 animation |

## Final outputs

```text
screenshots/01_scalar_slice.png
screenshots/02_contour_or_threshold.png
screenshots/03_streamlines.png
screenshots/04_combined_view.png
paraview/flow_pipeline.pvsm
metadata/run_summary.json
animation/flow_orbit.mp4
```

## Validation checks I used

A successful run should show:

- a scalar field selected for color mapping, such as `speed`
- a vector field selected for streamlines, such as `velocity`
- `streamlines_created: true` in `metadata/run_summary.json`
- four screenshot files in `screenshots/`
- a saved ParaView state file in `paraview/`
- a playable MP4 video in `animation/`

The actual successful run summary for this package is:

```json
{
  "input": "data/fallback_cylinder_flow.vtk",
  "scalar_field_used": "speed",
  "vector_field_used": "velocity",
  "streamlines_created": true
}
```
