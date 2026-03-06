# 🎓 Paper Mentor Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![npm version](https://img.shields.io/npm/v/paper-mentor-skill.svg)](https://www.npmjs.com/package/paper-mentor-skill)
[![npm downloads](https://img.shields.io/npm/dm/paper-mentor-skill.svg)](https://www.npmjs.com/package/paper-mentor-skill)

> **让论文阅读更高效，让知识吸收更深入**

一个用于深入理解学术论文的 Claude Code Skill，基于多 Agent 架构，帮助您：
- 📚 从 HuggingFace Papers 搜索相似论文，建立领域认知
- 🧠 提取研究方向、进展演变、核心概念
- 💬 基于 Bloom 分类法生成问题，提供交互式学习体验

---

## ✨ 特性亮点

| 特性 | 描述 |
|------|------|
| 🔍 **智能搜索** | 从 HuggingFace Papers 自动搜索 10 篇相似论文 |
| 🧩 **多 Agent 架构** | Master + Paper Explorer + Teacher + Evaluator 协同工作 |
| 📖 **Bloom 分类法** | 涵盖记忆、理解、应用、分析、评价、综合 6 个认知层次 |
| 💡 **交互式学习** | 针对性评估答案，提供深度反馈 |
| ⚡ **高效执行** | 搜索时间 < 30 秒 |

---

## 🚀 快速开始

### 安装

```bash
# 方式一：使用 npx 安装（推荐）
npx paper-mentor-skill install

# 方式二：从 GitHub 安装
git clone https://github.com/sellerbubble/paper-mentor-skill.git ~/.claude/skills/paper-mentor
```

### 使用

在 Claude Code 中输入：

```bash
/paper-mentor https://arxiv.org/abs/1706.03762
```

或直接提供 arXiv ID：

```bash
/paper-mentor 1706.03762
```

---

## 📖 使用示例

### 示例 1：Attention Is All You Need

```bash
/paper-mentor https://arxiv.org/abs/1706.03762
```

**你将获得**：
- 相似论文：BERT, GPT, Vision Transformer 等
- 核心概念：Transformer, Self-Attention, Multi-head Attention
- 问题涵盖：位置编码、注意力机制、并行性等

### 示例 2：ResNet

```bash
/paper-mentor https://arxiv.org/abs/1512.03385
```

**你将获得**：
- 相似论文：VGG, Inception, DenseNet 等
- 核心概念：残差学习、跳跃连接、深度网络
- 问题涵盖：梯度消失、bottleneck 设计、残差块等

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────┐
│          🎓 Master Orchestrator Agent               │
│  - 流程管理 · 任务分配 · 结果聚合                    │
└──────────────┬──────────────┬──────────────┬─────────┘
               │              │              │
        ┌──────▼──────┐  ┌────▼─────┐  ┌───▼────────┐
        │ 📚 Paper    │  │ 🧑‍🏫       │  │ ✅         │
        │   Explorer  │  │ Teacher  │  │ Evaluator  │
        │   Agent     │  │ Agent    │  │ Agent      │
        └─────────────┘  └──────────┘  └────────────┘
```

### Agent 职责

| Agent | 职责 | 输出 |
|-------|------|------|
| **Master Orchestrator** | 整体流程控制 | 最终报告 |
| **Paper Explorer** | 论文搜索与领域分析 | 相似论文 + 领域报告 |
| **Teacher Agent** | 问题生成与交互 | 问题集 + 反馈 |
| **Evaluator Agent** | 答案评估 | 评分 + 建议 |

---

## 📁 文件结构

```
paper-mentor/
├── SKILL.md              # Skill 核心定义
├── README.md             # 使用说明
├── QUICKSTART.md         # 快速开始指南
├── PUBLISHING.md         # 发布指南
├── package.json          # npm 包配置
├── index.js              # 安装脚本
├── master_agent.py       # 主协调器
├── paper_explorer.py     # 论文搜索模块
├── teacher_agent.py      # 问题生成模块
├── evaluator_agent.py    # 答案评估模块
├── utils.py              # 工具函数
└── requirements.txt      # Python 依赖
```

---

## 🔧 配置要求

### Python 依赖

```bash
pip install -r requirements.txt
```

### 环境变量（可选）

```bash
# .env 文件
OPENAI_API_KEY=your_api_key_here
```

---

## 🧪 测试用例

| 论文 | arXiv ID | 预期结果 |
|------|----------|----------|
| Attention Is All You Need | 1706.03762 | Transformer, Self-Attention |
| ResNet | 1512.03385 | 残差学习，Skip Connection |
| BERT | 1810.04805 | Bidirectional, Pre-training |
| GPT | 2005.14165 | Language Model, Few-shot |

---

## 📚 学习路径

```
1. 输入论文 URL/ID
       ↓
2. 获取论文内容 (arXiv API)
       ↓
3. 提取关键词 (LLM)
       ↓
4. 搜索 HuggingFace Papers
       ↓
5. 领域分析报告
       ↓
6. 生成 Bloom 分类问题
       ↓
7. 交互问答 + 反馈
       ↓
8. 输出学习报告
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

```bash
# 克隆仓库
git clone https://github.com/sellerbubble/paper-mentor-skill.git

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/
```

---

## 📄 许可证

[MIT License](LICENSE)

---

## 📬 联系方式

- **作者**: sellerbubble
- **邮箱**: 3210106011@zju.edu.cn / wli954@connect.hkust-gz.edu.cn
- **GitHub**: [sellerbubble](https://github.com/sellerbubble)

---

## 🙏 致谢

感谢以下开源项目：

- [Claude Code](https://claude.ai/code) - AI 编程助手
- [HuggingFace Papers](https://huggingface.co/papers) - 论文资源
- [arXiv API](https://arxiv.org/help/api) - 论文数据

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star 吧！**

</div>
