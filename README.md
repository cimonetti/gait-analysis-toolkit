# Gait analysis toolkit

Python tools for reading normalized gait exports, combining trials, reviewing individual cycles and producing right/left kinematic figures with a comparison reference. Version 14 adds two-condition comparisons, GPS/GVS/MAP and optional GDI calculations, persistent cycle review and sidebar navigation. The repository also retains the supplied MATLAB extraction script for method traceability.

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

- Combine trials and check QJT/PP source filenames and right/left cycle counts.
- Compare two conditions, with combined and side-specific mean figures.
- Identify and remove a cycle consistently across all segments of one side; keep exclusions when switching sections.
- Automatically exclude incomplete evaluation cycles without interpolating missing values, retaining their identities in the export.
- Display individual cycles or means; compare right and left means with a reference band.
- Configure axes and optional toe-off markers from percentages or temporal measurements.
- Calculate GPS/GVS and MAP from the selected reference, and GDI when its separate calibration files are installed locally.
- Export PNG, SVG, index CSV, retained cycle arrays, trial provenance and the cycle-review history.

The interface requires Streamlit 1.65 or newer. On Windows, use `instalar.bat` followed by `abrir_interface.bat`.

## Input contract

Tab-separated TXT files with five header lines and 101 normalized rows. Incomplete evaluation cycles are excluded and reported; references must contain finite values. Column 1 contains the sample index or cycle percentage; plotting uses the 101 rows as 0–100% of the cycle. QJT blocks contain hip right, hip left, knee right, knee left, foot right and foot left. PP blocks contain pelvis right, pelvis left, foot right and foot left. Each cycle has three consecutive component columns. Component order and signs are specific to the supplied MATLAB routine; consult `mapping.py` before using exports from another model or convention.

No filtering, interpolation, normalization or event detection is performed here. The source exports must already be normalized. Reference means and sample SD are calculated across cycles, with equal weight per cycle, combining sides. They are descriptive cycle statistics; repeated trials are not independent participants. With one cycle, the current display uses a zero-width SD band. The optional legacy pelvic SD mode uses only left cycles while retaining the bilateral mean.

## Local references and indices

The public configuration retains the anonymized P01 example and synthetic demonstration reference. The laboratory's child/adult reference recordings, identifying headers, local paths and GDI calibration arrays from the uploaded local package are not distributed. The demonstration is not a normative database.

To use your own reference, create a local JSON file with a `controles` list (each item has `qjt`, `pp`, `ciclos_d`, `ciclos_e`) and register its path in `config.json` under `grupos_controle`. Set `grupo_controle_padrao` to the matching label. For command-line runs, also set the top-level `controles` list. Paths are relative to the configuration directory. Keep local recordings in the ignored `private_data/` directory.

GPS/GVS use the selected reference. Reference GPS is calculated leaving out one trial at a time, not one participant. The displayed 1.6° GPS comparison threshold is the value cited from Baker et al. (2012); its applicability must be checked for the population and comparison. Indices derived from the synthetic reference have demonstration value only.

GDI uses a separate, fixed calibration independent of the selected plotting reference. To enable it, place your authorized copies of `gillette.txt` (459 × 15 feature matrix) and `dados_con_GDI_orig.txt` (459 × number of reference cycles) in `dados_gdi/`. The directory is ignored by Git. Without these files, the application continues to generate gait figures and GPS/MAP and explains why GDI is unavailable.

The developer reports agreement with the previous laboratory GDI calculation for one participant; comparisons with additional participants are ongoing. This is an implementation cross-check, not a completed clinical validation.

## MATLAB

`matlab/processaMarchaControle.m` is the original workspace-dependent extraction script created by Prof. Felipe Arruda Moura. `matlab/importfile.m` retains the original MATLAB-generated import structure, including its fixed 181-column setting; identifying local paths and variable labels were replaced with generic examples. `matlab/demo.m` supplies filenames and cycle counts for the P01 example. MATLAB execution has not been verified; Python checks do not establish MATLAB runtime compatibility.

## Credits and tests

The Python application was adapted from Prof. Felipe Arruda Moura's MATLAB script with AI assistance.

Run the tests from `gait-analysis-toolkit/`:

```bash
python -m unittest discover -s tests -v
```

The tests cover column mapping, cycle exclusion, means and sample standard deviations. For the version 14 update, the existing three tests passed and the command-line example generated figures and arrays. The example reports axis-limit warnings for foot progression; adjust the Y limits when reviewing this example. File-upload and mouse interactions were not tested.

The evaluation example uses real recordings identified as P01, with names and local file paths removed. The executable example uses a synthetic comparison reference; the README figure shows the real reference from the local workflow. Original reference arrays are not distributed. P01 demonstrates the application and is not a normative control group. The demonstration reference has no normative or clinical meaning. For local data, adapt `config.json` and check that column, axis and sign conventions match your exports.

