<!--
TEMPLATE: library / package (classic left-aligned, dense, info-first).
Replace every {{PLACEHOLDER}}. Delete sections without real content.
-->
<!-- Use this as the English body after the Chinese body. Render the English title and tagline once above both language sections. -->
<a id="english"></a>

## English

![Build](https://img.shields.io/github/actions/workflow/status/{{OWNER}}/{{REPO}}/{{CI_FILE}})
![Version](https://img.shields.io/npm/v/{{PACKAGE}})
![Downloads](https://img.shields.io/npm/dm/{{PACKAGE}})
![License](https://img.shields.io/github/license/{{OWNER}}/{{REPO}})

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## About

{{WHAT_AND_WHY}}

## Install

```bash
{{INSTALL_COMMAND}}
```

## Usage

```{{PRIMARY_LANG}}
{{IMPORT_AND_CALL_EXAMPLE}}
```

## API

### `{{FUNCTION_SIGNATURE}}`

{{DESCRIPTION}}

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `{{PARAM}}` | `{{TYPE}}` | `{{DEFAULT}}` | {{DESC}} |

Returns: `{{RETURN_TYPE}}` — {{RETURN_DESC}}

<details>
<summary>Advanced usage</summary>

```{{PRIMARY_LANG}}
{{ADVANCED_EXAMPLE}}
```

</details>

## Examples

{{LINKS_OR_SNIPPETS}}

## Contributing

PRs accepted. See {{CONTRIBUTING_LINK}}. Open an issue at
[github.com/{{OWNER}}/{{REPO}}/issues](https://github.com/{{OWNER}}/{{REPO}}/issues).

## License

{{SPDX}} © {{MAINTAINER}}. See [`LICENSE`](LICENSE).
