# TOPEASE 海关数据 MCP Skill

这是一个面向 Codex、ChatGPT、Claude Code 等支持 Agent Skills / Custom Skills 的客户端的 skill，用于通过 TOPEASE/Tradee 海关数据 MCP 查询全球进出口贸易记录。适合查询产品关键词、HS 编码、企业名、国家/地区维度下的买家、供应商、进口商、出口商和出货样本。

## 一键调用需要满足什么条件

要让这个 skill 真正“一键调用”海关数据，需要同时满足：

1. 当前客户端支持 Agent Skills / Custom Skills，例如 Codex、ChatGPT 或 Claude Code。
2. 已安装本 skill：`topease-customs-mcp`。
3. 当前客户端支持读取 `agents/openai.yaml` 中声明的 MCP dependency，或已经手动配置 MCP server。
4. 当前网络可以访问 `https://mcp.topease.net/mcp`。
5. 已在 Tradee 获取 MCP API key。
6. MCP 请求携带鉴权：`Authorization: Bearer <TOPEASE_API_KEY>`。
7. Tradee 账号有 MCP 海关数据权限和足够余额。

如果客户端不支持自动读取 `agents/openai.yaml`，需要手动添加 MCP 配置。Claude Code 支持目录式 custom skill（`SKILL.md` + references/scripts），但是否自动读取 `agents/openai.yaml` 取决于具体运行环境；稳妥做法是在 Claude Code 里单独配置 `topease-customs-data` MCP server。见下方“手动配置 MCP”。

### Claude Code 说明

Claude Code 可以使用这个 skill 目录。把 `topease-customs-mcp/` 放到 Claude Code 可发现的 skills 目录后，Claude Code 可读取 `SKILL.md`、`references/` 和 `scripts/`。要真正查询海关数据，还需要把 TOPEASE MCP server 配到 Claude Code 的 MCP 配置里，并提供 `TOPEASE_MCP_API_KEY` 或 `Authorization: Bearer <TOPEASE_API_KEY>`。

## 如何调用

安装并配置 MCP 后，在对话里直接写：

```text
用 $topease-customs-mcp 查询 2025 年美国 LED 进口海关记录，列前 5 条。
```

也可以用自然语言：

```text
帮我找墨西哥 brake pad 的进口买家线索。
```

skill 会把请求转换为 MCP 工具 `search_customs_data` 的参数，并把结果整理成中文表格和业务观察。

## 如何在 Tradee 注册并获取 MCP key

1. 打开 Tradee 平台：<https://tradee.topease.net/>。
2. 注册账号或登录已有账号。
3. 进入左侧菜单的“账户中心”或“订阅与管理”区域。
4. 打开“MCP 服务”页面。
5. 点击“创建 API key”。
6. 选择正式环境 key，并勾选需要的服务范围。通常至少需要“海关数据查询”。
7. 创建成功后立即复制完整 key。完整 key 只展示一次，后续列表只显示脱敏 key。
8. 保存 key 到你的 MCP 客户端配置或密钥管理工具中。
9. 如果页面提示余额不足，先充值或联系管理员开通额度。

常见 key 前缀类似：

```text
trdmcp_live_...
```

不要把完整 key 提交到 GitHub。

## 手动配置 MCP

### streamable HTTP

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

### stdio

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

skill 内置脚本可以生成 MCP 配置 JSON：

```bash
python topease-customs-mcp/scripts/generate_mcp_config.py --mode streamable-http
python topease-customs-mcp/scripts/generate_mcp_config.py --mode stdio
```

默认生成占位符 `<TOPEASE_API_KEY>`。也可以读取环境变量：

```bash
export TOPEASE_MCP_API_KEY="trdmcp_live_xxx"
python topease-customs-mcp/scripts/generate_mcp_config.py --mode streamable-http
```

## Skill 文件结构

```text
topease-customs-mcp/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── api-reference.md
│   └── getting-started.md
└── scripts/
    └── generate_mcp_config.py
```

## 查询能力

MCP 工具名：`search_customs_data`

支持参数：

- `company_name`：企业名称
- `product_keyword`：产品关键词
- `hs_code`：HS 编码前缀
- `trade_type`：`import`、`export`、`all`
- `country`：国家/地区中文名、英文名、ISO-2 或 ISO-3
- `date_from` / `date_to`：日期范围
- `page_index` / `page_size`：分页，`page_size` 最大 20
- `sort_by`：`tradedate`、`quantity`、`weight`、`uusd`
- `sort_order`：`asc`、`desc`

至少需要提供 `company_name`、`product_keyword`、`hs_code`、`country` 之一。

## 排障

MCP 工具不可见：

- 确认 skill 已安装。
- 确认客户端支持 MCP dependency，或已经手动配置 MCP。
- 确认 server 名称为 `topease-customs-data`。

鉴权失败：

- 确认使用的是完整 key，不是脱敏 key。
- 确认 header 是 `Authorization: Bearer <TOPEASE_API_KEY>`。
- 确认 key 没有被删除或吊销。

查不到数据：

- 放宽日期范围。
- 缩短 HS 编码。
- 尝试中英文产品关键词。
- 尝试中文、英文或 ISO 国家写法。

余额不足：

- 到 Tradee MCP 服务页或账户中心查看余额。
- 充值后重试，或联系管理员确认权限。
