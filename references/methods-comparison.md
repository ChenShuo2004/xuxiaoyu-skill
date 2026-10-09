# 别人怎样蒸馏：四套公开方法对照

检查日期2026-10-08。以下基于项目原始说明与具体文件阅读，不是榜单，也不代表已运行或验证其营销效果。没有安装这些外部技能；它们仅作为研究资料。

## 实际查看的项目

| 项目 | 实际读到的做法 | 对本次的价值 | 使用时需注意 |
| --- | --- | --- | --- |
| [女娲 nuwa-skill](https://github.com/alchaincyf/nuwa-skill) | 研究人物认知与决策，检查观点是否复现、能否用于新问题、是否有区分度；保留观点张力 | 将稳定模型、情境规则与未知分开 | 不能为凑模型数量，把单次观点升级为跨域规律 |
| [soul.skill](https://github.com/larashero3-dotcom/soul.skill) | 将材料分块标记，聚合与筛选后分成人格、表达样本和领域知识 | 证据与运行指令分层，按问题读取 | 示例Wei Ran是虚构人物；仓库的样本量和效果说法不等于已验证标准 |
| [digital-twin-skill](https://github.com/FredHJC/digital-twin-skill) | 从对象本人材料提取行为，共有core与情境facet分开 | 避免把投资场合表达外推到私人生活 | 这里没有私聊语料；也未验证其隐私防护效果 |
| [AI-character-skill](https://github.com/yb2460/AI-character-skill) | 说明以作品、对话、决策、外部观察和时间线组织人物结构 | 在人物之外保留时间与来源归属 | 仓库README称七层但列Layer 0至7，共八项；以内容为准，不机械照抄层数 |

## 读过的具体文件

- [女娲提炼框架](https://github.com/alchaincyf/nuwa-skill/blob/main/references/extraction-framework.md)：用于核对模型的准入逻辑。
- [女娲芒格实例](https://github.com/alchaincyf/nuwa-skill/blob/main/examples/munger-perspective/SKILL.md)：观察完整产物如何组织规则、模型、反模式和执行流程。
- [女娲评分卡](https://github.com/alchaincyf/nuwa-skill/blob/main/references/fidelity-scorecard.md)：区分已知立场、超范围问题与独立验证。其分数与等级是该项目的评价方案，不直接代表本Skill质量。
- [soul.skill蒸馏指南](https://github.com/larashero3-dotcom/soul.skill/blob/main/docs/distillation-guide.md)：了解材料到结构化文件的三轮处理。
- [soul.skill虚构人物样本](https://github.com/larashero3-dotcom/soul.skill/blob/main/examples/wei-ran/_persona/rules.md)：观察人格与情境结构，未将样本内容作为真实人物证据。
- [digital-twin主Skill](https://github.com/FredHJC/digital-twin-skill/blob/main/SKILL.md)：读到行为提取、core/facet合成与更新流程。
- AI-character-skill此轮读取README，未声称逐个运行其人物角色。

## 本次实际采用的流程

人物确认→来源与说话人核对→抽取短命题→按主题和时间聚合→标记稳定/情境/未知→转成可运行规则→检查新问题与归因边界。

1. **先看证据形态**：原始问答、本人发文、机构页面、节目摘要和媒体旁白分别处理。关键词相似不等于同一人说过。
2. **再看重复与范围**：同一句话被转载十次仍是一份证据。不同年份、场景的支持才增强稳定性。
3. **规则写成机制**：来源说了什么、何时触发、怎么分析、什么观察会推翻、何时不适用。
4. **表达单独校准**：没有自然口语样本，就只记录可观察解释方式，不捏造语言统计。
5. **质量与完整性分开**：文件结构可校验；人格保真需要独立行为对照，此版没有给自身打A分。

## 可复用的蒸馏记录模板

每个候选特征记录：人物、命题、说话人、来源、日期、原文定位、语境、跨源支持、反例、类型（稳定模型/情境启发式/弱推断）、运行方式、适用边界。

每个新问题记录：用户事实→启用机制→条件结论→改变判断所需的证据→下一步。人物自己的观点和为用户设计的动作必须能分开辨认。

## 对本次质量的判断

材料足以制作具有来源的工作视角与有限职业建议。v3补充了两集完整机器转写、原视频字幕和失败案例；仍缺少完整人工听校、私人交互与投委会记录，不支持“完整复刻本人”或“近乎无法区分”。扩大文件长度不能弥补这些缺口。
