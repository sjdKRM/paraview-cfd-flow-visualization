# Video Creation Instructions

I generated the video without opening the ParaView GUI. The workflow uses `pvpython` to export PNG frames and `ffmpeg` to convert those frames into an MP4.

## Step 1 — Generate the state file and screenshots

From the project root:

```bash
pvpython scripts/build_paraview_pipeline.py --input data/fallback_cylinder_flow.vtk
```

On macOS with ParaView 6.1.1 installed through Homebrew, the command can be run with the full path:

```bash
"/Applications/ParaView-6.1.1.app/Contents/bin/pvpython" scripts/build_paraview_pipeline.py --input data/fallback_cylinder_flow.vtk
```

This creates:

```text
paraview/flow_pipeline.pvsm
screenshots/01_scalar_slice.png
screenshots/02_contour_or_threshold.png
screenshots/03_streamlines.png
screenshots/04_combined_view.png
metadata/run_summary.json
```

## Step 2 — Generate orbit frames

```bash
pvpython scripts/export_orbit_frames.py --state paraview/flow_pipeline.pvsm --frames 120
```

macOS full-path version:

```bash
"/Applications/ParaView-6.1.1.app/Contents/bin/pvpython" scripts/export_orbit_frames.py --state paraview/flow_pipeline.pvsm --frames 120
```

This creates:

```text
animation/frames/frame_0000.png
animation/frames/frame_0001.png
...
animation/frames/frame_0119.png
```

## Step 3 — Convert frames to MP4

```bash
ffmpeg -framerate 24 -start_number 0 -i animation/frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p animation/flow_orbit.mp4
```

The final video is:

```text
animation/flow_orbit.mp4
```

## Platform notes

### macOS

Install ParaView and ffmpeg:

```bash
brew install --cask paraview
brew install ffmpeg
```

Find `pvpython`:

```bash
find /Applications -path "*ParaView*.app/Contents/bin/pvpython" -type f 2>/dev/null
```

### Windows

`pvpython.exe` is usually under a path like:

```text
C:\Program Files\ParaView 6.1.1\bin\pvpython.exe
```

Example PowerShell command:

```powershell
& "C:\Program Files\ParaView 6.1.1\bin\pvpython.exe" scripts\build_paraview_pipeline.py --input data\fallback_cylinder_flow.vtk
```

### Linux

```bash
which pvpython
pvpython scripts/build_paraview_pipeline.py --input data/fallback_cylinder_flow.vtk
sudo apt install ffmpeg
```

## Troubleshooting notes

### `pvpython: command not found`

ParaView is installed, but its `pvpython` executable is not on the shell PATH. Use the full path to `pvpython`.

### `ffmpeg` cannot find frame files

The frame export step did not run, or the command was run from the wrong directory. Check:

```bash
ls animation/frames | head
```

### OpenVKL warnings appear on macOS

ParaView may print OpenVKL rendering warnings on some macOS installations. In this project, the warnings did not prevent the screenshots, `.pvsm` state, PNG frames, or MP4 video from being created.
