# Uiverse MCP Tool

<p align="center">English | <a href="README.zh.md">中文</a>

A tool based on Model Context Protocol (MCP) for automatically extracting UI component code from the [Uiverse.io](https://uiverse.io/) website. Supports multiple frontend frameworks, including HTML/CSS, React, Vue, Svelte, and Lit.

## 🌟 Features

- **Multi-framework support**: Supports five frameworks: HTML, React, Vue, Svelte, Lit
- **Automated extraction**: Uses Playwright for automated browser operations, simulating user clicks and copying
- **Smart recognition**: Automatically identifies and switches to the corresponding framework code view
- **Markdown output**: Returns formatted Markdown code blocks for easy reading and use
- **MCP integration**: Fully compatible with MCP protocol, can be used in MCP-supported clients like Cursor and Claude Desktop

## 📦 Installation

1. Clone the project:
```bash
git clone https://github.com/YBMecho/Uiverse_MCP.git
cd Uiverse_MPC
```

2. Install dependencies:
```bash
uv sync
```

3. Install Playwright browser:
```bash
uv run playwright install chromium
```

4. If it doesn't work, unzip `uiverse_MPC.zip` and run.

## ⚙️ Configuration

### Cursor Configuration (mcp.json)

Add the following MCP server configuration in Cursor settings:

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

### Claude Desktop Configuration

Add to Claude Desktop configuration file:

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

> **Note**: Replace the path `/path/to/uiverse_MPC` with the actual project path.

## 🚀 Usage

### Available Tools

1. **parse_and_extract**: Parse and extract component code
2. **list_supported_frameworks**: List supported frameworks

### Usage Format

```
<Framework name> <Uiverse link>
```

### Supported Frameworks

- `HTML` - Extract HTML and CSS code
- `React` - Extract React component code (includes description content)
- `Vue` - Extract Vue component code
- `Svelte` - Extract Svelte component code
- `Lit` - Extract Lit Element component code

### Usage Examples

#### 1. Extract HTML/CSS code
```
HTML https://uiverse.io/Na3ar-17/evil-dragon-24
```

#### 2. Extract React code
```
React https://uiverse.io/Codecite/angry-bullfrog-58
```

#### 3. Extract Vue code
```
Vue https://uiverse.io/Codecite/angry-bullfrog-58
```

#### 4. List supported frameworks
Directly call the `list_supported_frameworks` tool.

## 📋 Output Format

The tool returns single-line Markdown format, including framework name and code blocks:

- **HTML**: `### HTML ```html <code> ``` ### CSS ```css <code> ````
- **React**: `### Content <description content> ### React ```tsx <code> ````
- **Vue**: `### Vue ```vue <code> ````
- **Svelte**: `### Svelte ```svelte <code> ````
- **Lit**: `### Lit ```ts <code> ````

## 🔧 Tech Stack

- **Python 3.11+**
- **Playwright**: Automated browser operations
- **FastMCP**: MCP server framework
- **UV**: Python package management tool

## 📝 Notes

1. **Link format**: Must be a complete link starting with `https://uiverse.io/`
2. **Network requirements**: Requires stable internet connection to access Uiverse.io
3. **Browser permissions**: Tool needs clipboard read/write permissions to get copied code
4. **Framework case sensitivity**: Framework names are case-insensitive (html, HTML, Html are all acceptable)

## 🔍 How It Works

1. Parse user-input framework and link
2. Launch Playwright headless browser
3. Access the specified Uiverse link
4. Select the corresponding code view based on framework type
5. Simulate clicking the copy button
6. Wait for copy completion ("✔" icon appears)
7. Read code content from clipboard
8. Format into Markdown and return

## 🤝 Contribution

Welcome to submit Issues and Pull Requests to improve this tool!

## 📄 License

MIT License