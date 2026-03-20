# BARseq Acquisition Metadata

Generates `acquisition.json` files for BARseq subjects 780345 and 780346.

## Approach

This uses a **black-box approach**: each acquisition is described by its inputs
(brain sections), approximate timeframe, and experimenters — without attempting
to capture the detailed multi-day, multi-slide imaging process.

This decision was made after Saskia reviewed the raw data structure with Doug
on 2026-02-16 and concluded that fully capturing the acquisition details was not
feasible given the complexity of the multi-slide, multi-day workflow and the
effort required to coordinate with the BARseq team.

See [PR #1690](https://github.com/AllenNeuralDynamics/aind-data-schema/pull/1690)
for the previous detailed attempt, which includes extensive documentation of the
imaging parameters, channel configurations, and tile structure.

## Usage

```bash
uv run python examples/barseq_acquisition.py
```

Output goes to the current directory by default, or specify:

```bash
uv run python examples/barseq_acquisition.py --output-dir path/to/output
```

## Remaining Placeholders

- **`specimen_id`**: Pending from BARseq procedures work. See
  [PR #1763](https://github.com/AllenNeuralDynamics/aind-data-schema/pull/1763).
  Once available, update `SUBJECTS[subject_id]["specimen_id"]` in `barseq_acquisition.py`.

## Data Sources

| Field | Source |
|---|---|
| Timestamps | Folder names at `smb://allen/aind/stage/barseq/` + `experiment_detail.txt` files |
| Experimenters | `experiment_detail.txt` files in raw data slide folders |
| Protocol | `MAPseq-BARseq methods_forSciComp.pdf` |
| Instrument | BARseq instrument PR #1685 |
