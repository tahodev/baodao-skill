# 安裝指南

baodao-skill 透過 `npx skills add` 安裝。需要 Node.js 18 以上。

## 需求

- Node.js 18 以上與 `npx`
- 執行期工具（各技能用到）：`curl`（全部技能）、`jq`（youbike-realtime、taiwan-garbage）、`python3`（invoice-winning-numbers、taiwan-weather）、`pdftotext`（invoice-winning-numbers 的 PDF 清單）、`awk` 與 `sed`（taiwan-garbage 的台北 CSV）

## 安裝全部技能

```bash
npx --yes skills add tahodev/baodao-skill --all -g
```

## 只安裝一個技能

```bash
npx --yes skills add tahodev/baodao-skill --skill taiwan-weather -g
```

技能名就是倉庫根目錄下的目錄名（例如 `invoice-winning-numbers`、`youbike-realtime`、`taiwan-garbage`、`taiwan-weather`、`cwa-weather`）。

## 全域與專案安裝

- `-g`：安裝到使用者的全域技能目錄，所有專案都能用。
- 不加 `-g`：安裝到目前專案，只有該專案的代理能用到。

## 乾淨環境安裝實測（2026-09-11）

以 Node.js v22 / npm 10.9、空的 HOME 與 npm cache、無 TTY（非互動）的環境實際執行上面的指令：

- `--all -g`：非互動也能完成，5 個技能安裝到 `~/.agents/skills/<技能名>/`，各代理的技能目錄（`~/.claude/skills/<技能名>/` 等）以 symlink 連結過去。`Eve` 與 `PromptScript` 兩個目標不支援全域安裝會被略過 — 這是安裝器本身的行為，不是技能的問題。
- `--skill <名稱> -g`：互動環境會出現「要裝到哪些代理」的選擇提示；**非互動環境（CI、SSH 等無 TTY）提示會被取消，結束碼 1、什麼都不裝**。這種情況要加 `-y`（或用 `--agent <名稱>` / `--agent '*'` 指定代理）：

```bash
npx --yes skills add tahodev/baodao-skill --skill taiwan-weather -g -y
```

- 加 `-y` 後確認 `~/.agents/skills/taiwan-weather/SKILL.md` 安裝成功。

## 確認安裝

```bash
ls ~/.agents/skills 2>/dev/null || ls ~/.claude/skills 2>/dev/null || true
```

在支援的代理（Claude Code、Codex、OpenCode 等）裡，安裝後重啟或重新整理，代理就會在需要時自動讀取對應的 SKILL.md。

## 移除

刪除技能目錄即可，例如：

```bash
rm -rf ~/.agents/skills/taiwan-weather
```

## English

Install with `npx skills add` (Node.js 18+). Use `--all` for every skill or `--skill <name>` for one, and `-g` for a global install. Skill names are the top-level directories in this repo. Runtime tools used by the skills: `curl` (all), `jq` (youbike-realtime, taiwan-garbage), `python3` (invoice-winning-numbers, taiwan-weather), `pdftotext` (invoice PDF lists), `awk`/`sed` (taiwan-garbage Taipei CSV).

Verified in a clean environment (2026-09-11, Node.js v22 / npm 10.9, empty HOME and npm cache, no TTY): `--all -g` installs all 5 skills non-interactively into `~/.agents/skills/<skill>/` with agent directories such as `~/.claude/skills/<skill>/` symlinked to them. A single `--skill <name> -g` install cancels its agent-picker prompt without a TTY and installs nothing (exit code 1) - add `-y` (or `--agent <name>` / `--agent '*'`) in CI/SSH. The `Eve` and `PromptScript` targets are skipped by the installer itself (no global-install support), not a skill problem. Restart or refresh your agent after installing; it will pick up each SKILL.md automatically. To uninstall, delete the skill directory.
