#!/usr/bin/env pvpython
"""Export a camera-orbit image sequence from a saved ParaView state, without GUI.

Run:

    pvpython scripts/export_orbit_frames.py --state paraview/flow_pipeline.pvsm --frames 120

Then convert frames to MP4:

    ffmpeg -framerate 24 -i animation/frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p animation/flow_orbit.mp4
"""
from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

from paraview.simple import *  # type: ignore

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRAME_DIR = PROJECT_ROOT / "animation" / "frames"
FRAME_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", default=str(PROJECT_ROOT / "paraview" / "flow_pipeline.pvsm"))
    parser.add_argument("--frames", type=int, default=120)
    parser.add_argument("--resolution", nargs=2, type=int, default=[1600, 1000])
    parser.add_argument("--radius", type=float, default=8.0)
    parser.add_argument("--height", type=float, default=4.0)
    args = parser.parse_args()

    state = Path(args.state).resolve()
    if not state.exists():
        raise FileNotFoundError(f"State file not found: {state}. Run build_paraview_pipeline.py first.")

    # Run from the project root so relative data paths in the .pvsm state resolve correctly.
    os.chdir(PROJECT_ROOT)

    ResetSession()
    LoadState(str(state))
    view = GetActiveViewOrCreate("RenderView")
    view.ViewSize = args.resolution
    view.Background = [1.0, 1.0, 1.0]

    # Basic camera orbit around origin. Adjust focal point for your dataset if needed.
    focal = [0.0, 0.0, 0.0]
    view.CameraFocalPoint = focal
    view.CameraViewUp = [0.0, 0.0, 1.0]

    for i in range(args.frames):
        theta = 2.0 * math.pi * i / args.frames
        view.CameraPosition = [args.radius * math.cos(theta), args.radius * math.sin(theta), args.height]
        Render(view)
        out = FRAME_DIR / f"frame_{i:04d}.png"
        SaveScreenshot(str(out), view, ImageResolution=args.resolution)
        print(f"Wrote {out}")

    print("Done. Convert frames with:")
    print("ffmpeg -framerate 24 -i animation/frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p animation/flow_orbit.mp4")


if __name__ == "__main__":
    main()
