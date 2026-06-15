# ParaView State Output

This directory contains the generated ParaView state file:

```text
flow_pipeline.pvsm
```

A `.pvsm` file saves the ParaView application state: data sources, filters, views, color maps, camera settings, layouts, and pipeline properties.

For portability, the included state file uses a relative data path:

```text
data/fallback_cylinder_flow.vtk
```

If the state file does not load correctly on another machine, regenerate it from the project root:

```bash
pvpython scripts/build_paraview_pipeline.py --input data/fallback_cylinder_flow.vtk
```
