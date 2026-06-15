#!/usr/bin/env pvpython
"""Build a ParaView scientific visualization pipeline without using the GUI.

Run with:

    pvpython scripts/build_paraview_pipeline.py --input data/fallback_cylinder_flow.vtk

The script saves screenshots, a ParaView state file, and a run summary.

Outputs:
    screenshots/01_scalar_slice.png
    screenshots/02_contour_or_threshold.png
    screenshots/03_streamlines.png
    screenshots/04_combined_view.png
    paraview/flow_pipeline.pvsm
    metadata/run_summary.json
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from paraview.simple import *  # type: ignore


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
PARAVIEW_DIR = PROJECT_ROOT / "paraview"
METADATA_DIR = PROJECT_ROOT / "metadata"

SCREENSHOT_DIR.mkdir(exist_ok=True)
PARAVIEW_DIR.mkdir(exist_ok=True)
METADATA_DIR.mkdir(exist_ok=True)


def choose_array(source, candidates, association="POINTS"):
    """Pick the first array name that exists, otherwise return the first candidate.

    ParaView array discovery differs by reader/filter. This function is intentionally
    defensive so the script works with both disk_out_ref.ex2 and the fallback VTK file.
    """
    try:
        info = source.GetDataInformation()
        if association == "POINTS":
            arrays = info.GetPointDataInformation()
        else:
            arrays = info.GetCellDataInformation()
        available = [arrays.GetArray(i).GetName() for i in range(arrays.GetNumberOfArrays())]
        lower = {a.lower(): a for a in available}
        for c in candidates:
            if c.lower() in lower:
                return lower[c.lower()]
        return available[0] if available else candidates[0]
    except Exception:
        return candidates[0]


def color_by_safe(display, association, name):
    try:
        ColorBy(display, (association, name))
        display.RescaleTransferFunctionToDataRange(True, False)
        display.SetScalarBarVisibility(GetActiveView(), True)
    except Exception:
        ColorBy(display, None)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input dataset path, e.g. data/disk_out_ref.ex2")
    parser.add_argument("--resolution", nargs=2, type=int, default=[1600, 1000])
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    # Run from the project root so relative paths inside the saved state stay portable.
    os.chdir(PROJECT_ROOT)

    # Reset the session so repeated runs are deterministic.
    ResetSession()

    data = OpenDataFile(str(input_path))
    data.UpdatePipeline()
    RenameSource("Input CFD/Flow Dataset", data)

    view = GetActiveViewOrCreate("RenderView")
    view.ViewSize = args.resolution
    view.Background = [1.0, 1.0, 1.0]

    # Make a best-effort guess for scalar/vector names.
    scalar_name = choose_array(data, ["speed", "velocity_magnitude", "Cp", "pressure", "Temp", "temp", "temperature"])
    vector_name = choose_array(data, ["velocity", "Velocity", "V", "vel", "U"])

    # Base display: translucent surface/mesh.
    base_display = Show(data, view)
    base_display.Representation = "Surface"
    base_display.Opacity = 0.20
    color_by_safe(base_display, "POINTS", scalar_name)
    view.ResetCamera()
    SaveScreenshot(str(SCREENSHOT_DIR / "01_scalar_slice.png"), view, ImageResolution=args.resolution)

    # Slice through the dataset.
    slice1 = Slice(registrationName="Midplane Scalar Slice", Input=data)
    try:
        slice1.SliceType = "Plane"
        slice1.SliceType.Normal = [0.0, 0.0, 1.0]
    except Exception:
        pass
    slice_display = Show(slice1, view)
    slice_display.Representation = "Surface"
    color_by_safe(slice_display, "POINTS", scalar_name)
    Hide(data, view)
    view.ResetCamera()
    SaveScreenshot(str(SCREENSHOT_DIR / "01_scalar_slice.png"), view, ImageResolution=args.resolution)

    # Contour, with fallback to threshold if contour fails for the input.
    try:
        contour1 = Contour(registrationName="Scalar Contour / Isosurface", Input=data)
        contour1.ContourBy = ["POINTS", scalar_name]
        # Let ParaView compute a reasonable iso-value by using the center of range when possible.
        try:
            data_info = data.GetDataInformation().GetPointDataInformation().GetArray(scalar_name)
            rng = data_info.GetRange()
            contour1.Isosurfaces = [(rng[0] + rng[1]) / 2.0]
        except Exception:
            pass
        contour_display = Show(contour1, view)
        contour_display.Representation = "Surface"
        color_by_safe(contour_display, "POINTS", scalar_name)
    except Exception:
        contour1 = Threshold(registrationName="Scalar Threshold", Input=data)
        contour1.Scalars = ["POINTS", scalar_name]
        contour_display = Show(contour1, view)
        contour_display.Representation = "Surface"
        color_by_safe(contour_display, "POINTS", scalar_name)

    Hide(slice1, view)
    view.ResetCamera()
    SaveScreenshot(str(SCREENSHOT_DIR / "02_contour_or_threshold.png"), view, ImageResolution=args.resolution)

    # Streamlines from vector field. This may fail if the selected dataset has no vector field.
    stream_created = False
    try:
        stream1 = StreamTracer(registrationName="Vector Streamlines", Input=data, SeedType="Point Cloud")
        stream1.Vectors = ["POINTS", vector_name]
        stream1.MaximumStreamlineLength = 20.0
        stream1.SeedType.NumberOfPoints = 150
        stream1.SeedType.Radius = 2.5
        stream1.SeedType.Center = [0.0, 0.0, 0.0]

        tube1 = Tube(registrationName="Streamline Tubes", Input=stream1)
        tube1.Radius = 0.025
        tube1.NumberofSides = 12
        tube_display = Show(tube1, view)
        tube_display.Representation = "Surface"
        try:
            ColorBy(tube_display, ("POINTS", scalar_name))
            tube_display.RescaleTransferFunctionToDataRange(True, False)
        except Exception:
            ColorBy(tube_display, None)
        stream_created = True
    except Exception as exc:
        print(f"Streamline step skipped: {exc}")

    Hide(contour1, view)
    if stream_created:
        view.ResetCamera()
        SaveScreenshot(str(SCREENSHOT_DIR / "03_streamlines.png"), view, ImageResolution=args.resolution)

    # Combined final view.
    try:
        Show(slice1, view)
        Show(contour1, view)
        if stream_created:
            Show(tube1, view)
    except Exception:
        pass
    view.ResetCamera()
    SaveScreenshot(str(SCREENSHOT_DIR / "04_combined_view.png"), view, ImageResolution=args.resolution)

    # Save reproducible ParaView state.
    state_path = PARAVIEW_DIR / "flow_pipeline.pvsm"
    SaveState(str(state_path))

    # Make the saved state portable by replacing the local absolute data path
    # with a path relative to the project root.
    try:
        relative_input = input_path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        relative_input = input_path.name
    try:
        text = state_path.read_text(encoding="utf-8")
        text = text.replace(str(input_path), relative_input)
        state_path.write_text(text, encoding="utf-8")
    except Exception:
        pass

    summary = {
        "input": relative_input,
        "scalar_field_used": scalar_name,
        "vector_field_used": vector_name,
        "streamlines_created": stream_created,
        "outputs": [
            "screenshots/01_scalar_slice.png",
            "screenshots/02_contour_or_threshold.png",
            "screenshots/03_streamlines.png" if stream_created else "streamlines skipped",
            "screenshots/04_combined_view.png",
            "paraview/flow_pipeline.pvsm",
        ],
    }
    (METADATA_DIR / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
