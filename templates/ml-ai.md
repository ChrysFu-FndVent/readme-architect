<!--
TEMPLATE: ml-ai / research (rigorous, results + citation).
Replace every {{PLACEHOLDER}}. Delete sections without real content.
-->
<!-- Use this as the English body after the Chinese body. Render the English title and tagline once above both language sections. -->
<a id="english"></a>

## English

![arXiv](https://img.shields.io/badge/arXiv-{{ARXIV_ID}}-b31b1b)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![License](https://img.shields.io/github/license/{{OWNER}}/{{REPO}})

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Results](#results)
- [Installation](#installation)
- [Usage](#usage)
- [Citation](#citation)
- [License](#license)

## Overview

{{WHAT_THE_METHOD_DOES}}

## Architecture

![Pipeline](assets/readme/architecture.png)

{{MODEL_OR_PIPELINE_EXPLANATION}}

## Results

| Model | Dataset | Metric | Score |
|-------|---------|--------|-------|
| {{MODEL}} | {{DATASET}} | {{METRIC}} | {{SCORE}} |

## Installation

```bash
conda create -n {{ENV}} python=3.10
conda activate {{ENV}}
pip install -r requirements.txt
```

## Usage

```bash
# Training
python train.py --config configs/{{CONFIG}}.yaml

# Inference
python inference.py --checkpoint {{CKPT}}
```

<details>
<summary>Full hyperparameters</summary>

{{HYPERPARAMETER_TABLE}}

</details>

## Citation

```bibtex
@article{{{BIBKEY}},
  title   = {{{TITLE}}},
  author  = {{{AUTHORS}}},
  journal = {{{VENUE}}},
  year    = {{{YEAR}}}
}
```

## License

{{SPDX}}. See [`LICENSE`](LICENSE).
