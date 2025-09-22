"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
import asyncio
import re
from typing import Dict, Any

# 导入各提取函数
from browser import extract_html_css
from browser_React import extract_react_code
from browser_Vue import extract_vue_code
from browser_Svelte import extract_svelte_code
from browser_Lit import extract_lit_code

mcp = FastMCP("UiverseExtractor")

UIVERSE_PREFIX = "https://uiverse.io/"
SUPPORTED_FRAMEWORKS = ["HTML", "React", "Vue", "Svelte", "Lit"]


def _is_valid_uiverse_link(url: str) -> bool:
    return isinstance(url, str) and url.startswith(UIVERSE_PREFIX)


def _has_path_after_prefix(url: str) -> bool:
    return _is_valid_uiverse_link(url) and len(url) > len(UIVERSE_PREFIX)


async def _dispatch_extract(framework: str, url: str) -> str:
    fw = framework.strip().lower()
    if fw == "html":
        return await extract_html_css(url)
    if fw == "react":
        return await extract_react_code(url)
    if fw == "vue":
        return await extract_vue_code(url)
    if fw == "svelte":
        return await extract_svelte_code(url)
    if fw == "lit":
        return await extract_lit_code(url)
    raise ValueError(f"不支持的框架: {framework}")


@mcp.tool()
async def parse_and_extract(query: str) -> str:
    """
    规则：输入格式为 “框架+空格+链接”，例如：
    HTML https://uiverse.io/Na3ar-17/evil-dragon-24

    AI 调用信息：
    如果用户输入的链接的开头是 “https://uiverse.io/”，那么先识别该前缀后面是否有内容：
    - 没有内容：不使用 MCP（此处返回说明）
    - 有内容：根据‘框架’选择对应的 MCP 实现提取代码
    """
    if not query or not isinstance(query, str):
        raise ValueError("输入不能为空，格式应为：<框架> <链接>")

    parts = query.strip().split(maxsplit=1)
    if len(parts) != 2:
        raise ValueError("格式错误，应为：<框架> <链接>")

    framework, url = parts[0], parts[1]

    if not _is_valid_uiverse_link(url):
        raise ValueError("链接必须以 https://uiverse.io/ 开头")

    if not _has_path_after_prefix(url):
        # 不使用 MCP 的分支：直接返回说明
        return "> 链接没有指定组件路径，不执行提取。"

    # 调度到具体实现（直接 await，避免在已运行的事件循环中再次调用 asyncio.run）
    md = await _dispatch_extract(framework, url)
    # 再次兜底清洗，移除输出中的 \r 与 \n
    return md.replace("\r", " ").replace("\n", " ")


@mcp.tool()
def list_supported_frameworks() -> str:
    """列出当前支持的框架名称列表（Markdown）。"""
    items = " ".join(f"- {name}" for name in SUPPORTED_FRAMEWORKS)
    return f"### 支持的框架 {items}"


if __name__ == "__main__":
    mcp.run(transport="stdio")