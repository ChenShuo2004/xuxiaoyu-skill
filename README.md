# xuxiaoyu-skill · 徐霄羽

安装后，直接和徐霄羽（Sue Xu）公开观点提炼的思维角色聊天。适合讨论创业、AI产品、数据壁垒、团队、融资、全球化和职业选择。

这是独立仓库中的一个 Skill。核心资料随包提供，普通对话无需读取制作者电脑、登录原始网站、连接私有知识库、申请 API Key 或安装 MCP。运行它的 AI 宿主仍需你自己的正常账号与模型服务。它不是徐霄羽本人或 AMINO 官方产品。

## 最快安装：直接 clone

### Codex（macOS / Linux）

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git ~/.agents/skills/xuxiaoyu-skill
```

然后在 Codex 新对话中输入：

```text
$xuxiaoyu-skill 我想和你聊聊，我正在做一个AI内容工具。
```

后面正常聊天，继续提供情况即可。也可以说“用徐霄羽的公开观点视角，帮我看看这个选择”。未出现在技能列表时重新打开会话或重启宿主。使用方式与默认目录依据 [OpenAI 官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)。

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git ~/.claude/skills/xuxiaoyu-skill
```

新会话输入 `/xuxiaoyu-skill 我想聊聊我的创业想法`，或用自然语言提到徐霄羽。参考 [Claude Code 官方 Skills 文档](https://code.claude.com/docs/en/skills)。

### Cursor

```bash
mkdir -p ~/.cursor/skills
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git ~/.cursor/skills/xuxiaoyu-skill
```

在 Agent 中输入 `/` 并选择 `xuxiaoyu-skill`。想让该视角在整个会话保持，可用宿主的 Custom Mode。参考 [Cursor 官方 Skills 文档](https://cursor.com/docs/skills)。本地安装不会自动让远程或云端执行器取得你电脑上的资料，需要安装到实际执行环境。

### Windows PowerShell（Codex）

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
git clone https://github.com/ChenShuo2004/xuxiaoyu-skill.git "$HOME/.agents/skills/xuxiaoyu-skill"
```

已有同名目录时不要重复 clone 或手工覆盖。可在原 clone 目录运行 `git pull --ff-only`；若有自己修改先保存修改。

## 下载ZIP或安装到指定目录

从 GitHub 的 Code → Download ZIP 下载、解压，在解压目录运行：

```bash
python3 scripts/install.py --agent codex
# 其他宿主任选一个：
python3 scripts/install.py --agent claude
python3 scripts/install.py --agent cursor
# 指定的是“技能父目录”，脚本在其中创建 xuxiaoyu-skill：
python3 scripts/install.py --target ./project/.agents/skills
```

Windows 可用 `py -3` 替代 `python3`。安装脚本只需 Python 3.9+ 标准库，无需 pip；普通聊天不需要 Python。已有安装会拒绝覆盖，使用 `--update` 时先备份到技能父目录之外的 `skill-backups`，再安装完整资料。脚本不会修改宿主安全配置。

## 直接给 AI 的安装请求

将下面这段发给有本地文件能力的 Codex、Claude Code 或 Cursor：

```text
请安装这个独立 Skill：https://github.com/ChenShuo2004/xuxiaoyu-skill
将完整仓库安装到当前宿主的用户技能目录，保留 references 与 agents。
不要只复制 SKILL.md。安装后启用 xuxiaoyu-skill，和我自然对话。
如果已安装，保留我的修改并说明如何更新。
```

## 可以怎么聊

| 需求 | 可直接发送 |
| --- | --- |
| 日常项目交流 | 我正在做一个内容工具，但不知道先服务谁。 |
| 数据壁垒 | 我有很多日志，可是别人也能接同样的模型，优势在哪里？ |
| Agent产品 | 我该做聊天界面，还是替代一段实际工作？ |
| 团队与失败 | 我之前失败过，这次怎样证明自己学到了东西？ |
| 融资练习 | 先跟我讨论，再帮我整理一个融资叙事。 |
| 全球化 | 我有国内客户资源，进入美国市场该先验证什么？ |
| 职业探索 | 我不确定要不要转行，帮我从实际兴趣聊起。 |
| 观点核验 | 她真的说过这句话吗？给我来源和定位。 |
| 退出 | 退出徐霄羽模式，正常回答。 |

默认是对话，只有你要求时才输出完整报告或决策表。一个会话内沿用已提供的情况；不承诺跨会话自动记住你，也不会代表本人投资、引荐或背书。

## 本版实际资料

- 17个来源条目，63条有来源编号、日期、定位、说话人归属和限制的短释义。
- 新增原视频约65分钟自动字幕，以及约115和49分钟两集中文访谈的完整本地机器转写。中文转写只对所列选段进行提炼阅读；不是229分钟完整人工听校。
- 8个人物工作/职业模型，另有对话示例、报告模板、来源卡、关键词检索和评估场景。
- 原附件49个链接仅作为线索索引；45个微信入口不能算45篇已读正文。未绕过站点拦截、登录或付费限制。

来源和真实读取范围见 [来源卡](references/source-cards.md)。公开包分发原创整理与索引，保留引用入口，不分发完整原文、字幕、音频或私人附件。所有数据在下载包里即可使用；原网站链接只是核验入口。

## 遇到“没有权限”

日常对话的必要知识已放在 `SKILL.md` 内，不要求首次激活读取附加文件。高级资料相对 **Skill 文件所在目录**解析，不能相对当前项目工作目录。

1. 完整保留仓库文件；确认实际执行机器也安装了它。云端 Agent 无法自动读取本机安装。
2. 要核对详细资料时，在安装目录运行 `python3 scripts/check_package.py`，检查缺失或损坏。若宿主允许，只为该 Skill 目录提供正常读取权限，无需开放整台电脑。
3. 无文件工具的平台可打开 [单文件对话版](portable/徐霄羽-单文件对话版.md)，将内容作为对话说明或上传后要求按其对话。它是提示词兼容方式，不是自动注册的原生 Skill。

这个修订消除了原作者路径和远程账号依赖，并验证了换目录的完整安装；没有对未知的对方设备权限设置作远程修改。精确原文核验仍受目标宿主的文件与网络权限约束。

## 文件与维护

`SKILL.md` 是入口，`references/` 是随包知识，`agents/openai.yaml` 是显示元数据，`portable/` 是无文件工具兼容稿。`scripts/` 提供离线安装、检查与可选检索，不是每次聊天都运行的程序。

```bash
python3 scripts/check_package.py
python3 -m unittest discover -s tests -v
python3 scripts/find_evidence.py 数据 工作流
```

修改资料后运行 `python3 scripts/build_portable.py`，再运行 `python3 scripts/build_manifest.py` 更新兼容稿和校验清单。新增观点先核对真实说话人、日期和已读范围；转载不会增加独立证据数。人格行为场景见 [evaluations.md](references/evaluations.md)，测试通过不等于人物保真认证。

原创指令、整理和脚本使用 MIT 许可；外部来源内容权利归原作者。见 [LICENSE](LICENSE) 和 [NOTICE.md](NOTICE.md)。
