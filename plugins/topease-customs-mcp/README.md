# TOPEASE Customs MCP Claude Code Plugin

这是面向 Claude Code 的插件包，内置 `topease-customs-mcp` skill，并通过 `.mcp.json` 声明 TOPEASE Customs MCP server。

## 安装

在 Claude Code 中添加 marketplace：

```bash
claude plugin marketplace add TopEase-AI/topease-customs-mcp-skill
claude plugin install topease-customs-mcp@topease-agent-skills
```

## 使用前提

本插件不会也不应该保存真实 API key。使用前请在本机环境变量中设置：

```bash
export TOPEASE_MCP_API_KEY="trdmcp_live_xxx"
```

然后在 Claude Code 中发起查询：

```text
用 $topease-customs-mcp 查询 2025 年美国 LED 进口海关记录，列前 5 条。
```

如果 skill 可用但提示没有 `search_customs_data` 工具，请检查 `.mcp.json` 是否已被 Claude Code 加载，以及 `TOPEASE_MCP_API_KEY` 是否有效。
