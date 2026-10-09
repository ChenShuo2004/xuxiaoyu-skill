# 扩展知识库导航

入口知识核心用于即时会话，本目录按问题加载。无需每次读取全部资料。所有相对链接以本文件所在目录为起点。

|主题|资料页|适合的问题|
|---|---|---|
|T01 · 数据优势|[读取主题](topics/data.md)|数据、壁垒、飞轮、标注、日志|
|T02 · AI与工作流|[读取主题](topics/workflow.md)|Agent、智能体、模型、交付、自动化|
|T03 · 用户与采用|[读取主题](topics/product.md)|用户、需求、增长、复购、SaaS、PMF|
|T04 · 创始团队与领导力|[读取主题](topics/team.md)|团队、创始人、管理、合伙、招聘|
|T05 · 阶段与融资|[读取主题](topics/capital.md)|融资、投资、现金、估值、VC、拒投|
|T06 · 网络与协作|[读取主题](topics/network.md)|人脉、资源、信任、使命、引荐|
|T07 · 出海与本地化|[读取主题](topics/global.md)|出海、全球化、美国、硅谷、本地|
|T08 · 科研、兴趣与职业|[读取主题](topics/career.md)|职业、转行、科研、热爱、学习、人生|
|T09 · 医疗与深科技|[读取主题](topics/health.md)|医疗、临床、科研转化、基因、研发|
|T10 · 创作者与消费体验|[读取主题](topics/creator.md)|创作者、直播、粉丝、内容、娱乐、品牌|
|T11 · 数据系统与决策|[读取主题](topics/operations.md)|CRM、ERP、尽调、数据整理、检索|
|T12 · 风险、诚实与边界|[读取主题](topics/ethics.md)|伦理、隐私、风险、偏见、责任|

## 结构化资源

- [来源状态](sources.json)：25个入口，23个证据组，包含正文、元数据与旧摘要线索；不表示25篇完整采访。
- [命题账本](claims.jsonl)：短释义、归属、日期、定位与限制。
- [24张历史案例卡](case-library.md) / [结构化案例](case-library.json)：应用机制、实验、失效情况和待核验项。
- [72个原创对话场景](scenario-library.md) / [JSONL](scenarios.jsonl)：带命题锚点的应用推断，不是人物原话。
- [观点时间线与张力](timeline.md)：时间、条件和未知。
- [9条新研究缺口](research-gaps.json)：待补音频、登录资料和超时页面；不进入命题。
- [实际统计](corpus-stats.json)：命题与原创应用分开统计；JSON/Markdown不重复计算。

## 本地查找

`python3 <Skill目录>/scripts/find_evidence.py 融资 --kind all --limit 8`

默认只检索命题；`--kind`可选claims/cases/scenarios/topics/all，`--source S16`或`--topic capital`缩窄结果。中文按关键词匹配，不能代替语义搜索或核验。结果带类型、命题或来源ID；先核对证据再生成结论。
