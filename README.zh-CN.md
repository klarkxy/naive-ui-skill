# Naive UI Skill

> 🌐 **您正在阅读简体中文版本。** [English →](./README.md)

一个用于 [Naive UI](https://www.naiveui.com/)（Vue 3 组件库）的 Claude skill。内容根据官方仓库 `tusen-ai/naive-ui` 自动生成。

## 安装

可根据自己的环境任选其一，三种方式最终都会把 skill 安装到 `~/.claude/skills/naive-ui/`。

### 方式 A — `npx skills`（推荐；适用于 Claude Code、Codex、Cursor、Windsurf）

```bash
npx skills add klarkxy/naive-ui-skill --skill naive-ui -g -y
```

这条命令会从本仓库下载 `naive-ui/` 子目录并放入全局 skills 目录，无需 `git`。后续更新只需执行 `npx skills update klarkxy/naive-ui-skill`。

### 方式 B — 一行 shell 安装脚本（无需 Node）

```bash
curl -fsSL https://raw.githubusercontent.com/klarkxy/naive-ui-skill/main/install.sh | bash
```

只依赖 POSIX 标准的 `curl` + `tar`。可通过环境变量 `NAIVE_UI_SKILL_DIR` 自定义安装目录。

### 方式 C — 手动 clone / 本地打包

```bash
# 方式一：从 clone 出来的目录直接拷贝
git clone https://github.com/klarkxy/naive-ui-skill.git
cp -r naive-ui-skill/skills/naive-ui ~/.claude/skills/

# 方式二：先在本地打包成 zip，再解压安装
git clone https://github.com/klarkxy/naive-ui-skill.git
cd naive-ui-skill
python scripts/package_skill.py
unzip dist/naive-ui.zip -d ~/.claude/skills/
```

> 若使用 Codex / Trae / 其他 agent，请把 `~/.claude/skills/` 替换为 `~/.codex/skills/` / `~/.trae/skills/` 等。

## 使用方法

安装完成后，可以显式调用：

```
/skill naive-ui
```

也可以依赖 description 自动匹配：只要用户请求中包含 "Naive UI"、`n-data-table`、`n-form`、`"Naive UI 组件 / 主题 / 暗色"`、`"nuxt 集成 naive-ui"` 等关键词，就会触发本 skill。

## 来源与许可

内容基于 [tusen-ai/naive-ui](https://github.com/tusen-ai/naive-ui)（MIT 协议）自动生成。组件的官方 API 名称、默认值、版本字段等以官方仓库为准；本 skill 只在其上补充了路由、模式（patterns）与决策支持。
