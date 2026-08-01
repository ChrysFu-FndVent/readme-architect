# Input Controls

README quality depends on examining the right evidence. By default, the analyzer skips generated
artifacts, dependency folders, VCS metadata, and common build output. A project can further narrow
the evidence set with a repository-root `.readme-architectignore` file.

## `.readme-architectignore`

The file supports a practical gitignore-style subset. Later matches override earlier ones.

```text
# Comments are ignored.
# Exclude a sensitive directory and generated reports.
internal/
reports/generated/**

# Exclude by filename or extension.
.env.local
*.snapshot

# Re-include a specific path.
!docs/public-example.md
```

Supported patterns:

| Pattern | Effect |
|---|---|
| `file.ext` | Match that filename anywhere in the project. |
| `*.ext` | Match files by extension. |
| `directory/` | Exclude that directory and its contents. |
| `path/**` | Exclude all paths below a directory. |
| `**/path/` | Exclude matching directories at any depth. |
| `!pattern` | Re-include a later matching path. |
| `/path` | Match a path only from the project root. |

Use this for secrets, private examples, generated reports, or large unrelated fixtures. It narrows
what the analyzer uses as evidence; it does not delete, move, or modify any project file. Do not use
it to hide behavior that the README needs to document.

## Output Contract

The default bilingual output is one `README.md` with this stable order:

1. One English-only title and short tagline.
2. A Chinese/English anchor switch.
3. The complete Simplified Chinese body.
4. The complete English body.

Run `validate_readme.py --bilingual README.md` after assembly. It validates the anchor switch,
Chinese-first order, one shared H1 title, and the removal of legacy `README.zh-CN.md` links.
