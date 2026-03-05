# Paper Mentor Skill 快速开始指南

## 使用方法

### 基本用法

```
/paper-mentor https://arxiv.org/abs/1706.03762
```

或提供 arXiv ID：

```
/paper-mentor 1706.03762
```

### 完整流程

1. **输入论文 URL** - 提供 arXiv URL 或 ID
2. **选择难度级别** - 回复 `beginner`、`intermediate` 或 `advanced`
3. **领域探索** - 系统搜索并展示 10 篇相似论文
4. **交互问答** - 回答问题并获得反馈
5. **报告输出** - 可选输出完整学习报告

## 测试用例

### 用例 1: Attention Is All You Need

```
/paper-mentor https://arxiv.org/abs/1706.03762
```

### 用例 2: ResNet

```
/paper-mentor https://arxiv.org/abs/1512.03385
```

## 难度级别说明

| 级别 | 适合人群 | 问题特点 |
|------|----------|----------|
| beginner | 刚接触该领域 | 简单语言，提供提示，基础概念 |
| intermediate | 有一定基础 | 标准技术语言，平衡概念和应用 |
| advanced | 深入研究者 | 高级技术语言，分析评价和综合创新 |

## 输出示例

### 领域探索报告

```markdown
## 📚 领域探索报告

### 主论文
- **标题**: Attention Is All You Need
- **arXiv ID**: 1706.03762
- **作者**: Vaswani et al.

### 相似论文 (Top 10)
1. BERT: Pre-training of Deep Bidirectional Transformers
2. Language Models are Unsupervised Multitask Learners (GPT-2)
3. Vision Transformer
...

### 领域分析
- **研究方向**: 从 RNN/CNN 向基于注意力机制的模型转变
- **进展演变**: Transformer 已成为 NLP 和 CV 的标准架构
- **核心概念**: Self-Attention, Multi-head Attention, Position Encoding
- **核心价值**: 提出了完全基于注意力的序列建模方法
```

### 学习问题

```markdown
## 📝 学习问题

请选择一个问题回答，或直接输入答案:

1. [记忆] 什么是 Self-Attention 机制？
2. [理解] 解释位置编码的作用
3. [应用] 如何将 Transformer 应用到图像分类任务？
...
```

## 常见问题

**Q: 搜索不到足够的相似论文怎么办？**

A: 系统会自动扩大搜索范围，从 20 周扩展到 40 周或更多。

**Q: 可以更改难度级别吗？**

A: 可以，在交互过程中随时回复 `change difficulty to beginner/intermediate/advanced`。

**Q: 如何保存学习报告？**

A: 回复 `save report` 可以生成完整的 Markdown 格式报告。
