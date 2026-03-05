# Paper Mentor Skill 发布指南

## 📦 通过 npx 安装的技能配置

您的 Skill 现在已经支持通过 `npx` 安装！

---

## 📋 发布前准备

### 1. 更新 package.json

编辑 `/Users/liwenhao.109/.claude/skills/paper-mentor/package.json`：

```json
{
  "name": "paper-mentor-skill",
  "version": "1.0.0",
  "author": "您的名字 <您的邮箱>",
  "repository": {
    "url": "https://github.com/您的用户名/paper-mentor-skill.git"
  }
}
```

### 2. 创建 GitHub 仓库

```bash
cd /Users/liwenhao.109/.claude/skills/paper-mentor

# 初始化为 git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Paper Mentor Skill v1.0"

# 在 GitHub 创建仓库后关联
git remote add origin https://github.com/您的用户名/paper-mentor-skill.git

# 推送
git push -u origin main
```

---

## 🚀 发布到 npm

### 方式一：发布到公共 npm（推荐）

1. **注册 npm 账号**（如果没有）
   ```bash
   npm adduser
   ```

2. **测试包内容**
   ```bash
   cd /Users/liwenhao.109/.claude/skills/paper-mentor
   npm pack --dry-run
   ```

3. **发布到 npm**
   ```bash
   npm publish
   ```

4. **验证发布**
   访问 https://www.npmjs.com/package/paper-mentor-skill

### 方式二：发布为 scoped package（避免命名冲突）

如果您的包名与他人冲突，可以使用 scoped package：

1. **修改 package.json**
   ```json
   {
     "name": "@您的用户名/paper-mentor-skill"
   }
   ```

2. **发布**
   ```bash
   npm publish --access public
   ```

3. **用户安装方式**
   ```bash
   npx @您的用户名/paper-mentor-skill install
   ```

---

## 📥 用户安装方式

### 公共 npm 包
```bash
# 直接安装
npx paper-mentor-skill install
```

### Scoped package
```bash
npx @您的用户名/paper-mentor-skill install
```

### 从 GitHub 安装
```bash
git clone https://github.com/您的用户名/paper-mentor-skill.git ~/.claude/skills/paper-mentor
```

---

## ✅ 验证安装

在 Claude Code 中输入：

```
/skills
```

或直接使用：

```
/paper-mentor https://arxiv.org/abs/1706.03762
```

---

## 📝 文件清单

发布前确保包含以下文件：

| 文件 | 必需 | 说明 |
|------|------|------|
| `SKILL.md` | ✅ | 核心技能定义 |
| `README.md` | ✅ | 使用说明 |
| `package.json` | ✅ | npm 包配置 |
| `index.js` | ✅ | 安装脚本入口 |
| `.npmignore` | ✅ | npm 忽略文件 |
| `QUICKSTART.md` | 可选 | 快速开始指南 |
| `*.py` | 可选 | Python 框架代码 |
| `requirements.txt` | 可选 | Python 依赖 |

---

## 🔧 故障排除

### 问题：npm publish 失败 - 包名已存在

**解决方案**：
1. 修改 package.json 中的包名，添加唯一前缀
2. 或使用 scoped package：`@您的用户名/paper-mentor-skill`

### 问题：安装后技能不显示

**解决方案**：
1. 确认安装位置：`~/.claude/skills/paper-mentor/`
2. 重启 Claude Code
3. 检查 SKILL.md 格式是否正确

### 问题：npx 命令找不到

**解决方案**：
```bash
# 确保安装了 Node.js 和 npm
node --version
npm --version

# 如果未安装，访问 https://nodejs.org/
```

---

## 📊 完整目录结构

```
paper-mentor/
├── .npmignore            # npm 忽略文件
├── package.json          # npm 包配置
├── index.js              # 安装脚本入口
├── SKILL.md              # 核心技能定义（必需）
├── README.md             # 使用说明（必需）
├── QUICKSTART.md         # 快速开始指南
├── master_agent.py       # 主协调器框架
├── paper_explorer.py     # 论文搜索框架
├── teacher_agent.py      # 问题生成框架
├── evaluator_agent.py    # 评估框架
├── utils.py              # 工具函数
└── requirements.txt      # Python 依赖
```

---

## 🎯 快速发布命令汇总

```bash
# 1. 进入目录
cd /Users/liwenhao.109/.claude/skills/paper-mentor

# 2. 更新 package.json（修改作者和仓库信息）

# 3. 初始化为 git 仓库
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/您的用户名/paper-mentor-skill.git
git push -u origin main

# 4. 发布到 npm
npm adduser        # 首次需要
npm publish

# 5. 验证
# 访问 https://www.npmjs.com/package/paper-mentor-skill
```

---

## 📚 相关资源

- [npm 发布文档](https://docs.npmjs.com/packages-and-modules/contributing-packages-and-projects/publishing-packages)
- [Claude Code Skills 文档](https://docs.anthropic.com/claude-code/)
- [Scoped packages](https://docs.npmjs.com/cli/using-npm/scope)
