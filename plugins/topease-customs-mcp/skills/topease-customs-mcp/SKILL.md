---
name: topease-customs-mcp
description: 通过 TOPEASE/Tradee Customs MCP 查询和分析全球海关贸易记录。用于用户要求查询进出口海关数据、买家或供应商出货记录、产品关键词贸易数据、HS 编码贸易数据、国家或市场进出口记录、进口商/出口商线索，或要求配置、接入、排查 TOPEASE 海关数据 MCP 服务时。
---

# TOPEASE 海关数据 MCP

## 能力定位

使用 TOPEASE Customs MCP 获取全球海关贸易记录，并把原始记录整理成可读的业务结论。该 skill 适合处理“查数据、找买家、找供应商、看某类产品出口/进口记录、按 HS 编码看市场、按企业名看交易记录”等任务。

它只负责使用 MCP 查询和解释海关记录，不负责伪造缺失数据、不负责绕过鉴权、不把单页样本包装成完整市场结论。需要更完整的参数表、返回字段、客户端配置或排障细节时，读取 `references/api-reference.md`。

如果用户问“怎么安装、怎么一键调用、怎么在 Tradee 拿 MCP key、需要满足什么条件”，读取 `references/getting-started.md`。如果用户只需要生成 MCP 客户端配置 JSON，可运行 `scripts/generate_mcp_config.py`。

## 先判断是否应该调用 MCP

满足以下任一场景时，优先使用本 skill：

- 用户问某个产品、HS 编码、企业、国家/地区的海关进出口记录。
- 用户想找某产品的海外买家、供应商、进口商、出口商、交易对手或出货线索。
- 用户给出公司名，要求查看该公司的进口/出口记录、采购来源、销售市场或交易产品。
- 用户给出 HS 编码，要求查看某国家/市场下的进口或出口样本。
- 用户要求接入 `topease-mcp`、`mcp.topease.net/mcp`、Tradee MCP、TOPEASE 海关数据 MCP。
- 用户遇到 MCP 鉴权、API key、streamable HTTP、stdio 配置问题。

不要在以下场景硬调用：

- 用户只要宏观政策、税率、法规或公开网页搜索，且没有要求海关记录。
- 用户要求“全量市场报告”，但没有任何可用于查询的产品、HS、公司或国家线索。先提取条件或要求补充条件。
- 当前环境没有可用 MCP 工具或 API key。此时说明依赖缺失并给配置建议，不要编造数据。

## 标准执行流程

1. 解析用户意图，明确查询目标是产品、HS 编码、公司、国家/地区，还是组合查询。
2. 提取查询参数：`company_name`、`product_keyword`、`hs_code`、`country`、`trade_type`、`date_from`、`date_to`、`page_index`、`page_size`、排序字段和排序方向。
3. 若用户条件足够，直接调用 MCP 工具 `search_customs_data`。若条件不足，优先从上下文补齐；仍不足时只问一个最关键的问题。
4. 若用户要求“先看样本”“列几条”“找线索”，默认 `page_size` 用 5 到 10。若用户明确要求更多，也不要超过 20。
5. 对返回结果做结构化整理：先说查询条件和总量，再给表格，最后给可行动观察和下一步查询建议。
6. 若需要翻页、缩小范围或扩大范围，说明应该改哪个参数，而不是重复泛泛建议。

## 查询参数规则

至少提供以下四个条件之一：

- `company_name`：企业名称，模糊匹配进口商或出口商。
- `product_keyword`：产品描述关键词，例如 `led`、`valve`、`CABIN`、`brake pad`。
- `hs_code`：HS 编码前缀匹配，例如 `8415`、`870830`。
- `country`：国家/地区，可用中文名、英文名、ISO-2 或 ISO-3，例如 `美国`、`Japan`、`JP`。

贸易方向：

- 用户说“进口”“采购”“买家进口记录”，使用 `trade_type: "import"`。
- 用户说“出口”“供货”“卖家出口记录”，使用 `trade_type: "export"`。
- 用户没有明确方向，使用 `trade_type: "all"`，并在结果里标注进口/出口类型。

日期：

- 用户给年份时，转为全年范围，例如 `2025` 转为 `date_from: "2025-01-01"`、`date_to: "2025-12-31"`。
- 用户给月份时，转为该月第一天到最后一天。
- 用户没有给日期时，不要随便声称“最新”。可以不传日期，或说明“未限定时间范围”。

分页和排序：

- `page_index` 默认 1。
- `page_size` 最大 20；概览用 5 到 10。
- `sort_by` 只能用 `tradedate`、`quantity`、`weight`、`uusd`。
- `sort_order` 只能用 `asc` 或 `desc`。
- 默认按 `tradedate desc` 看最新记录；用户要“金额最大”时用 `uusd desc`。

## 常见用户说法到参数的映射

用户说“查 LED 产品 2025 年美国进口数据前 5 条”：

```json
{
  "product_keyword": "LED",
  "country": "美国",
  "trade_type": "import",
  "date_from": "2025-01-01",
  "date_to": "2025-12-31",
  "page_index": 1,
  "page_size": 5,
  "sort_by": "tradedate",
  "sort_order": "desc"
}
```

用户说“看 IKEA SUPPLY AG 的出口记录”：

```json
{
  "company_name": "IKEA SUPPLY AG",
  "trade_type": "export",
  "page_index": 1,
  "page_size": 10
}
```

用户说“日本 8415 类目进口样本”：

```json
{
  "country": "Japan",
  "hs_code": "8415",
  "trade_type": "import",
  "page_index": 1,
  "page_size": 10
}
```

用户说“找墨西哥刹车片买家”：

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

## 结果解读规范

回答必须让用户看清楚三个层次：

1. 查询口径：说明使用了哪些过滤条件，例如国家、产品关键词、HS、方向、时间、页码、每页条数。
2. 数据结果：优先用表格展示关键字段，不要把大量原始 JSON 直接甩给用户。
3. 业务观察：指出出现频率高的买家/供应商、主要产品描述、金额或重量较大的记录、日期集中度、是否需要翻页继续查。

推荐表格列：

| 列 | 内容 |
| --- | --- |
| 日期 | `贸易日期` |
| 类型 | `贸易类型` |
| HS | `海关编码` |
| 产品 | `产品描述`，过长时压缩 |
| 进口商 | `进口商` |
| 出口商 | `出口商` |
| 数量 | `数量` + `数量单位` |
| 重量 | `重量` |
| 金额 | `金额(USD)` |
| 原产国 | `原产国` |

如果返回分页字段，必须说明：

- `total`：匹配总记录数。
- `page_index`：当前页。
- `page_size`：本页记录数上限。
- `total_pages`：总页数。

## 空结果和异常处理

没有记录时，不要直接说“没有市场”。按以下方式处理：

- 说明当前查询条件过窄或数据源未命中。
- 给一个放宽建议：缩短 HS 编码、去掉日期、扩大国家、换英文/中文关键词。
- 给一个收窄建议：如果结果为 0 但条件很泛，建议换更贴近海关描述的产品词或补 HS 编码。

MCP 工具不可用时：

- 说明当前运行环境没有连接 TOPEASE Customs MCP。
- 给出配置方向：streamable HTTP 使用 `https://mcp.topease.net/mcp`，请求头为 `Authorization: Bearer <TOPEASE_API_KEY>`；stdio 使用 `uvx topease-mcp` 并设置 `TOPEASE_MCP_API_KEY`。
- 不要试图通过普通网页搜索替代 MCP 结果，除非用户明确要求改用公开网页。

鉴权或余额问题：

- 不要泄露、回显或保存 API key。
- 如果报错指向缺少 key、key 无效、余额不足或计费限制，要求用户检查 Tradee/TOPEASE 账号和 MCP key。
- 不要反复重试同一个鉴权失败请求。

## 输出模板

简短查询结果：

```markdown
按以下条件查询：国家=...，产品/HS/企业=...，方向=...，时间=...。返回 total=...，当前第 ... 页。

| 日期 | 类型 | HS | 产品 | 进口商 | 出口商 | 数量 | 重量 | 金额USD | 原产国 |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| ... |

观察：
- ...
- ...

下一步建议：...
```

配置排障回答：

```markdown
这个 skill 需要连接 TOPEASE Customs MCP。当前问题是：...

streamable HTTP 配置：
...

stdio 配置：
...

配置好 API key 后再发起 `search_customs_data` 查询。
```

## 安全和边界

- 不要在最终回答中展示完整 API key、Authorization header、secret 或 token。
- 不要承诺数据覆盖绝对完整；称为“本次 MCP 返回的海关记录”。
- 不要把海关记录直接解释为客户意向或采购需求；只能说“可作为潜在线索，需要进一步核验”。
- 不要把单页样本总结成全市场份额，除非用户明确要求抽样观察并接受限制。
- 对金额、数量、重量保持原单位和原字段口径，不要未经说明做汇率或单位换算。

## 参考资料

读取 `references/api-reference.md` 获取：

- MCP streamable HTTP 和 stdio 配置示例。
- `search_customs_data` 完整参数表。
- 返回字段说明。
- 常见鉴权、空结果、结果过多的排障建议。

读取 `references/getting-started.md` 获取：

- skill 广场/GitHub 发布时的上手说明。
- 一键调用该 skill 需要满足的运行环境条件。
- Tradee 注册、进入 MCP 服务页、创建并保存 MCP API key 的步骤。
- 手动配置 MCP 客户端和排障清单。

运行 `scripts/generate_mcp_config.py` 可生成 MCP 客户端配置片段：

```bash
python scripts/generate_mcp_config.py --mode streamable-http
python scripts/generate_mcp_config.py --mode stdio
```
