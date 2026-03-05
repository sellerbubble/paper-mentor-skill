---
name: paper-mentor
description: Use when you want to deeply understand an academic paper - searches similar papers from HuggingFace, analyzes the research domain, generates learning questions, and provides interactive feedback
---

# Paper Mentor Skill

## 概述

此技能扮演科研论文指导者角色，帮助用户深入理解学术论文。

## 核心功能

1. **领域探索** - 从 HuggingFace Papers 搜索 10 篇相似论文
2. **知识提炼** - 提取研究方向、进展演变、核心概念
3. **交互学习** - 基于 Bloom 分类法生成问题，提供针对性反馈

## 输入格式

用户提供论文 URL 或 arXiv ID：
- arXiv URL: `https://arxiv.org/abs/1706.03762`
- arXiv ID: `1706.03762`

---

## 工作流程

```
用户输入论文 URL → 步骤 1: 获取论文内容 → 步骤 2: 提取关键词
                                                        ↓
步骤 6: 交互问答 ← 步骤 5: 生成问题 ← 步骤 4: 领域分析 ← 步骤 3: 搜索 HuggingFace
```

---

## 详细步骤

### 步骤 1: 获取论文内容

**目标**: 从 arXiv 获取论文标题和摘要

**方法**: 使用 arXiv API

**URL 格式**: `http://export.arxiv.org/api/query?id_list={arxiv_id}`

**示例请求**:
```
http://export.arxiv.org/api/query?id_list=1706.03762
```

**解析 XML 提取**:
- `<title>` - 论文标题
- `<summary>` - 论文摘要
- `<name>` - 作者姓名

**提示词模板**:
```
请从以下 arXiv API 响应中提取论文信息：

XML 内容：{xml_content}

请提取:
1. 论文标题 (title 标签内容)
2. 论文摘要 (summary 标签内容)
3. 作者列表 (name 标签内容)

返回格式 (JSON):
{
  "title": "...",
  "abstract": "...",
  "authors": ["...", "..."],
  "arxiv_id": "..."
}
```

---

### 步骤 2: 提取关键词

**目标**: 从论文标题和摘要提取 3-5 个核心技术关键词

**提示词模板**:
```
请从以下论文中提取 3-5 个核心技术关键词：

论文标题：{title}

论文摘要：{abstract}

提取要求:
1. 选择最能代表论文核心贡献的技术术语
2. 避免过于通用的词 (如 "model", "learning")
3. 优先选择具体的技术名称 (如 "Transformer", "Self-Attention")

返回格式 (JSON 列表):
["keyword1", "keyword2", "keyword3"]
```

**难度调节**:
- 如果关键词太专业，可以请用户确认是否需要调整

---

### 步骤 3: 搜索 HuggingFace Papers

**目标**: 从 HuggingFace Papers 获取相似论文列表

**方法**: 使用 WebFetch 工具访问 HuggingFace Papers 页面

**URL 格式**:
- 主页面：`https://huggingface.co/papers`
- 周次页面：`https://huggingface.co/papers?week={year}-W{week}`

**示例**:
```
https://huggingface.co/papers?week=2026-W09
https://huggingface.co/papers?week=2026-W08
```

**提示词模板 (WebFetch)**:
```
URL: https://huggingface.co/papers?week={week_id}
Prompt: 提取此页面所有论文的标题，每行一个标题。只返回标题，不要其他内容。
```

**周次计算**:
- 从当前日期向前推算 20 周
- 如果 20 周内不足 10 篇相关论文，继续扩展

**搜索策略 (优化版)**:

```
┌─────────────────────────────────────────────────────────────┐
│  性能优化策略                                                │
├─────────────────────────────────────────────────────────────┤
│  1. 分批获取：先获取最近 5 周，如果足够则停止                │
│  2. 关键词过滤：每获取一周就立即评分过滤                    │
│  3. 早停机制：如果已找到 10 篇高分论文，停止获取            │
│  4. 缓存机制：保存已获取的周次结果，避免重复请求            │
│  5. 并发限制：每次请求间隔 1-2 秒，避免过载                  │
└─────────────────────────────────────────────────────────────┘
```

**详细步骤**:
1. 获取最近 5 周的论文列表
2. 使用关键词进行评分，选择 Top 10
3. 如果不足 10 篇，继续获取下一个 5 周
4. 重复直到找到 10 篇或达到 20 周上限
5. 如果 20 周仍不足，扩展到 40 周

**评分标准**:
- 标题完全匹配关键词：+3 分
- 摘要包含关键词：+1 分
- 包含多个关键词：额外 +1 分

---

### 步骤 4: 领域分析

**目标**: 基于主论文和相似论文生成领域分析报告

**提示词模板**:
```
请基于以下论文生成领域分析报告：

主论文:
- 标题：{main_title}
- 摘要：{main_abstract}

相似论文列表:
{similar_papers_titles}

请分析以下内容:

1. **研究方向** (2-3 句)
   - 这个领域的研究者试图解决什么问题？
   - 核心挑战是什么？

2. **进展演变** (2-3 句)
   - 这个领域是如何发展的？
   - 有哪些关键的里程碑？

3. **核心概念** (3-5 个)
   - 列出该领域最重要的概念
   - 用逗号分隔

4. **核心价值** (1-2 句)
   - 主论文的核心贡献是什么？
   - 为什么这个贡献重要？

返回格式 (JSON):
{
  "research_direction": "...",
  "evolution": "...",
  "key_concepts": ["...", "..."],
  "core_value": "..."
}
```

---

### 步骤 5: 生成问题

**目标**: 基于 Bloom 分类法生成 8-12 个学习问题

**难度级别**:
- `beginner` - 入门级，简单语言和提示
- `intermediate` - 中级，标准技术语言
- `advanced` - 高级，深入分析和评价

**提示词模板**:
```
请基于以下论文生成 {num_questions} 个学习问题：

主论文: {main_title}
摘要：{main_abstract}

领域分析:
- 研究方向：{research_direction}
- 核心概念：{key_concepts}

用户认知水平：{difficulty} (beginner/intermediate/advanced)

请按照 Bloom 分类法生成问题:
- 2 个记忆 (Remember) 问题 - 回忆事实
- 2 个理解 (Understand) 问题 - 解释概念
- 2 个应用 (Apply) 问题 - 应用知识
- 2 个分析 (Analyze) 问题 - 分析比较
- 2 个评价 (Evaluate) 问题 - 评价判断
- 2 个综合 (Create) 问题 - 综合创新

难度要求 ({difficulty}):
{difficulty_instructions}

返回格式 (JSON 列表):
[
  {
    "level": "remember",
    "question": "...",
    "expected_answer": "..."
  },
  ...
]
```

**难度指令**:
- `beginner`: "使用简单语言，提供提示，避免技术术语"
- `intermediate`: "使用标准技术语言，平衡概念和应用"
- `advanced`: "使用高级技术语言，关注分析、评价和综合，询问权衡和局限性"

---

### 步骤 6: 交互问答

**目标**: 与用户进行交互式问答，提供针对性反馈

**交互流程**:
1. 展示问题列表
2. 用户选择问题并回答
3. 评估答案并提供反馈
4. 引导深入讨论

**评估提示词模板**:
```
请评估以下用户答案：

问题：{question}
问题级别：{level}
预期答案要点：{expected_answer}

用户答案：{user_answer}

评估维度:
1. **准确性** (0-100%) - 答案是否正确
2. **完整性** (0-100%) - 答案是否完整
3. **深度** (0-100%) - 理解是否深入
4. **清晰度** (0-100%) - 表达是否清晰

请提供:
1. 总体评价 (1 句)
2. 具体反馈 (2-3 句)
3. 补充知识 (如有必要)
4. 后续问题 (引导深入思考)

返回格式 (JSON):
{
  "accuracy": 85,
  "completeness": 70,
  "depth": 60,
  "clarity": 90,
  "overall": "...",
  "feedback": "...",
  "supplement": "...",
  "follow_up_question": "..."
}
```

---

## 输出格式

### 领域探索报告

```markdown
## 📚 领域探索报告

### 主论文
- **标题**: {title}
- **arXiv ID**: {arxiv_id}

### 相似论文 (Top 10)
1. {paper1_title}
2. {paper2_title}
...

### 领域分析
- **研究方向**: {research_direction}
- **进展演变**: {evolution}
- **核心概念**: {key_concepts}
- **核心价值**: {core_value}
```

### 学习问题

```markdown
## 📝 学习问题

请选择一个问题回答，或直接输入答案:

1. [记忆] 问题 1...
2. [理解] 问题 2...
3. [应用] 问题 3...
...
```

### 答案反馈

```markdown
## 💬 答案评估

**准确性**: ████████░░ 80%
**完整性**: ██████░░░░ 60%
**深度**: ███████░░░ 70%
**清晰度**: █████████░ 90%

**评价**: {overall}

**反馈**: {feedback}

**补充知识**: {supplement}

**思考题**: {follow_up_question}
```

---

## 错误处理

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| arXiv API 超时 | 重试 3 次，使用指数退避 |
| HuggingFace 无法访问 | 降级到 Semantic Scholar API |
| 不足 10 篇相似论文 | 扩大搜索范围到 40 周 |
| 关键词提取失败 | 使用简单频率分析作为后备 |

### 上下文管理

**问题**: 多篇论文标题和摘要可能超出 token 限制

**解决方案**:
1. **分批处理** - 将 10 篇论文分为 2-3 批处理
2. **摘要压缩** - 每篇论文摘要限制在 200 字以内
3. **智能摘要** - 使用 summarization skill 压缩领域分析报告
4. **增量处理** - 先处理主论文，再分批处理相似论文

**提示词模板 (上下文压缩)**:
```
请压缩以下领域分析报告，保留核心信息：

原始报告：{original_report}

压缩要求:
1. 保留研究方向、核心概念、核心价值
2. 删除冗余描述
3. 保持在 300 字以内
```

---

## 测试用例

### 用例 1: Attention Is All You Need

```
/paper-mentor https://arxiv.org/abs/1706.03762
```

**预期**:
- 关键词：Transformer, Self-Attention, Multi-head Attention
- 相似论文：BERT, GPT, Vision Transformer 等
- 问题涵盖：Self-Attention, Position Encoding, Multi-head Attention

### 用例 2: ResNet

```
/paper-mentor https://arxiv.org/abs/1512.03385
```

**预期**:
- 关键词：Residual Learning, Skip Connection, Deep Network
- 相似论文：VGG, Inception, DenseNet 等
- 问题涵盖：梯度消失、残差连接、bottleneck 设计

---

## 相关技能

- **huggingface-papers-research** - 批量论文收集
- **analyzing-research-papers** - 单篇论文深入分析
- **summarization** - 上下文压缩
