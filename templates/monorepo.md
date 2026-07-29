<!--
TEMPLATE: monorepo (packages table front-and-center).
Replace every {{PLACEHOLDER}}. Delete sections without real content.
-->
<div align="right"><a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a></div>

# {{PROJECT_NAME}}

![Build](https://img.shields.io/github/actions/workflow/status/{{OWNER}}/{{REPO}}/{{CI_FILE}})
![License](https://img.shields.io/github/license/{{OWNER}}/{{REPO}})

{{TAGLINE_UNDER_120_CHARS}}

## Table of Contents

- [About](#about)
- [Packages](#packages)
- [Getting Started](#getting-started)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## About

{{WHAT_AND_WHY}}

## Packages

| Package | Version | Description |
|---------|---------|-------------|
| [`{{PKG_NAME}}`]({{PKG_PATH}}) | ![v](https://img.shields.io/npm/v/{{PKG_NAME}}) | {{PKG_DESC}} |

## Getting Started

```bash
git clone https://github.com/{{OWNER}}/{{REPO}}.git
cd {{REPO}}
{{INSTALL_COMMAND}}
{{BUILD_COMMAND}}
```

## Development

```bash
{{DEV_COMMAND}}
{{TEST_COMMAND}}
```

## Contributing

PRs welcome — see {{CONTRIBUTING_LINK}}.

## License

{{SPDX}}. See [`LICENSE`](LICENSE).
