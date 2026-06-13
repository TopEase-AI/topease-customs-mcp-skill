# 分发提交材料

本文件用于把 TOPEASE 海关数据 MCP skill 提交到 Agent Skills / Claude Code / MCP 目录平台。

## 已发布仓库

| 类型 | 仓库 |
| --- | --- |
| Agent Skill / Claude Code Plugin | https://github.com/TopEase-AI/topease-customs-mcp-skill |
| MCP Server | https://github.com/TopEase-AI/topease-customs-mcp-server |

## OpenAI / Codex Agent Skills

提交内容：

- Skill 目录：`topease-customs-mcp/`
- 核心文件：`topease-customs-mcp/SKILL.md`
- OpenAI/Codex 元数据：`topease-customs-mcp/agents/openai.yaml`
- MCP dependency：`https://mcp.topease.net/mcp`

推荐描述：

```text
TOPEASE 海关数据 MCP Agent Skill，帮助 Codex / ChatGPT Agent Skills 把自然语言贸易查询转换为 search_customs_data MCP 调用，用于查询全球海关进出口贸易记录、买家线索、供应商线索、HS 编码样本和企业交易记录。
```

## Claude Code Plugin Marketplace

本仓库已经包含 Claude Code marketplace 结构：

```text
.claude-plugin/marketplace.json
plugins/topease-customs-mcp/.claude-plugin/plugin.json
plugins/topease-customs-mcp/.mcp.json
plugins/topease-customs-mcp/skills/topease-customs-mcp/SKILL.md
```

用户安装命令：

```bash
claude plugin marketplace add TopEase-AI/topease-customs-mcp-skill
claude plugin install topease-customs-mcp@topease-agent-skills
```

使用前提：

```bash
export TOPEASE_MCP_API_KEY="trdmcp_live_xxx"
```

验证命令：

```bash
claude plugin validate .
claude plugin validate plugins/topease-customs-mcp
```

## Smithery

可提交对象：MCP server，而不是 skill 仓库。

推荐仓库：

```text
https://github.com/TopEase-AI/topease-customs-mcp-server
```

当前状态：

- 远程 MCP endpoint：`https://mcp.topease.net/mcp`
- Transport：Streamable HTTP
- Auth：`Authorization: Bearer <TOPEASE_API_KEY>`

注意：Smithery URL 发布要求鉴权型服务支持 OAuth。当前 TOPEASE MCP 远程服务使用 Bearer API key，不是 OAuth，因此建议先补 OAuth 或使用 Smithery 支持的 MCPB/托管方案后再正式发布。

## Glama / PulseMCP / MCP Server Directory

提交对象：

```text
https://github.com/TopEase-AI/topease-customs-mcp-server
```

建议字段：

| 字段 | 值 |
| --- | --- |
| Name | TOPEASE Customs MCP |
| Description | Query global customs import/export trade records through TOPEASE / Tradee MCP. |
| Repository | `https://github.com/TopEase-AI/topease-customs-mcp-server` |
| Package | `topease-mcp` |
| Transport | stdio, streamable HTTP |
| Remote endpoint | `https://mcp.topease.net/mcp` |
| Auth | Bearer API key from Tradee MCP service |
| Tags | customs-data, trade-data, mcp, fastmcp, tradee, topease |

## mcpservers.org / Agent Skills Library

可分别提交：

- Skill：`https://github.com/TopEase-AI/topease-customs-mcp-skill`
- MCP server：`https://github.com/TopEase-AI/topease-customs-mcp-server`

推荐一句话介绍：

```text
TOPEASE Customs MCP Skill connects agents to Tradee customs trade data, enabling buyer discovery, supplier discovery, company trade record lookup, product keyword search, HS code search, and country/market import-export sample analysis.
```
