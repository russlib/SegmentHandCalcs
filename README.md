# Segment Hand Calculations

`FSAESegmentHandCalcs.ipynb` is the Python/LaTeX segment notebook. `SegmentHandCalcs.mlx` preserves the original MATLAB live script. Both are retained intentionally; their stored outputs and differing assumptions are historical calculations, not evidence of physical qualification.

## Preserved histories

The repository was initialized with only the notebook, then the original MATLAB file was restored. Broader experiments remain in their accepted repository rather than being imported into this curated default.

| History | Recovery reference | Scope |
|---|---|---|
| Notebook snapshot | `branch-retired-20260929/backup-20260926/laptop-trjdifeu-42047905b74d/worktree` | Same cell sources as the current Python notebook; old output/serialization metadata |
| MATLAB overview snapshot | `branch-retired-20260929/backup-20260926/laptop-trjdifeu-e4ee69939c34/worktree` | Same MATLAB document and embedded assets; historical output state and `SegmentHandCalcsOverviewpdf.pdf` |
| Mixed experiments | `branch-retired-20260929/mmax-vmax-calc-40275` | Accepted in [MiscPythoning PR #4](https://github.com/russlib/MiscPythoning/pull/4); includes thermal/cell/busbar experiments, telemetry and notebook-editing scripts |
| Pressure-fit experiment | branch `backup-20260926/laptop-trjdifeu-61fc34bd7eae/worktree` | Unique `pressurePressFit.m`; units, material/reference provenance and intended placement remain unresolved |

Inspect a preserved history without merging it into the current calculations:

```sh
git fetch origin --tags
git show branch-retired-20260929/mmax-vmax-calc-40275:CoolingTestData/HCoeffFindingEnepaqCooling.ipynb
git show branch-retired-20260929/backup-20260926/laptop-trjdifeu-e4ee69939c34/worktree:SegmentHandCalcsOverviewpdf.pdf > historical-overview.pdf
```

Use the corresponding tag with `git switch --detach <tag>` to recover the complete tree. Cached plots, CSV rankings and recorded safety factors keep their original assumptions and provenance. Review those assumptions before using any result for design acceptance.
