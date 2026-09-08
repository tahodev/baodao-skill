# 安裝指南

baodao-skill 透過 `npx skills add` 安裝。需要 Node.js 18 以上。

## 安裝全部技能

```bash
npx --yes skills add tahodev/baodao-skill --all -g
```

## 只安裝一個技能

```bash
npx --yes skills add tahodev/baodao-skill --skill taiwan-weather -g
```

技能名就是倉庫根目錄下的目錄名(例如 `invoice-winning-numbers`、`youbike-realtime`、`taipei-garbage`、`taiwan-weather`)。

## 全域與專案安裝

- `-g`:安裝到使用者的全域技能目錄,所有專案都能用。
- 不加 `-g`:安裝到目前專案,只有該專案的代理能用到。

## 確認安裝

```bash
ls ~/.claude/skills 2>/dev/null || true
```

在支援的代理(Claude Code、Codex、OpenCode 等)裡,安裝後重啟或重新整理,代理就會在需要時自動讀取對應的 SKILL.md。

## 移除

刪除技能目錄即可,例如:

```bash
rm -rf ~/.claude/skills/taiwan-weather
```

## English

Install with `npx skills add` (Node.js 18+). Use `--all` for every skill or `--skill <name>` for one, and `-g` for a global install. Skill names are the top-level directories in this repo. Restart or refresh your agent after installing; it will pick up each SKILL.md automatically. To uninstall, delete the skill directory.
