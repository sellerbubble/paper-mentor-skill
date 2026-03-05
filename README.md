# Paper Mentor Skill

一个用于深入理解学术论文的 Claude Code Skill。

## 功能

- 📚 **领域探索** - 从 HuggingFace Papers 搜索 10 篇相似论文
- 🧠 **知识提炼** - 提取研究方向、进展演变、核心概念
- 💬 **交互学习** - 基于 Bloom 分类法生成问题，提供针对性反馈

## 安装

### 方式一：使用 npx 安装（推荐）

```bash
npx paper-mentor-skill install
```

### 方式二：从 GitHub 安装

```bash
git clone https://github.com/YOUR_USERNAME/paper-mentor-skill.git ~/.claude/skills/paper-mentor
```

### 方式三：手动安装

将 `paper-mentor` 目录复制到：
- macOS/Linux: `~/.claude/skills/paper-mentor/`
- Windows: `%USERPROFILE%\.claude\skills\paper-mentor\`

## 验证安装

在 Claude Code 中输入：
```
/skills
```
或直接使用：
```
/paper-mentor https://arxiv.org/abs/1706.03762
```

### 基本用法

```
/paper-mentor https://arxiv.org/abs/1706.03762
```

或提供 arXiv ID：

```
/paper-mentor 1706.03762
```

### 交互流程

1. **输入论文** - 提供 arXiv URL 或 ID
2. **领域探索** - 系统搜索并展示 10 篇相似论文
3. **难度选择** - 选择问题难度 (beginner/intermediate/advanced)
4. **交互问答** - 回答问题并获得反馈
5. **报告输出** - 可选输出完整学习报告

## 文件结构

```
paper-mentor/
├── SKILL.md              # Skill 定义
├── master_agent.py       # 主协调器
├── paper_explorer.py     # 论文搜索和领域分析
├── teacher_agent.py      # 问题生成和交互
├── evaluator_agent.py    # 答案评估
├── utils.py              # 工具函数
└── requirements.txt      # Python 依赖
```

## Agent 架构

```
Master Orchestrator
  ↓
Paper Explorer Agent (关键词提取 → HuggingFace 搜索 → 领域分析)
  ↓
Teacher Agent (问题生成 → 交互问答)
  ↓
Evaluator Agent (答案评估 → 反馈)
```

## 问题难度级别

| 级别 | 描述 |
|------|------|
| beginner | 简单语言和基础概念，提供提示 |
| intermediate | 标准技术语言，平衡概念和应用 |
| advanced | 高级技术语言，关注分析、评估和创造 |

## Bloom 分类法

问题涵盖 6 个认知层次：
- 📗 **Remember** - 回忆事实
- 📘 **Understand** - 解释概念
- 📙 **Apply** - 应用知识
- 📕 **Analyze** - 分析比较
- 📔 **Evaluate** - 评价判断
- 📒 **Create** - 综合创新

## 测试用例

### Attention Is All You Need
```
/paper-mentor https://arxiv.org/abs/1706.03762
```

### ResNet
```
/paper-mentor https://arxiv.org/abs/1512.03385
```

## 依赖

```bash
pip install -r requirements.txt
```

## 开发说明

这是迭代周期 #1 的框架实现。待完善功能：
- [ ] HuggingFace 搜索实际实现 (需要 WebFetch 集成)
- [ ] LLM 调用集成
- [ ] 完整集成测试
- [ ] 错误处理和日志记录

## 相关文档

- [设计文档](../../docs/plans/2026-03-05-paper-mentor-design.md)
- [迭代日志](../../docs/iterations/iteration-1-summary-full.md)
- [进度总览](../../docs/progress-summary.md)
