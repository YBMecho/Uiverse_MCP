# Uiverse MCP 工具

<p align="center"><a href="README.md">English </a>| 中文

一个基于 Model Context Protocol (MCP) 的工具，用于自动提取 [Uiverse.io](https://uiverse.io/) 网站上的 UI 组件代码。支持多种前端框架，包括 HTML/CSS、React、Vue、Svelte 和 Lit。

## 🌟 功能特性

- **多框架支持**: 支持 HTML、React、Vue、Svelte、Lit 五种框架
- **自动化提取**: 使用 Playwright 自动化浏览器操作，模拟用户点击和复制
- **智能识别**: 自动识别并切换到对应的框架代码视图
- **Markdown 输出**: 返回格式化的 Markdown 代码块，便于阅读和使用
- **MCP 集成**: 完全兼容 MCP 协议，可在 Cursor、Claude Desktop 等支持 MCP 的客户端中使用

## 📦 安装

1. 克隆项目：
```bash
git clone https://github.com/YBMecho/Uiverse_MCP.git
cd Uiverse_MPC
```

2. 安装依赖：
```bash
uv sync
```

3. 安装 Playwright 浏览器：
```bash
uv run playwright install chromium
```

4.如果不行就解压`uiverse_MPC.zip`运行。

## ⚙️ 配置

### Cursor 配置 (mcp.json)

在 Cursor 设置中添加以下 MCP 服务器配置：

```json
{
  "mcpServers": {
    "uiverse的MCP工具": {
      "name": "uiverse的MCP工具",
      "type": "stdio",
      "description": "uiverse的MCP工具",
      "isActive": true,
      "command": "UV",
      "args": [
        "--directory",
        "D:\\desktop\\uiverse_MPC",
        "run",
        "app.py"
      ]
    }
  }
}
```

### Claude Desktop 配置

在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "uiverse-extractor": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/uiverse_MPC",
        "run",
        "app.py"
      ]
    }
  }
}
```

> **注意**: 请将路径 `/path/to/uiverse_MPC` 替换为项目的实际路径。

## 🚀 使用方法

### 可用工具

1. **parse_and_extract**: 解析并提取组件代码
2. **list_supported_frameworks**: 列出支持的框架

### 使用格式

```
<框架名称> <Uiverse链接>
```

### 支持的框架

- `HTML` - 提取 HTML 和 CSS 代码
- `React` - 提取 React 组件代码（包含说明内容）
- `Vue` - 提取 Vue 组件代码
- `Svelte` - 提取 Svelte 组件代码
- `Lit` - 提取 Lit Element 组件代码

### 使用示例

#### 1. 提取 HTML/CSS 代码
```
HTML https://uiverse.io/Na3ar-17/evil-dragon-24
```

#### 2. 提取 React 代码
```
React https://uiverse.io/Codecite/angry-bullfrog-58
```

#### 3. 提取 Vue 代码
```
Vue https://uiverse.io/Codecite/angry-bullfrog-58
```

#### 4. 列出支持的框架
直接调用 `list_supported_frameworks` 工具。

## 📋 输出格式

工具返回单行 Markdown 格式，包含框架名称和代码块：

- **HTML**: `### HTML ```html <代码> ``` ### CSS ```css <代码> ````
- **React**: `### 内容 <说明内容> ### React ```tsx <代码> ````
- **Vue**: `### Vue ```vue <代码> ````
- **Svelte**: `### Svelte ```svelte <代码> ````
- **Lit**: `### Lit ```ts <代码> ````

## 🔧 技术栈

- **Python 3.11+**
- **Playwright**: 自动化浏览器操作
- **FastMCP**: MCP 服务器框架
- **UV**: Python 包管理工具

## 📝 注意事项

1. **链接格式**: 必须是 `https://uiverse.io/` 开头的完整链接
2. **网络要求**: 需要稳定的网络连接访问 Uiverse.io
3. **浏览器权限**: 工具需要剪贴板读写权限来获取复制的代码
4. **框架大小写**: 框架名称不区分大小写（html、HTML、Html 都可以）

## 🔍 工作原理

1. 解析用户输入的框架和链接
2. 启动 Playwright 无头浏览器
3. 访问指定的 Uiverse 链接
4. 根据框架类型选择对应的代码视图
5. 模拟点击复制按钮
6. 等待复制完成（"✔" 图标出现）
7. 从剪贴板读取代码内容
8. 格式化为 Markdown 并返回

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具！

## 📄 许可证

MIT License
