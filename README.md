# Gait analysis toolkit

Python tools for reading normalized gait exports, combining trials, reviewing individual cycles and producing right/left kinematic figures with a comparison reference. The repository also retains the supplied MATLAB extraction script for method traceability.

![P01 mean gait curves compared with the reference used in the local workflow](docs/gait_comparison.png)

Blue: right mean (4 cycles). Red: left mean (3 cycles). Grey: reference mean ± 1 SD. This figure was supplied from the local workflow using the real comparison reference. The reference data are not included in this repository; the executable public example uses a synthetic demonstration reference and therefore produces a different grey curve and band.

## Run the included example

```bash
git clone https://github.com/cimonetti/gait-analysis-toolkit.git
cd gait-analysis-toolkit
python -m pip install -r requirements.txt
python marcha.py
python -m streamlit run app.py
```

The command-line example uses `config.json` and writes PNG/SVG figures and numerical arrays to `outputs/`. For the interface, upload `examples/P01_001_QJT_E3D4.txt` and `examples/P01_001_PP_E3D4.txt`, using four right and three left cycles. These are real movement recordings with the participant name and local computer paths removed. Numerical values are unchanged. The included comparison reference is synthetic and has no normative meaning.

## Features

- Combine cycles from multiple trials without overwriting input files.
- Identify and remove a cycle consistently across the segments of one side.
- Display individual cycles or means; compare right and left means with a reference band.
- Configure axes and optional stance-end markers.
- Export PNG, SVG and cycle arrays.

## Input contract

Tab-separated TXT files with five header lines, 101 normalized rows and finite numerical values. Column 1 contains the sample index or cycle percentage; plotting uses the 101 rows as 0–100% of the cycle. QJT blocks contain hip right, hip left, knee right, knee left, foot right and foot left. PP blocks contain pelvis right, pelvis left, foot right and foot left. Each cycle has three consecutive component columns. Component order and signs are specific to the supplied MATLAB routine; consult `mapping.py` before using exports from another model or convention.

No filtering, interpolation, normalization or event detection is performed here. The source exports must already be normalized. Reference means and sample SD are calculated across cycles, with equal weight per cycle, combining sides. They are descriptive cycle statistics; repeated trials are not independent participants. With one cycle, the current display uses a zero-width SD band. The optional legacy pelvic SD mode uses only left cycles while retaining the bilateral mean.

## MATLAB

`matlab/processaMarchaControle.m` is the original workspace-dependent extraction script created by Prof. Felipe Arruda Moura. `matlab/importfile.m` retains the original MATLAB-generated import structure, including its fixed 181-column setting; identifying local paths and variable labels were replaced with generic examples. `matlab/demo.m` supplies filenames and cycle counts for the P01 example. MATLAB execution has not been verified; Python checks do not establish MATLAB runtime compatibility.

## Credits and tests

The Python application was adapted from Prof. Felipe Arruda Moura's MATLAB script with AI assistance.

Run the tests from `gait-analysis-toolkit/`:

```bash
python -m unittest discover -s tests -v
```

The tests cover column mapping, cycle exclusion, means and sample standard deviations. During portfolio preparation, the command-line example generated figures and arrays, and the Streamlit interface passed an initialization check. File-upload and mouse interactions were not tested.

The evaluation example uses real recordings identified as P01, with names and local file paths removed. The executable example uses a synthetic comparison reference; the README figure shows the real reference from the local workflow. Original reference arrays are not distributed. P01 demonstrates the application and is not a normative control group. The demonstration reference has no normative or clinical meaning. For local data, adapt `config.json` and check that column, axis and sign conventions match your exports.
