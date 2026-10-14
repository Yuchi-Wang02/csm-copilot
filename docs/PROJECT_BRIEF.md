# A two-page introduction for an interview

[Download the project brief](../demo/project-brief.pdf).

The brief is a portable introduction to the working prototype. Page one explains the customer situation, the CSM workflow, and why Android and iOS require different next actions. Page two follows the recorded model failure through structured field checks and assisted correction. Seven clickable links lead to the live examples, practice experience, model recordings, and verification record.

Use it as a leave-behind or an offline introduction, then open the live case when someone wants to inspect the evidence. It does not replace the detailed source records or imply that the site is a live AI chat.

## Evidence and contribution boundaries

Counts and example states are read from the checked-in account data, workflow, MCP transcript, model recordings, review annotations, and evaluation results. The builder stops if the key editorial examples no longer match those records. The footer contains the first 12 hexadecimal characters of a SHA-256 digest of that source bundle, serialized as sorted-key JSON.

The brief distinguishes synthetic diagnostics, assisted model correction, and independent validation. It identifies substantial AI assistance and does not claim completed personal mastery, production use, or measured business impact.

## Rebuild and inspect

```sh
python -m pip install -e ".[brief]"
python scripts/build_project_brief.py
pdftoppm -scale-to 1400 -png demo/project-brief.pdf work/brief-page
```

Create the `work` directory before the optional rendering command. Poppler supplies `pdftoppm`; it is needed for visual inspection, not for generating the PDF.

The optional `brief` dependency group pins ReportLab and pypdf. It is not required to run the MCP server. The builder checks the two-page length, essential contribution and result boundaries, and seven public link annotations. PDF metadata uses a fixed creation timestamp and uncompressed page streams for reproducible output; the document's stated evidence date is the relevant snapshot date.

GitHub CI rebuilds the PDF on Windows and Ubuntu and compares it with the checked-in artifact. Initial visual review used rendered images of both pages. Layout inspection is still required after editorial changes: a passing text or page-count check cannot establish that a PDF is readable.
