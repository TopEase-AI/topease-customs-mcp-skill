#!/usr/bin/env python3
"""Generate MCP client configuration snippets for TOPEASE Customs MCP."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def build_config(mode: str, api_key: str, server_name: str) -> dict[str, Any]:
    if mode == "streamable-http":
        server = {
            "type": "streamableHttp",
            "url": "https://mcp.topease.net/mcp",
            "headers": {"Authorization": f"Bearer {api_key}"},
        }
    elif mode == "stdio":
        server = {
            "command": "uvx",
            "args": ["topease-mcp"],
            "env": {"TOPEASE_MCP_API_KEY": api_key},
        }
    else:
        raise ValueError(f"unsupported mode: {mode}")

    return {"mcpServers": {server_name: server}}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a TOPEASE Customs MCP client config JSON snippet."
    )
    parser.add_argument(
        "--mode",
        choices=["streamable-http", "stdio"],
        default="streamable-http",
        help="MCP transport mode to generate.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("TOPEASE_MCP_API_KEY") or "<TOPEASE_API_KEY>",
        help="API key to place in the snippet. Defaults to env TOPEASE_MCP_API_KEY or a placeholder.",
    )
    parser.add_argument(
        "--server-name",
        default="topease-customs-data",
        help="MCP server name in the generated config.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path. If omitted, prints JSON to stdout.",
    )
    args = parser.parse_args()

    config = build_config(args.mode, args.api_key, args.server_name)
    text = json.dumps(config, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
