# CFD-Style Flow Visualization in ParaView

**Portfolio type:** Scientific visualization / ParaView / Python automation  
**Complexity:** Easy to medium  
**Primary tool:** ParaView command-line Python (`pvpython`)  
**Dataset used for included outputs:** `data/fallback_cylinder_flow.vtk`

I built this project to demonstrate a reproducible ParaView workflow for CFD-style flow visualization without relying on the ParaView GUI. The project loads a VTK structured-grid dataset, identifies scalar and vector fields, creates ParaView filters, exports screenshots, saves a `.pvsm` state file, and generates a camera-orbit video.

The included dataset is a small analytic cylinder-flow-style sample with these fields:

- `speed` — scalar field used for color mapping
- `Cp` — pressure-coefficient-style scalar field
- `velocity` — vector field used for streamlines

This is a visualization and workflow project, not a claim of running a high-fidelity CFD solver. I used the dataset to show that I can build, automate, document, and validate ParaView visualization pipelines.

## Final outputs

```text
screenshots/01_scalar_slice.png
screenshots/02_contour_or_threshold.png
screenshots/03_streamlines.png
screenshots/04_combined_view.png
paraview/flow_pipeline.pvsm
animation/flow_orbit.mp4
metadata/run_summary.json
```

## What I demonstrated

- Loaded and visualized VTK scientific data in ParaView
- Used scalar fields and vector fields appropriately
- Created slice, contour/threshold, streamline, and tube-based views
- Exported reproducible screenshots and a camera-orbit animation
- Saved a portable `.pvsm` ParaView state file
- Documented validation notes for AI-training-style technical review

## Folder structure

```text
paraview_cfd_flow_portfolio/
├── README.md
├── PROJECT_CARD.md
├── portfolio.html
├── data/
│   ├── README.md
│   └── fallback_cylinder_flow.vtk
├── scripts/
│   ├── build_paraview_pipeline.py
│   └── export_orbit_frames.py
├── screenshots/
│   ├── 01_scalar_slice.png
│   ├── 02_contour_or_threshold.png
│   ├── 03_streamlines.png
│   └── 04_combined_view.png
├── animation/
│   └── flow_orbit.mp4
├── paraview/
│   ├── README.md
│   └── flow_pipeline.pvsm
├── docs/
│   ├── workflow.md
│   ├── ai_evaluation_notes.md
│   ├── video_instructions.md
│   └── resume_linkedin_blurb.md
└── metadata/
    ├── project_summary.json
    └── run_summary.json
```

## Reproduce the project without the GUI

From the project root:

```bash
pvpython scripts/build_paraview_pipeline.py --input data/fallback_cylinder_flow.vtk
pvpython scripts/export_orbit_frames.py --state paraview/flow_pipeline.pvsm --frames 120
ffmpeg -framerate 24 -start_number 0 -i animation/frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p animation/flow_orbit.mp4
```

On my Mac, ParaView was installed through Homebrew, so I used the full path:

```bash
"/Applications/ParaView-6.1.1.app/Contents/bin/pvpython" scripts/build_paraview_pipeline.py --input data/fallback_cylinder_flow.vtk
"/Applications/ParaView-6.1.1.app/Contents/bin/pvpython" scripts/export_orbit_frames.py --state paraview/flow_pipeline.pvsm --frames 120
```

## Resume bullet

Built a reproducible scientific visualization workflow in ParaView using `pvpython`, including dataset loading, scalar slicing, contour/threshold visualization, vector-field streamlines, tube rendering, color mapping, screenshot export, `.pvsm` state saving, and MP4 animation creation.
