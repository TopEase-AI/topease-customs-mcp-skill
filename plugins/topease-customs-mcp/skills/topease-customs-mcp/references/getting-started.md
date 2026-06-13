# TOPEASE Customs MCP Skill 上手指南

本文件用于回答用户关于安装、调用、获取 MCP key 和排障的问题。不要把用户的完整 API key 写入最终回答、日志或文档。

## 一键调用需要满足的条件

用户要“一键调用”本 skill，至少需要满足以下条件：

1. 已安装 `topease-customs-mcp` skill。安装方式可以是 skill 广场安装，也可以是把 skill 目录放入 Codex、ChatGPT、Claude Code 或其它客户端可发现的 skills 目录。
2. 运行环境支持读取 skill 的 `agents/openai.yaml` 并支持其中声明的 MCP dependency，或已在客户端中手动配置 MCP server。
3. MCP 客户端能访问公网地址 `https://mcp.topease.net/mcp`。
4. 用户拥有 Tradee/TOPEASE MCP API key，并能把它配置为 MCP 请求头 `Authorization: Bearer <TOPEASE_API_KEY>`。
5. Tradee 账户有访问 MCP 海关数据的权限和足够余额。若账户按余额计费，余额不足会导致查询失败或被拦截。
6. 用户查询时至少提供一个有效过滤条件：企业名、产品关键词、HS 编码或国家/地区。

如果运行环境不能自动读取 `agents/openai.yaml`，就不能真正“一键”接入 MCP；需要用户手动添加 MCP server 配置。Claude Code 支持目录式 custom skill（`SKILL.md` + references/scripts），但 MCP server 仍建议单独配置。

## Claude Code 使用说明

Claude Code 可以使用这个 skill，但要区分两件事：

- skill 本体：把 `topease-customs-mcp/` 目录放到 Claude Code 可发现的 skills 目录，Claude Code 即可读取 `SKILL.md`、`references/` 和 `scripts/`。
- MCP 数据连接：把 `topease-customs-data` MCP server 配到 Claude Code 的 MCP 配置里，并提供 Tradee/TOPEASE MCP API key。

如果 Claude Code 已能识别 skill，但调用时提示没有 `search_customs_data` 工具，通常是 MCP server 没有配置或没有鉴权，而不是 skill 文件本身损坏。

## 推荐调用方式

安装 skill 并配置 MCP 后，用户可以直接在对话里显式调用：

```text
用 $topease-customs-mcp 查询 2025 年美国 LED 进口海关记录，列前 5 条。
```

也可以用业务化说法：

```text
帮我找墨西哥 brake pad 的进口买家线索。
```

Agent 应把它转换为 `search_customs_data` 参数，例如：

```json
{
  "country": "Mexico",
  "product_keyword": "brake pad",
  "trade_type": "import",
  "page_index": 1,
  "page_size": 10,
  "sort_by": "tradedate",
  "sort_order": "desc"
}
```

## 在 Tradee 获取 MCP API key

可按以下步骤指导用户：

1. 打开 Tradee 平台：`https://tradee.topease.net/`。
2. 注册账号或登录已有账号。
3. 进入左侧菜单的“账户中心”或“订阅与管理”区域。
4. 打开“MCP 服务”页面。
5. 点击“创建 API key”。
6. 选择正式环境 key，勾选需要的服务范围。通常至少需要：
   - 海关数据查询
   - 客户搜索日志查询（如需要查日志）
7. 创建后立即复制完整 key。完整 key 只在创建成功时展示一次，后续列表只显示脱敏 key。
8. 妥善保存 key，并配置到 MCP 客户端。不要把 key 发给无关人员，不要提交到 GitHub。
9. 若页面提示余额不足或可查询行数不足，先在 Tradee 账户充值或联系管理员开通额度。

常见 key 形态类似：

```text
trdmcp_live_...
```

不要在最终回答中展示完整真实 key。

## 手动配置 MCP 客户端

streamable HTTP 模式：

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

stdio 模式：

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

如果用户使用 Python 包安装，也可以用：

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

注意：上游 README 里部分示例可能写成 `python -m topease-mcp`；Python 模块名应使用下划线形式 `topease_mcp`。

## 使用脚本生成配置

运行：

```bash
python scripts/generate_mcp_config.py --mode streamable-http
python scripts/generate_mcp_config.py --mode stdio
```

默认输出占位符 `<TOPEASE_API_KEY>`。如果用户明确要写入 key，可传 `--api-key`，但不建议把含真实 key 的配置提交到仓库。

## 排障清单

MCP 工具不可见：

- 确认 skill 已安装并被当前客户端加载。
- 确认客户端支持 skill dependencies 或已手动配置 MCP server。
- 确认 MCP server 名称为 `topease-customs-data`。

鉴权失败：

- 检查请求头是否是 `Authorization: Bearer <TOPEASE_API_KEY>`。
- 检查 key 是否为 Tradee MCP 服务页创建的完整 key，不是脱敏 key。
- 检查 key 是否被删除、吊销或复制不完整。

余额或额度不足：

- 打开 Tradee 的 MCP 服务页或账户中心查看余额。
- 按余额计费时，海关数据查询可能按返回行数扣点。
- 充值后重试，或联系管理员确认权限。

查不到数据：

- 放宽日期范围。
- 缩短 HS 编码前缀。
- 尝试中文、英文或 ISO 国家写法。
- 把产品关键词换成更接近海关描述的英文词。
- 如果只给了公司名，尝试补国家、进出口方向或产品关键词。
