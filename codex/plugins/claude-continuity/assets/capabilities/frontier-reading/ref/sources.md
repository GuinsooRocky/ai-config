# 来源清单

**核实日期：2026-09-21**，每条 URL 当时都真实访问过。结构性事实（谁有 RSS、谁停更）会变，隔几个月重核一次。

## 一层：真做危险能力评估的四家

只有这四家在发带红队、危险能力评测、缓解措施的 system card。别家发的叫技术报告。

| 厂商 | 入口 | 能订吗 |
|---|---|---|
| OpenAI | `https://deploymentsafety.openai.com/` | 无 RSS、无邮件，只能手动刷 |
| Anthropic | `https://www.anthropic.com/transparency/model-report`（表格每行挂 PDF） | 无 RSS（rss.xml / feed.xml 实测 404） |
| Google DeepMind | 模型卡 `https://deepmind.google/models/model-cards/`；**真数字在** `https://deepmind.google/frontier-safety/` | **有 RSS**：`https://deepmind.google/blog/rss.xml` |
| xAI | `https://x.ai/safety`（索引页 403，盯 PDF 直链） | 无 |

Anthropic 四样东西别混：模型卡 PDF 在 `transparency/model-report`；总入口 `anthropic.com/transparency`；扩展安全政策 `anthropic.com/rsp`；对齐研究博客是**独立域名** `alignment.anthropic.com`。

Google 的坑：模型卡页很多只有定性描述，带评测数字的是 `frontier-safety/` 下的 FSF 报告 PDF。

## 二层：能力报告（无安全章节）

### 中国厂商

核过的九家里**没有一家提供 RSS**，也没有一家旗舰模型报告带安全/对齐评测章节。唯一例外是 Qwen 发过护栏模型报告（Qwen3Guard），不是旗舰卡。跟踪只能靠 HF follow org + GitHub watch org。

| 厂商 | 首发位 | 入口 |
|---|---|---|
| DeepSeek | 官网 news + HF 同步，报告 PDF 挂 HF 仓 | `https://www.deepseek.com/news/`、`https://www.deepseek.com/transparency/` |
| 阿里 Qwen | 官网 blog + HF 模型卡，深度报告走 arXiv | `https://qwen.ai/blog`（JS 壳）；旧站 `qwenlm.github.io/blog/` 已停更 |
| Moonshot / Kimi | **GitHub repo 首发**，技术报告 PDF 直接进仓 | `https://github.com/MoonshotAI` |
| 字节 Seed | 官网 blog + 独立论文库 | `https://seed.bytedance.com/en/public_papers` |
| 智谱 GLM | z.ai 单篇 blog（**索引页 404**） | 版本表走 `https://docs.z.ai/release-notes/new-released` |
| MiniMax | blog 先行，约十天后补 arXiv 报告 | `https://www.minimax.io/blog`（不是 /news） |
| 腾讯混元 | 官方新闻稿 + GitHub/HF 同步 | `https://github.com/Tencent-Hunyuan` |
| 百度文心 | 官方 blog + arXiv | `https://ernie.baidu.com/blog` |
| 阶跃 StepFun | 单篇静态页（**无索引页**） | HF `stepfun-ai` |

### 西方开源

| 厂商 | 入口 | 备注 |
|---|---|---|
| Ai2 (OLMo) | `https://huggingface.co/allenai` | 全开放评测表，质量扎实 |
| NVIDIA (Nemotron) | `https://huggingface.co/nvidia` | 能力数字硬；`build.nvidia.com` 是 JS 壳 |
| Meta (Llama) | `https://github.com/meta-llama/llama-models` | **已停更**，MODEL_CARD 最后提交 2025-04 |
| Mistral | `https://legal.mistral.ai/ai-governance/models/` | 只有发布日期，**一个评测数字都没有** |
| Microsoft MAI | `https://microsoft.ai/blog/` | 技术报告有真数字；年度 Responsible AI 报告是公关文体 |
| Amazon Nova | `https://aws.amazon.com/ai/responsible-ai/resources/` | Service Card 是产品文档腔 |
| Cohere / AI21 / Reka | — | 模型卡停更或不存在，不用跟 |

## 三层：非厂商来源（独立性最高）

| 来源 | 干什么 | 能订吗 |
|---|---|---|
| CAISI（美国 NIST 下属） `https://www.nist.gov/caisi` | 唯一逐个评中国开源模型的官方来源 | **RSS + GovDelivery 邮件** |
| UK AI Security Institute `https://www.aisi.gov.uk/research` | 政府里产出最多、真自跑评测；也是 International AI Safety Report 秘书处 | 站内找不到订阅入口 |
| METR `https://metr.org/blog/` | 前沿模型自主能力预部署评测，独此一家 | 邮件 + Substack |
| Apollo Research `https://www.apolloresearch.ai/` | 欺骗 / scheming 评测；成果常只出现在厂商 system card 里 | 站内表单 |
| Epoch AI `https://epoch.ai/benchmarks` | 自跑基准 + 模型数据库，**CSV 可下载（CC-BY）** | Substack |
| Artificial Analysis `https://artificialanalysis.ai/` | 性能与价格全自跑实测 | 邮件 |
| FLI AI Safety Index `https://futureoflife.org/` | 各家公司安全评级 | newsletter |
| Arena `https://arena.ai/leaderboard` | 人类盲投 Elo（lmarena.ai 已 301 到此） | 未核到 RSS |
| Scale Labs `https://labs.scale.com/leaderboard` | 自跑评测，但 Meta 持股，独立性打折 | 未核到 |
| Transformer `https://www.transformernews.ai/` | 三人编辑部周报，专盯这类报告发布，**兜底防漏** | 免费 Substack |
| CAIS newsletter `https://newsletter.safe.ai/` | AI 安全双周报 | 免费邮件 |

## 两个结构性事实

1. **不存在一站式聚合站**。没有任何地方把各家 system card 原文集中归档。搜到的 awesome-list 全是「评测工具与基准」清单，个人维护、质量没核，不要当情报源。
2. **欧盟 AI Act 的坑**：法规强制厂商披露技术文档，但欧盟 AI Office **没有公开库**（Art.53(1)(d) 要求厂商发在自家官网），文档只能去各厂商官网自己收。中国 CAC 的备案公告只有名单，零安全评估内容。

## 真有 RSS 的只有三个

`deepmind.google/blog/rss.xml`、CAISI、arXiv（`https://rss.arxiv.org/rss/cs.CL`、`cs.AI`）。其余全靠 API 轮询或手动刷。

HF 轮询口径（实测可用）：
```
https://huggingface.co/api/models?author=<org>&sort=lastModified&direction=-1&limit=20
https://huggingface.co/api/daily_papers?limit=40
```
