<div align="center">

# xuxiaoyu-skill · 徐霄羽

**和徐霄羽公开观点提炼的思维角色，聊创业、AI产品和人生选择。**

安装 → 提出问题 → 继续对话

`v3.0.0` · `随包知识` · `Codex / Claude Code / Cursor` · `MIT`

[快速安装](#快速安装) · [可以聊什么](#可以聊什么) · [资料与来源](#资料与来源) · [常见问题](#常见问题)

</div>

你可以带着一个还没想清楚的想法来：产品怎么做、壁垒在哪里、团队如何成长，或者自己要不要换一条路。Skill 会结合已整理的公开观点，与你讨论关键问题，并随着你补充的信息调整判断。

默认是自然对话；需要时再生成项目分析、验证实验或融资练习稿。它是公开材料的模拟视角，并非徐霄羽本人，也不代表 AMINO 的实际意见。

## 先看一段对话

> **你：** 我想做一个什么内容都能生成的AI平台。
>
> **Skill：** 我先看它替谁完成哪一段工作。你现在最熟悉的是哪类创作者，他们每周最痛苦的一项重复任务是什么？如果只是比别人多接几个模型，优势很难积累。
>
> **你：** 我熟悉电商短视频，每周反复改素材，但我没有数据。
>
> **Skill：** 那就先从一个真实交付拿反馈。跟一位客户完成选素材、出片、修改的全过程，记录哪些修改影响最终采用。先检验他是否愿意下周再用，再谈数据规模。

*这是为展示使用方式编写的模拟示例，不是本人原话或目标宿主实测记录。更多示例见 [对话示例](references/dialogue.md)。*

## 快速安装

需要一个支持本地 Skills 的 AI 宿主和正常可用的模型账号。**这个 Skill 不要求额外 API Key、MCP、私有知识库或原作者电脑权限。**

### Codex

macOS / Linux 运行：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git ~/.agents/skills/xuxiaoyu-skill
```

打开新对话，输入：

```text
$xuxiaoyu-skill 我想和你聊聊，我正在做一个AI内容工具。
```

后面直接接着聊，无需每轮重复命令。Skill 未出现在列表时，重新打开会话或重启宿主。[Codex 官方安装目录与调用说明](https://learn.chatgpt.com/docs/build-skills)

<details>
<summary><strong>Claude Code：安装与开聊</strong></summary>

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git ~/.claude/skills/xuxiaoyu-skill
```

打开新会话：

```text
/xuxiaoyu-skill 我想聊聊我的创业想法。
```

也可以在自然语言中说“用徐霄羽的公开观点视角和我讨论”。[Claude Code 官方说明](https://code.claude.com/docs/en/skills)

</details>

<details>
<summary><strong>Cursor：安装与开聊</strong></summary>

```bash
mkdir -p ~/.cursor/skills
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git ~/.cursor/skills/xuxiaoyu-skill
```

在 Agent 中输入 `/`，选择 `xuxiaoyu-skill`。需要让该视角在整个会话保持时，可使用宿主的 Custom Mode。[Cursor 官方说明](https://cursor.com/docs/skills)

本地目录不会自动复制到远程执行环境。使用云端 Agent 时，需把 Skill 安装或同步到实际运行的环境。

</details>

<details>
<summary><strong>Windows / ZIP / 指定项目目录</strong></summary>

**Windows PowerShell · Codex：**

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git "$HOME/.agents/skills/xuxiaoyu-skill"
```

**ZIP 安装：** 点击仓库的 **Code → Download ZIP**，解压，在解压目录运行：

```bash
python3 scripts/install.py --agent codex
# 换用其他宿主：--agent claude 或 --agent cursor
```

Windows 可用 `py -3` 替代 `python3`。安装脚本需 Python 3.9+，无第三方依赖；日常聊天不需要运行 Python。

**安装到某个项目：** `--target` 指定技能父目录，脚本会在其中创建 `xuxiaoyu-skill`。

```bash
python3 scripts/install.py --target ./project/.agents/skills
```

完整保留 `SKILL.md`、`references/` 和 `agents/`。只复制入口文件可使用基础视角，但无法核对完整随包出处。

</details>

### 不想自己操作：把这段发给 AI

```text
请安装这个独立 Skill：https://github.com/ChenShuo2004/xuxiaoyu-skill
将完整仓库安装到当前宿主的用户技能目录，保留 references 与 agents。
如果已安装，保留我的修改并说明如何更新。
安装后启用 xuxiaoyu-skill，和我自然对话。我想先聊聊正在做的项目。
```

这段适用于能操作本地文件的 AI 宿主。没有文件工具时，用下方的单文件对话版。

## 可以聊什么

| 你正在纠结 | 可以这样开始 | 对话会关注 |
| --- | --- | --- |
| 产品方向 | “我有一个AI工具，应该先服务谁？” | 具体群体、真实需求与采用 |
| 数据壁垒 | “别人也能接同样的模型，优势在哪里？” | 数据入口、领域知识与结果反馈 |
| Agent工作流 | “我应该做聊天界面，还是替代一段工作？” | 行动能力、流程交付与价值 |
| 团队与失败 | “我失败过两次，这次如何证明有变化？” | 学习、责任、管理与能力证据 |
| 融资练习 | “先和我讨论，再整理一份融资叙事。” | 阶段、实际演示与下一里程碑 |
| 全球化 | “我有国内资源，进入美国先验证什么？” | 独特资源、销售成本、品牌与社群 |
| 职业选择 | “我不确定要不要转行。” | 实际兴趣、小实验与现实代价 |
| 原观点核验 | “她真的说过这句话吗？” | 来源、时间、说话人与读取范围 |

需要更深入时，可以说“挑战一下我的想法”“比较这两个方向”“帮我设计一个最小验证实验”。想退出时说：**“退出徐霄羽模式，正常回答。”**

同一会话内沿用你已提供的情况；跨会话记忆取决于宿主，不由 Skill 单独提供。它不能替本人背书、承诺投资或提供真实引荐。

## 资料与来源

这份蒸馏覆盖数据优势、工作流、用户采用、团队成长、融资阶段、资源网络、全球化和职业选择 **8 个模型**。模型名称与验证动作由整理者设计，原观点与工程化推断分开标记。

| 随包内容 | 实际范围 | 查看 |
| --- | --- | --- |
| 来源索引 | 17个来源条目，包含问答、机构资料、摘要与补充线索 | [来源卡](references/source-cards.md) |
| 提炼命题 | 63条短释义，附来源、日期、定位、归属与限制 | [命题账本](references/claims.jsonl) |
| 长访谈补充 | 约65分钟原视频自动字幕；约115与49分钟中文访谈完整本地机器转写 | [读取状态](references/sources.json) |
| 思维与迁移 | 8个模型、反证、适用情境和观点张力 | [人物模型](references/persona.md) |
| 使用与报告 | 对话示例、案例迁移、决策模板 | [项目模板](references/decision-template.md) |
| 蒸馏方法 | 对照4个公开人物蒸馏项目 | [方法对照](references/methods-comparison.md) |

**研究截止：2026-10-09。** 中文机器转写仅对所列选段进行提炼阅读；不是约229分钟完整人工听校。原附件49个链接仅为线索索引，其中45个微信入口没有被算作45篇已读正文。被拦截、登录或付费限制的资料仍保留缺口。

公开包提供原创整理、模型和来源入口，不分发完整原始采访、字幕、音频或私人附件。具体估值、业绩、临床效果及当期法律需要独立核验。

## 常见问题

<details>
<summary><strong>安装后读取资料提示“没有权限”怎么办？</strong></summary>

日常对话需要的知识已经放在 `SKILL.md` 内。附加资料不可读时，Skill 会使用这个知识核心继续对话，并对精确出处核验说明限制。

详细资料路径相对 **Skill 所在目录**解析，不依赖制作者的电脑或当前项目目录。先确认整包安装在实际执行机器上，再运行：

```bash
python3 scripts/check_package.py
```

若宿主确实限制文件读取，只需给该 Skill 目录正常读取权限；不要为此开放整台电脑或关闭安全保护。这个版本已验证换目录安装，不表示远程修改了任何使用者设备的权限。

</details>

<details>
<summary><strong>没有本地文件工具，也能对话吗？</strong></summary>

可以使用 [徐霄羽 · 单文件对话版](portable/徐霄羽-单文件对话版.md)。把内容作为对话说明或上传后要求按其对话，其中已经内嵌人物模型、示例和来源。

这是提示词兼容方式，不会自动注册成平台原生 Skill。普通对话无需访问来源网站；需要最新事实时再联网核验。

</details>

<details>
<summary><strong>怎样更新？会覆盖自己的修改吗？</strong></summary>

直接 clone 的安装，在安装目录更新：

```bash
git pull --ff-only
```

如果有本地修改，先保存并处理冲突，不要强制覆盖。

使用 ZIP 或安装脚本时，在新包目录运行：

```bash
python3 scripts/install.py --agent codex --update
```

脚本先备份已有目录到技能父目录之外的 `skill-backups`，再安装完整资料。换用 Claude Code / Cursor 时调整 `--agent`。

</details>

## 文件与维护

```text
xuxiaoyu-skill/
├── SKILL.md                 对话入口与随包知识核心
├── agents/openai.yaml       显示名称、示例调用与发现策略
├── references/              人物模型、命题、来源、案例与模板
├── portable/                无文件工具的单文件对话版
├── scripts/                 可选安装、检索与完整性检查
└── tests/                   安装、备份与损坏检测
```

普通对话不要求运行脚本。维护者可以用以下命令检查包与检索证据：

```bash
python3 scripts/check_package.py
python3 -m unittest discover -s tests -v
python3 scripts/find_evidence.py 数据 工作流
```

修改资料后运行 `python3 scripts/build_portable.py` 和 `python3 scripts/build_manifest.py`。新增命题需核对真实说话人、日期和已读范围；转载不能增加独立证据数量。

已验证匿名 clone、换目录完整安装、更新备份、损坏检测和 ZIP 解压完整性。对话场景见 [评估说明](references/evaluations.md)；安装检查不等于人物保真认证，目标宿主中的对话效果仍应实际试用。

---

由 **陈硕** 整理。原创指令、短释义整理、模板与脚本使用 [MIT 许可](LICENSE)；外部来源权利归原作者。身份与来源说明见 [NOTICE.md](NOTICE.md)。
