# AI Evaluation Notes

I wrote this section as a validation rubric for reviewing AI-generated ParaView or scientific visualization answers. This is relevant to AI-training work because the reviewer needs to identify whether a model's workflow is technically correct, reproducible, and clear.

## What a correct answer should understand

A technically correct answer should distinguish between:

- **Scalar fields** such as speed, pressure, temperature, density, or `Cp`
- **Vector fields** such as velocity or displacement
- **Slice filters**, which show planar cross-sections
- **Contour filters**, which extract iso-values from scalar fields
- **Threshold filters**, which isolate cells or points within scalar ranges
- **Stream Tracer**, which requires a vector field
- **Tube filter**, which turns line-based streamlines into visible cylindrical geometry
- **Color maps**, which should be rescaled to the active data range
- **State files**, which preserve the ParaView pipeline but are not images or videos

## Common mistakes I would check for

1. **Confusing contour and threshold**  
   A contour extracts iso-values. A threshold selects a range of values.

2. **Trying to create streamlines from a scalar field**  
   Streamlines require a vector field. A scalar field like temperature or speed alone is not enough.

3. **Calling `.pvsm` the final video**  
   A `.pvsm` file is the saved ParaView state. The screenshots and MP4 are exported outputs.

4. **Skipping reproducibility**  
   A strong answer should mention the input data, exact filters, output files, and rerun commands.

5. **Ignoring point data vs. cell data**  
   Many ParaView operations depend on whether an array is associated with points or cells.

6. **Not rescaling color maps**  
   Color ranges can be misleading if they are not rescaled after filtering.

7. **Suggesting only GUI steps when automation is requested**  
   For this project, the intended approach is command-line automation with `pvpython`.

## Evaluation rubric

| Criterion | Strong answer | Weak answer |
|---|---|---|
| ParaView knowledge | Names correct filters and uses them appropriately | Uses generic visualization language only |
| Scientific correctness | Distinguishes scalar and vector data | Treats all variables the same |
| Reproducibility | Provides commands and output paths | Gives vague manual instructions |
| Automation | Uses `pvpython`, `SaveScreenshot`, and `SaveState` | Requires only manual GUI screenshots |
| Validation | Mentions expected outputs and failure modes | Gives no quality checks |
