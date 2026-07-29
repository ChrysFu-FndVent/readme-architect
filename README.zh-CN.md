<a id="readme-top"></a>
<div align="right"><a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a></div>

<div align="center">

<img src="assets/readme/banner.png" alt="README Architect 横幅" width="100%" />

<h1>README Architect</h1>

<p><em>把它对准一个代码库 —— 得到一份为该项目量身定制、风格契合的<strong>双语</strong> README。</em></p>

<p>
  <a href="https://github.com/ChrysFu-FndVent/readme-architect/stargazers"><img src="https://img.shields.io/github/stars/ChrysFu-FndVent/readme-architect?style=for-the-badge&color=38BDF8&labelColor=0B1221" alt="Stars" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/ChrysFu-FndVent/readme-architect?style=for-the-badge&color=4F46E5&labelColor=0B1221" alt="License" /></a>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0B1221" alt="Python" />
  <img src="https://img.shields.io/badge/Agent%20Skill-Qoder%20%26%20Claude-4F46E5?style=for-the-badge&labelColor=0B1221" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/Output-EN%20%2B%20ZH-38BDF8?style=for-the-badge&labelColor=0B1221" alt="双语输出" />
  <img src="https://img.shields.io/badge/Runs%20on-macOS%20%C2%B7%20Linux%20%C2%B7%20Windows-38BDF8?style=for-the-badge&labelColor=0B1221" alt="跨平台" />
</p>

<p>
  <a href="#about">简介</a> ·
  <a href="#features">特性</a> ·
  <a href="#how-it-works">工作原理</a> ·
  <a href="#getting-started">快速开始</a> ·
  <a href="#usage">使用方法</a>
</p>

</div>

> [!NOTE]
> **有意思的是：** 这份 README 正是由该技能自己生成的 —— 它把自己识别为一个开发者工具，赋予其
> *蓝图（blueprint）* 设计语言，并配上一张生成的主视觉横幅和一张真正的 **draw.io** 架构图。
> 这就是技能“自己吃自己的狗粮”。🐕

<table>
<tr><td>

**一眼概览**

</td><td>

| | |
|---|---|
| **类型** | Agent Skill（开发者工具） |
| **语言** | Python 3.8+ · 仅标准库 |
| **产物** | `README.md`（英）+ `README.zh-CN.md`（中） |
| **运行于** | macOS · Linux · Windows |
| **依赖** | 无强制依赖 —— 视觉技能均为可选 |

</td></tr>
</table>

<details>
<summary>📑 目录 · Table of Contents</summary>

- [✨ 简介](#about)
- [🎯 特性](#features)
- [⚙️ 工作原理](#how-it-works)
- [🏗️ 架构](#architecture)
- [🧩 项目类型（Archetype）](#archetypes)
- [🎨 个性化装饰工具箱](#personalization)
- [🖼️ 视觉联动](#visuals)
- [📂 项目结构](#structure)
- [🚀 快速开始](#getting-started)
- [💡 使用方法](#usage)
- [📋 环境要求](#requirements)
- [🗺️ 路线图](#roadmap)
- [🤝 参与贡献](#contributing)
- [📄 许可证](#license)
- [🙏 致谢](#acknowledgments)

</details>

---

<a id="about"></a>

## ✨ 简介

**README Architect** 是一个面向 Qoder / Claude 的 [Agent Skill](https://docs.anthropic.com)，它读取项目
真实的代码与文件，写出一份**看起来是为该项目手工打磨**的 README —— 而不是通用的填空模板。

它**全自动**运行：分析 → 分类 → 推导设计语言 → 挑选章节 → 生成视觉 → 组装双语 README → 校验。
产物是一份英文 `README.md` 加一份中文 `README.zh-CN.md`，其排版、徽章、语气与插图都为**当前这个仓库**
量身选择。

> [!TIP]
> 核心在于**契合**。精简的库会得到信息密集、以内容为先的 README；Web 应用则得到带横幅和功能网格的居中
> 英雄区。两者都由代码中的真实证据驱动。

<a id="features"></a>

## 🎯 特性

- 🔍 **基于证据的分析** —— 纯标准库的 Python 分析器提取语言、包管理器、框架、入口、脚本、CI、许可证以及
  git remote。绝不臆造任何特性。
- 🧩 **项目类型识别** —— 将仓库归类为 `library`、`cli-tool`、`web-app`、`framework`、`ml-ai`、
  `monorepo` 或 `minimal`，并据此调整排版、章节与语气。
- 🎨 **按项目定制的设计语言** —— 从真实项目中推导调色板、性格与意象，让它们**同时**驱动排版风格**和**每一个
  配图生成提示词。
- 🌐 **默认双语** —— 平行的 `README.md`（英文）+ `README.zh-CN.md`（中文），每份顶部都有语言切换。
- 🖼️ **可选 AI 视觉** —— 架构/流程图与 AI 生成横幅，联动 `drawio`、`nano-banana-pro` →
  `nano-banana-flash` → `generate-gpt-image-2` 链路，每一级都具备优雅降级（最终降到原生 Mermaid 图）。
- 🖥️ **可移植，不绑定单机** —— 在*当前*机器上探测工具、凭据与技能安装路径（macOS / Linux / Windows）；
  换到别人的环境、用别的 API 密钥照样跑通。
- 🧰 **9 项装饰工具箱** —— 徽章、对齐 HTML 块、分割线、恰当的 emoji、可折叠 `<details>`、表格、
  动态数据卡片、`> [!NOTE]` 提示块以及锚点导航。
- ✅ **内置校验器** —— 检查锚点可解析、本地资源存在、无模板占位符残留。

<a id="how-it-works"></a>

## ⚙️ 工作原理

一条全自动流水线，把代码库变成一份成品、已校验的 README：

```mermaid
flowchart LR
    A[📂 分析<br/>代码与文件] --> B[🧩 分类<br/>项目类型]
    B --> C[🎨 推导<br/>设计语言]
    C --> D[🧱 选择<br/>章节]
    D --> E[🖼️ 生成<br/>视觉]
    E --> F[📝 组装<br/>中英双语]
    F --> G[✅ 校验]
    classDef step fill:#0B1221,stroke:#38BDF8,stroke-width:1.2px,color:#E5E7EB;
    class A,B,C,D,E,F,G step;
```

项目类型决定**骨架**，项目自身的设计语言决定**皮肤**。正是这种分离，让每份 README 都显得量身定制，而非
套模板。

<p align="right"><a href="#readme-top">↑ 回到顶部</a></p>

<a id="architecture"></a>

## 🏗️ 架构

一个纯标准库编排器驱动整条流水线，读取内置的 references/templates，并**仅在探测到时**才调用伴生技能
（每个都有优雅降级），最终产出中英两份 README。

<div align="center">

<img src="assets/readme/architecture.png" alt="README Architect 架构：代码库 → SKILL.md 编排器（分析 / 集成探测 / 校验脚本 + 参考文件 + 设计语言）→ 带降级的伴生技能 → 中英双 README" width="100%" />

</div>

> [!TIP]
> 这张图本身就是技能在本机上用 **draw.io** 导出的。当未安装 draw.io 时，同样的逻辑会改用原生
> Mermaid 块渲染 —— 无需任何二进制依赖。

<p align="right"><a href="#readme-top">↑ 回到顶部</a></p>

<a id="archetypes"></a>

## 🧩 项目类型（Archetype）

| 类型 | 识别依据 | 排版 | 默认视觉 |
|------|----------|------|----------|
| `library` | 公开 API、已发布包、无应用入口 | 经典、密集 | 可选 logo |
| `cli-tool` | `bin` 字段、argparse/click/cobra/commander | 紧凑、左对齐 | 流程图 |
| `web-app` | React/Vue/Next/Django/Rails 应用、部署配置 | 居中英雄区 | 横幅 + 架构图 |
| `framework` | 大型开发工具、插件生态、强品牌 | 品牌英雄区 | 横幅 + logo + 图 |
| `ml-ai` | notebook、torch/tf/transformers、数据集、论文 | 研究导向 | 流水线图 |
| `monorepo` | pnpm/yarn/nx/turbo/cargo 工作区 | 包列表表格 | 模块关系图 |
| `minimal` | 极小的配置/纯文档仓库 | 精简、单栏 | 无 |

<a id="personalization"></a>

## 🎨 个性化装饰工具箱

技能会运用的九项装饰技术 —— **依项目语气调校**，绝不盲目堆砌（库精简，Web 应用/框架丰富）：

| # | 技术 | # | 技术 |
|---|------|---|------|
| 1 | 徽章装饰（静态与动态） | 6 | 对比 / 参数表格 |
| 2 | 居中标题与装饰分割线 | 7 | 动态数据卡片（星标、统计） |
| 3 | 灵活对齐与多栏排版 | 8 | `> [!NOTE]` 提示块与代码高亮 |
| 4 | 恰当的分区 emoji | 9 | 锚点导航目录 |
| 5 | 可折叠 `<details>` 详情块 | | |

<a id="visuals"></a>

## 🖼️ 视觉联动

视觉资产**仅在有帮助时**才生成，且每个提示词都从项目的设计语言推导而来 —— 绝非通用素材图。

| 资产 | 工具 | 何时生成 |
|------|------|----------|
| 架构 / 流程 / 时序图 | [`drawio`](https://www.drawio.com) → 原生 **Mermaid** 兜底 | 多组件系统、流水线 |
| 横幅 / logo / 插图 | [`nano-banana-pro`](https://github.com/ChrysFu-FndVent) → [`nano-banana-flash`](https://github.com/ChrysFu-FndVent) → [`generate-gpt-image-2`](https://github.com/ChrysFu-FndVent) | 品牌感强、且尚无横幅 |

> [!WARNING]
> 技能**绝不伪造产品截图或虚假指标。** 只有当仓库里已存在真实截图时才使用；图像生成仅限于横幅、logo 与
> 抽象插画。若生成器或其凭据不可用，README 会沿链路优雅降级（图表降到原生 Mermaid），并始终标注任何省略。

<a id="structure"></a>

## 📂 项目结构

<details>
<summary>展开查看结构</summary>

```text
readme-architect/
├── SKILL.md                    # 编排与 7 步工作流
├── references/
│   ├── section-library.md      # 章节、排序、取舍规则
│   ├── style-archetypes.md     # 项目类型 → 排版/语气/徽章/章节预设
│   ├── badges.md               # shields.io 徽章目录
│   ├── decoration-toolkit.md   # 9 项个性化技术
│   └── visual-assets.md        # drawio / nano-banana-pro / gpt-image-2 联动
├── templates/                  # 各项目类型的 README 骨架
├── scripts/
│   ├── analyze_project.py      # 仓库 → profile.json（纯标准库）
│   ├── check_integrations.py    # 探测 drawio / 图像技能 / 凭据（任意系统）
│   └── validate_readme.py      # 锚点 / 链接 / 占位符校验
└── assets/readme/              # 生成的横幅与架构图
```

</details>

值得一读的参考文件：[SKILL.md](SKILL.md) ·
[section-library](references/section-library.md) ·
[style-archetypes](references/style-archetypes.md) ·
[decoration-toolkit](references/decoration-toolkit.md) ·
[visual-assets](references/visual-assets.md)。

<a id="getting-started"></a>

## 🚀 快速开始

把 `readme-architect/` 文件夹复制到你的 agent 技能目录：

```bash
# Qoder
cp -r readme-architect ~/.qoder/skills/

# Claude
cp -r readme-architect ~/.claude/skills/
```

就这么简单 —— 下次 agent 加载技能时会自动发现它。

<a id="usage"></a>

## 💡 使用方法

打开任意项目，对你的 agent 说：

```text
为这个项目生成一份 README。
```

技能会接管后续工作。你也可以直接运行辅助脚本：

```bash
# 1. 把仓库分析成结构化 profile
python3 scripts/analyze_project.py --root . --out .readme-architect/profile.json

# 2. 校验一份完成的 README
python3 scripts/validate_readme.py README.md
```

> [!TIP]
> 如果已存在一份实质性的手写 `README.md`，技能会写入 `README.generated.md` 而不会静默覆盖你的成果 ——
> 除非你明确要求替换原文件。

<p align="right"><a href="#readme-top">↑ 回到顶部</a></p>

<a id="requirements"></a>

## 📋 环境要求

- **Python 3.8+** —— 分析器与校验器只用标准库（无需 `pip install`）。
- **可选：** `drawio`、`nano-banana-pro`、`nano-banana-flash` 或 `generate-gpt-image-2` 技能用于视觉。
  没有它们，README 依然能正常渲染（图表降级为 Mermaid）。
- **任意系统。** 探测逻辑可跨 macOS / Linux / Windows 移植；运行
  `python3 scripts/check_integrations.py` 即可查看本机可用能力。若你的技能装在其他位置，可用
  `README_ARCHITECT_SKILL_ROOTS` 扩展技能搜索路径。

<a id="roadmap"></a>

## 🗺️ 路线图

- [ ] 更多项目类型（移动应用、浏览器扩展、游戏项目）。
- [ ] 英文与中文之外的更多输出语言。
- [ ] 更丰富的分析信号（测试覆盖率、包体积、依赖图）。
- [ ] 各项目类型的示例 README 画廊。

<a id="contributing"></a>

## 🤝 参与贡献

欢迎贡献。可以开一个 issue 讨论改动，或直接发 pull request。在新增项目类型或装饰技术时，请保持
*证据优先于臆造* 的原则。

<a id="license"></a>

## 📄 许可证

基于 **MIT 许可证** 发布。详见 [`LICENSE`](LICENSE)。

<a id="acknowledgments"></a>

## 🙏 致谢

- [standard-readme](https://github.com/RichardLitt/standard-readme) —— 章节排序规范。
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) —— 居中英雄区灵感。
- [Shields.io](https://shields.io) —— 徽章。
- [Mermaid](https://mermaid.js.org) —— 可在 GitHub 原生渲染的图表。

<div align="center">

由 **README Architect** 技能构建 · 横幅由 `gpt-image-2` 生成 · 架构图由 `draw.io` 导出

<a href="https://star-history.com/#ChrysFu-FndVent/readme-architect&Date"><img src="https://api.star-history.com/svg?repos=ChrysFu-FndVent/readme-architect&type=Date" alt="Star History Chart" width="70%" /></a>

</div>
