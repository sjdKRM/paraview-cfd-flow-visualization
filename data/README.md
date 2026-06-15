# Data

## Dataset used in this project

The included outputs were generated from:

```text
data/fallback_cylinder_flow.vtk
```

This is a small VTK structured-grid dataset representing an analytic cylinder-flow-style vector field. It contains:

- `speed` — scalar velocity-magnitude-style field
- `Cp` — pressure-coefficient-style scalar field
- `velocity` — vector field for streamlines

I used this dataset because it is lightweight, reproducible, and easy to inspect in ParaView. It is appropriate for demonstrating a scientific visualization workflow, but it should be described as a **CFD-style analytic sample**, not as a high-fidelity CFD simulation result.

## Notes

The project scripts can also be adapted to public ParaView tutorial datasets, Exodus files, VTK files, or other simulation outputs. The included screenshots, state file, and video in this package were generated from `fallback_cylinder_flow.vtk`.
