# Uiverse MCP 工具

<p align="center"><a href="README.md">English </a>| 中文

一个基于 FastMCP 的 [Uiverse.io](https://uiverse.io/) 代码提取工具，支持从 Uiverse 网站提取多种前端框架的组件代码。

## 功能特性

- 🎨 支持多种前端框架的代码提取
- 🚀 基于 FastMCP 构建，支持 stdio 和 SSE 两种传输方式
- 🔧 易于集成到 AI 工作流中
- 📦 使用 Playwright 进行网页内容提取

## 支持的框架

- HTML/CSS
- React
- Vue
- Svelte
- Lit

## 系统要求

- Python >= 3.12
- uv 包管理器

## 安装

### 1. 克隆或下载项目

```bash
git clone https://github.com/YBMecho/Uiverse_MCP.git
cd Uiverse_MPC
```

### 2. 安装依赖

使用 uv 安装依赖：

```bash
uv sync
```

### 3. 安装 Playwright 浏览器

```bash
uv run playwright install
```

## 配置

该工具支持两种 MCP 配置方式：**stdio** 和 **SSE**。请在你的 MCP 配置文件（如 Cursor 的 `mcp.json`）中添加以下配置之一。

### 方式一：stdio 配置（推荐）

```json
{
  "mcpServers": {
    "uiverse的MCP工具-stdio": {
      "name": "uiverse的MCP工具",
      "type": "stdio",
      "description": "uiverse的MCP工具",
      "isActive": true,
      "command": "uv",
      "args": [
        "--directory",
        "D:\\YBMecho\\Desktop\\Uiverse_MPC",
        "run",
        "app.py"
      ]
    }
  }
}
```

**注意**：请将 `D:\\YBMecho\\Desktop\\Uiverse_MPC` 替换为你的项目实际路径。

### 方式二：SSE 配置

```json
{
  "mcpServers": {
    "uiverse的MPC工具-SSE": {
      "name": "uiverse的MCP工具",
      "type": "sse",
      "description": "uiverse的MPC工具",
      "isActive": true,
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**注意**：使用 SSE 方式前需要先启动 HTTP 服务器。

## 使用方法

### 可用工具

#### 1. `parse_and_extract`

从 Uiverse 链接提取组件代码。

**输入格式**：`<框架> <链接>`

**示例**：

```
HTML https://uiverse.io/Na3ar-17/evil-dragon-24
React https://uiverse.io/username/component-name
Vue https://uiverse.io/username/component-name
Svelte https://uiverse.io/username/component-name
Lit https://uiverse.io/username/component-name
```

**使用规则**：
- 链接必须以 `https://uiverse.io/` 开头
- 链接必须包含具体的组件路径（不能只是域名）
- 框架名称不区分大小写

#### 2. `list_supported_frameworks`

列出当前支持的所有框架。

**返回**：支持的框架列表（Markdown 格式）

### 在 AI 助手中使用

配置完成后，你可以在支持 MCP 的 AI 助手（如 Cursor）中直接使用：

```
请帮我从 https://uiverse.io/Na3ar-17/evil-dragon-24 提取 HTML 代码
```

或

```
使用 React 框架提取 https://uiverse.io/username/component-name 的代码
```

AI 助手会自动调用 `parse_and_extract` 工具来获取代码。

## 项目结构

```
Uiverse_MPC/
├── app.py                  # FastMCP 主应用
├── browser.py              # HTML/CSS 提取器
├── browser_React.py        # React 提取器
├── browser_Vue.py          # Vue 提取器
├── browser_Svelte.py       # Svelte 提取器
├── browser_Lit.py          # Lit 提取器
├── pyproject.toml          # 项目配置
├── build_exe.spec          # PyInstaller 配置
├── dist/                   # 可执行文件输出目录
│   └── UiverseExtractor.exe
└── README.md
```

## 构建可执行文件

项目包含 PyInstaller 配置，可以构建为独立的 Windows 可执行文件：

```bash
pyinstaller build_exe.spec
```

生成的 `UiverseExtractor.exe` 将位于 `dist/` 目录。

## 依赖项

- `mcp[cli]` >= 1.16.0 - MCP 协议支持
- `fastmcp` >= 2.0.0 - FastMCP 框架
- `playwright` >= 1.55.0 - 浏览器自动化

## 开发说明

### 本地运行

使用 stdio 模式运行：

```bash
uv run app.py
```

### 添加新框架支持

1. 创建新的 `browser_<Framework>.py` 文件
2. 实现 `extract_<framework>_code(url: str) -> str` 异步函数
3. 在 `app.py` 中导入并添加到 `_dispatch_extract` 函数
4. 更新 `SUPPORTED_FRAMEWORKS` 列表

## 许可证

请根据你的需求添加相应的许可证信息。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 Issue 反馈。

