<!--
TEMPLATE: monorepo (packages table front-and-center).
Replace every {{PLACEHOLDER}}. Delete sections without real content.
-->
<!-- Use this as the English body after the Chinese body. Render the English title and tagline once above both language sections. -->
<a id="english"></a>

## English

![Build](https://img.shields.io/github/actions/workflow/status/{{OWNER}}/{{REPO}}/{{CI_FILE}})
![License](https://img.shields.io/github/license/{{OWNER}}/{{REPO}})

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
