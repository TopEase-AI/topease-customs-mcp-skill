# TOPEASE 海关数据 MCP 接口参考

参考来源：`https://github.com/topease020/topease-customs-mcp-server` 当前克隆版本。

本文件用于给 agent 精确查阅 MCP 连接方式、工具参数、返回字段和排障口径。面向最终用户回答时，不要直接暴露用户的完整 API key。

## MCP 服务

公共 streamable HTTP 地址：

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

本地 stdio 方式：

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

Python 包名是 `topease-mcp`，要求 Python 3.12+。如果用 `python -m` 方式启动，模块名应写作 `topease_mcp`。

## 工具：`search_customs_data`

用途：按企业、产品关键词、HS 编码、国家/地区、贸易方向、时间范围等条件组合查询全球海关进出口记录。

参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `company_name` | string | 否 | 企业名称，模糊匹配进口商或出口商。 |
| `product_keyword` | string | 否 | 产品描述关键词，例如 `led`、`valve`、`CABIN`。 |
| `hs_code` | string | 否 | HS 编码前缀匹配，例如 `8415`、`870830`。 |
| `trade_type` | string | 否 | `import`、`export` 或 `all`，默认 `all`。 |
| `country` | string | 否 | 国家/地区，支持中文名、英文名、ISO-2、ISO-3。 |
| `date_from` | string | 否 | 起始日期，格式 `YYYY-MM-DD`。 |
| `date_to` | string | 否 | 结束日期，格式 `YYYY-MM-DD`。 |
| `page_index` | integer | 否 | 页码，从 1 开始，默认 `1`。 |
| `page_size` | integer | 否 | 每页条数，当前公开查询建议不超过 20。 |
| `sort_by` | string | 否 | `tradedate`、`quantity`、`weight` 或 `uusd`，默认 `tradedate`。 |
| `sort_order` | string | 否 | `asc` 或 `desc`，默认 `desc`。 |

校验规则：

- `company_name`、`product_keyword`、`hs_code`、`country` 至少提供一个。
- `trade_type` 会映射到上游数值：`import` -> `1`，`export` -> `0`，`all` -> `2`。
- `page_size` 在当前 MCP 实现中会被限制到 20。

示例：

```json
{
  "product_keyword": "led",
  "country": "美国",
  "trade_type": "import",
  "date_from": "2025-01-01",
  "date_to": "2025-12-31",
  "page_index": 1,
  "page_size": 5
}
```

## 返回字段

记录可能包含以下中文展示字段：

| 字段 | 含义 |
| --- | --- |
| `单据ID` | 单据或提单编号。 |
| `海关编码` | HS 编码。 |
| `产品描述` | 海关记录中的产品描述。 |
| `贸易类型` | `进口` 或 `出口`。 |
| `进口商` | 进口商名称。 |
| `出口商` | 出口商名称。 |
| `数量` | 数量。 |
| `数量单位` | 数量单位。 |
| `重量` | 重量。 |
| `金额(USD)` | 美元金额。 |
| `贸易日期` | 贸易日期。 |
| `原产国` | 原产国。 |
| `原产国ID` | 原产国 ID。 |

分页字段：

| 字段 | 含义 |
| --- | --- |
| `total` | 匹配总记录数。 |
| `page_index` | 当前页码。 |
| `page_size` | 每页条数。 |
| `total_pages` | 总页数。 |

## 排障

缺少 key：

- streamable HTTP 模式配置 `Authorization: Bearer <TOPEASE_API_KEY>`。
- stdio 模式配置环境变量 `TOPEASE_MCP_API_KEY`。

空结果：

- 放宽日期范围。
- 缩短 HS 编码前缀。
- 尝试中文、英文或 ISO 国家写法。
- 更换更贴近海关描述的产品关键词。

结果过多：

- 增加国家/地区、日期范围、HS 编码、企业名或贸易方向过滤。
- 先取 `page_size: 5` 到 `10` 观察样本，再决定是否翻页。

鉴权、余额或计费错误：

- 这是服务侧访问问题。要求用户检查 Tradee/TOPEASE 账号、MCP key 状态和余额，不要盲目重复请求。
