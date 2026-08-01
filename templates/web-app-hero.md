<!--
TEMPLATE: web-app / framework (centered project opening, rich).
Replace every {{PLACEHOLDER}}. Delete sections without real content.
Uses: banner, badges, emoji headings, feature grid, dividers, TOC, callouts, dynamic cards.
-->
<a id="readme-top"></a>
<div align="right"><a href="#简体中文">简体中文</a> | <a href="#english">English</a></div>

<!-- Render this project opening once in English. Put the Chinese body before the English body below it. -->

<div align="center">
  <img src="assets/readme/banner.png" alt="{{PROJECT_NAME}} banner" width="100%" />

  <h1>{{PROJECT_NAME}}</h1>
  <p><em>{{TAGLINE_UNDER_120_CHARS}}</em></p>

  <p>
    <a href="https://img.shields.io/github/actions/workflow/status/{{OWNER}}/{{REPO}}/{{CI_FILE}}"><img src="https://img.shields.io/github/actions/workflow/status/{{OWNER}}/{{REPO}}/{{CI_FILE}}?style=for-the-badge" alt="Build" /></a>
    <img src="https://img.shields.io/github/license/{{OWNER}}/{{REPO}}?style=for-the-badge" alt="License" />
    <img src="https://img.shields.io/github/stars/{{OWNER}}/{{REPO}}?style=for-the-badge" alt="Stars" />
  </p>

  <p>
    <a href="{{DOCS_URL}}"><strong>Explore the docs »</strong></a>
    &middot; <a href="{{DEMO_URL}}">Live Demo</a>
    &middot; <a href="https://github.com/{{OWNER}}/{{REPO}}/issues">Report Bug</a>
  </p>
</div>

<details>
<summary>📑 Table of Contents</summary>

- [About](#-about)
- [Features](#-features)
- [Architecture](#️-architecture)
- [Built With](#-built-with)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Configuration](#️-configuration)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

</details>

---

## ✨ About

{{WHAT_AND_WHY_1_TO_3_PARAGRAPHS}}

> [!NOTE]
> {{OPTIONAL_KEY_CONTEXT_OR_STATUS}}

## 🎯 Features

<table>
  <tr>
    <td width="33%"><b>{{EMOJI}} {{FEATURE_1}}</b><br/>{{BENEFIT_1}}</td>
    <td width="33%"><b>{{EMOJI}} {{FEATURE_2}}</b><br/>{{BENEFIT_2}}</td>
    <td width="33%"><b>{{EMOJI}} {{FEATURE_3}}</b><br/>{{BENEFIT_3}}</td>
  </tr>
</table>

## 🏗️ Architecture

![Architecture diagram](assets/readme/architecture.png)

{{SHORT_EXPLANATION_OF_COMPONENTS_AND_DATA_FLOW}}

## 🧰 Built With

{{BADGE_GRID_OF_REAL_FRAMEWORKS}}

## 🚀 Getting Started

### Prerequisites

```bash
{{PREREQUISITE_INSTALL_COMMANDS}}
```

### Installation

```bash
git clone https://github.com/{{OWNER}}/{{REPO}}.git
cd {{REPO}}
{{INSTALL_COMMAND}}
```

## 💡 Usage

```{{PRIMARY_LANG}}
{{MINIMAL_RUNNABLE_EXAMPLE}}
```

<details>
<summary>More examples</summary>

```{{PRIMARY_LANG}}
{{ADVANCED_EXAMPLE}}
```

</details>

## ⚙️ Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `{{ENV_VAR}}` | {{YES_NO}} | `{{DEFAULT}}` | {{DESCRIPTION}} |

## 🗺️ Roadmap

- [x] {{DONE_ITEM}}
- [ ] {{PLANNED_ITEM}}

## 🤝 Contributing

Contributions are welcome! Please read {{CONTRIBUTING_LINK}} and open a PR.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes
4. Push and open a Pull Request

![Contributors](https://contrib.rocks/image?repo={{OWNER}}/{{REPO}})

## 📄 License

Distributed under the {{SPDX}} License. See [`LICENSE`](LICENSE) for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
