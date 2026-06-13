<div align="center">

# TOPEASE 海关数据 MCP Skill

通过 TOPEASE / Tradee Customs MCP，让 Codex、ChatGPT、Claude Code 等 Agent Skills 客户端直接查询全球海关进出口贸易记录。

[![Skill](https://img.shields.io/badge/Agent%20Skill-TOPEASE%20Customs-blue)](./topease-customs-mcp/SKILL.md)
[![MCP](https://img.shields.io/badge/MCP-streamable%20HTTP-7c3aed)](https://mcp.topease.net/mcp)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/topease020/topease-customs-mcp-server)
[![Tradee](https://img.shields.io/badge/Tradee-tradee.topease.net-orange)](https://tradee.topease.net/)

[快速开始](#快速开始) · [Claude Code 插件](#claude-code-插件) · [获取 MCP Key](#获取-mcp-key) · [手动配置 MCP](#手动配置-mcp) · [分发平台](#分发平台) · [排障](#排障)

</div>

## 为什么需要这个 Skill

大模型本身不知道你的海关数据权限，也不能凭空生成真实贸易记录。这个 skill 做两件事：

- 教 agent 如何把自然语言需求转换成 TOPEASE Customs MCP 的 `search_customs_data` 参数。
- 约束 agent 如何解释海关记录：说明查询口径、分页、样本边界、潜在线索和下一步查询建议。

适合这些场景：

| 任务 | 示例 |
| --- | --- |
| 找海外买家 | “帮我找墨西哥 brake pad 的进口买家线索” |
| 查企业交易 | “看 IKEA SUPPLY AG 的出口记录” |
| 查产品样本 | “查询 2025 年美国 LED 进口记录前 5 条” |
| 查 HS 市场 | “日本 8415 类目进口样本” |
| 配置 MCP | “帮我生成 Claude Code / Codex 的 TOPEASE MCP 配置” |

## 快速开始

### 1. 安装 Skill

把 `topease-customs-mcp/` 目录放到你的客户端可发现的 skills 目录，或通过支持 skills 的 marketplace / plugin 机制安装。

```text
topease-customs-mcp/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

### 2. 配置 TOPEASE MCP

如果你的客户端支持读取 `agents/openai.yaml` 里的 MCP dependency，可直接按客户端流程授权。

如果不支持，手动添加 MCP server：

```json
{
  "mcpServers": {
    "topease-customs-data": {
      "type": "streamableHttp",
      "url": "https://mcp.topease.net/mcp",
      "headers": {
        "Authorization": "Bearer <TOPEASE_API_KEY>"
      }
    }
  }
}
```

### 3. 在对话里调用

```text
用 $topease-customs-mcp 查询 2025 年美国 LED 进口海关记录，列前 5 条。
```

也可以直接说业务需求：

```text
帮我找墨西哥 brake pad 的进口买家线索。
```

## Claude Code 插件

本仓库同时可作为 Claude Code plugin marketplace 使用：

```bash
claude plugin marketplace add TopEase-AI/topease-customs-mcp-skill
claude plugin install topease-customs-mcp@topease-agent-skills
```

插件目录位于：

```text
plugins/topease-customs-mcp/
├── .claude-plugin/plugin.json
├── .mcp.json
├── README.md
└── skills/topease-customs-mcp/
```

使用前在本机配置 MCP key：

```bash
export TOPEASE_MCP_API_KEY="trdmcp_live_xxx"
```

`.mcp.json` 会通过环境变量生成请求头：

```json
{
  "mcpServers": {
    "topease-customs-data": {
      "type": "http",
      "url": "https://mcp.topease.net/mcp",
      "headers": {
        "Authorization": "Bearer ${TOPEASE_MCP_API_KEY}"
      }
    }
  }
}
```

说明：Claude Code 插件可以安装 skill 和声明 MCP server，但用户仍需要自己提供 Tradee/TOPEASE MCP API key。

如果你希望 Claude Code 里只显示单名 skill：`topease-customs-mcp`，不要用 plugin marketplace 安装，直接安装为 Claude Code custom skill：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/TopEase-AI/topease-customs-mcp-skill.git /tmp/topease-customs-mcp-skill
rm -rf ~/.claude/skills/topease-customs-mcp
cp -R /tmp/topease-customs-mcp-skill/topease-customs-mcp ~/.claude/skills/topease-customs-mcp
```

然后重启 Claude Code。此方式只安装 skill 本体，不会自动安装 `.mcp.json`，仍需单独配置 MCP server 或设置 `TOPEASE_MCP_API_KEY`。

## 获取 MCP Key

1. 打开 [Tradee 平台](https://tradee.topease.net/)。
2. 注册账号或登录已有账号。
3. 进入“账户中心”或“MCP 服务”页面。
4. 点击“创建 API key”。
5. 选择正式环境 key，并勾选需要的服务范围，通常至少需要“海关数据查询”。
6. 创建成功后立即复制完整 key。完整 key 只展示一次，后续列表只显示脱敏 key。
7. 把 key 配置到 MCP 客户端或密钥管理工具中。

常见 key 前缀类似：

```text
trdmcp_live_...
```

不要把完整 key 提交到 GitHub，也不要把它贴到公开 issue、README 或日志里。

## 客户端兼容

| 客户端 | Skill 支持 | MCP 配置建议 |
| --- | --- | --- |
| Codex | 支持 Agent Skills | 优先使用 `agents/openai.yaml`；不支持时手动配置 MCP |
| ChatGPT / OpenAI Agent Skills 环境 | 支持 Agent Skills | 依赖运行环境是否读取 `agents/openai.yaml` |
| Claude Code | 支持目录式 Custom Skills | skill 和 MCP 是两层；建议单独配置 MCP server |
| 其它 MCP 客户端 | 不一定支持 skill | 可只使用 README 中的 MCP 配置 |

## Claude Code

Claude Code 可以使用这个 skill 目录，但要区分两件事：

- Skill 本体：把 `topease-customs-mcp/` 放到 Claude Code 可发现的 skills 目录，Claude Code 即可读取 `SKILL.md`、`references/` 和 `scripts/`。
- MCP 数据连接：把 `topease-customs-data` MCP server 配到 Claude Code 的 MCP 配置里，并提供 `TOPEASE_MCP_API_KEY` 或 `Authorization: Bearer <TOPEASE_API_KEY>`。

如果 Claude Code 已能识别 skill，但调用时提示没有 `search_customs_data` 工具，通常是 MCP server 没有配置或没有鉴权，而不是 skill 文件损坏。

## 手动配置 MCP

### Streamable HTTP

```json
{
  "mcpServers": {
    "topease-customs-data": {
      "type": "streamableHttp",
      "url": "https://mcp.topease.net/mcp",
      "headers": {
        "Authorization": "Bearer <TOPEASE_API_KEY>"
      }
    }
  }
}
```

### Stdio

```json
{
  "mcpServers": {
    "topease-customs-data": {
      "command": "uvx",
      "args": ["topease-mcp"],
      "env": {
        "TOPEASE_MCP_API_KEY": "<TOPEASE_API_KEY>"
      }
    }
  }
}
```

如果使用 pip 安装包，也可以配置：

```json
{
  "mcpServers": {
    "topease-customs-data": {
      "command": "python",
      "args": ["-m", "topease_mcp"],
      "env": {
        "TOPEASE_MCP_API_KEY": "<TOPEASE_API_KEY>"
      }
    }
  }
}
```

## 生成配置片段

内置脚本可以生成 MCP 配置 JSON：

```bash
python topease-customs-mcp/scripts/generate_mcp_config.py --mode streamable-http
python topease-customs-mcp/scripts/generate_mcp_config.py --mode stdio
```

默认生成占位符 `<TOPEASE_API_KEY>`。也可以从环境变量读取：

```bash
export TOPEASE_MCP_API_KEY="trdmcp_live_xxx"
python topease-customs-mcp/scripts/generate_mcp_config.py --mode streamable-http
```

## 查询能力

MCP 工具名：`search_customs_data`

| 参数 | 说明 |
| --- | --- |
| `company_name` | 企业名称，模糊匹配进口商或出口商 |
| `product_keyword` | 产品描述关键词 |
| `hs_code` | HS 编码前缀 |
| `trade_type` | `import`、`export`、`all` |
| `country` | 国家/地区中文名、英文名、ISO-2 或 ISO-3 |
| `date_from` / `date_to` | 日期范围，格式 `YYYY-MM-DD` |
| `page_index` / `page_size` | 分页；`page_size` 最大 20 |
| `sort_by` | `tradedate`、`quantity`、`weight`、`uusd` |
| `sort_order` | `asc`、`desc` |

至少需要提供 `company_name`、`product_keyword`、`hs_code`、`country` 之一。

## 项目结构

```text
.
├── .claude-plugin/
│   └── marketplace.json
├── README.md
├── plugins/
│   └── topease-customs-mcp/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── .mcp.json
│       ├── README.md
│       └── skills/
│           └── topease-customs-mcp/
└── topease-customs-mcp/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── api-reference.md
    │   └── getting-started.md
    └── scripts/
        └── generate_mcp_config.py
```

## 分发平台

| 平台 | 当前可提交内容 | 说明 |
| --- | --- | --- |
| OpenAI / Codex Agent Skills | `topease-customs-mcp/` | `SKILL.md` 是核心文件，`agents/openai.yaml` 提供 OpenAI/Codex 元数据和 MCP dependency |
| Claude Code plugin marketplace | 本仓库根目录 | `.claude-plugin/marketplace.json` 指向 `plugins/topease-customs-mcp/` |
| Smithery / Glama / PulseMCP | MCP server 仓库 | 这些平台主要收录 MCP server，建议提交 [TopEase-AI/topease-customs-mcp-server](https://github.com/TopEase-AI/topease-customs-mcp-server) |
| mcpservers.org / Agent Skills Library | skill 仓库和 MCP server 仓库 | 可分别提交本仓库和 MCP server 仓库，覆盖 skill 与 MCP 两类入口 |

## 排障

| 问题 | 处理方式 |
| --- | --- |
| MCP 工具不可见 | 确认 skill 已安装，并确认 MCP server 已配置 |
| 鉴权失败 | 确认使用完整 key，不是脱敏 key；确认 header 是 `Authorization: Bearer <TOPEASE_API_KEY>` |
| 查不到数据 | 放宽日期范围、缩短 HS 编码、尝试中英文关键词或 ISO 国家写法 |
| 余额不足 | 到 Tradee MCP 服务页或账户中心查看余额，充值后重试 |

## 相关链接

- Tradee 平台：[https://tradee.topease.net/](https://tradee.topease.net/)
- TOPEASE Customs MCP Server：[TopEase-AI/topease-customs-mcp-server](https://github.com/TopEase-AI/topease-customs-mcp-server)
- MCP endpoint：`https://mcp.topease.net/mcp`
