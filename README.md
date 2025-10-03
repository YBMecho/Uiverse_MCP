# Uiverse MCP Tool

<p align="center">English | <a href="README_zh.md">中文</a>

A FastMCP-based code extraction tool for [Uiverse.io](https://uiverse.io/), supporting component code extraction from Uiverse website for various frontend frameworks.

## Features

- 🎨 Support for multiple frontend framework code extraction
- 🚀 Built on FastMCP, supporting both stdio and SSE transport methods
- 🔧 Easy integration with AI workflows
- 📦 Uses Playwright for web content extraction

## Supported Frameworks

- HTML/CSS
- React
- Vue
- Svelte
- Lit

## System Requirements

- Python >= 3.12
- uv package manager

## Installation

### 1. Clone or download the project

```bash
git clone https://github.com/YBMecho/Uiverse_MCP.git
cd Uiverse_MPC
```

### 2. Install dependencies

Using uv to install dependencies:

```bash
uv sync
```

### 3. Install Playwright browsers

```bash
uv run playwright install
```

## Configuration

This tool supports two MCP configuration methods: **stdio** and **SSE**. Please add one of the following configurations to your MCP configuration file (such as Cursor's `mcp.json`).

### Method 1: stdio configuration (recommended)

```json
{
  "mcpServers": {
    "uiverse-MCP-tool-stdio": {
      "name": "Uiverse MCP Tool",
      "type": "stdio",
      "description": "Uiverse MCP Tool",
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

**Note**: Please replace `D:\\YBMecho\\Desktop\\Uiverse_MPC` with your actual project path.

### Method 2: SSE configuration

```json
{
  "mcpServers": {
    "uiverse-MPC-tool-SSE": {
      "name": "Uiverse MCP Tool",
      "type": "sse",
      "description": "Uiverse MCP Tool",
      "isActive": true,
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**Note**: An HTTP server must be started before using the SSE method.

## Usage

### Available Tools

#### 1. `parse_and_extract`

Extract component code from Uiverse links.

**Input format**: `<framework> <link>`

**Examples**:

```
HTML https://uiverse.io/Na3ar-17/evil-dragon-24
React https://uiverse.io/username/component-name
Vue https://uiverse.io/username/component-name
Svelte https://uiverse.io/username/component-name
Lit https://uiverse.io/username/component-name
```

**Usage rules**:
- Links must start with `https://uiverse.io/`
- Links must contain a specific component path (not just the domain)
- Framework names are case-insensitive

#### 2. `list_supported_frameworks`

List all currently supported frameworks.

**Returns**: List of supported frameworks (Markdown format)

### Using with AI Assistants

After configuration, you can use it directly in MCP-supporting AI assistants (like Cursor):

```
Please extract HTML code from https://uiverse.io/Na3ar-17/evil-dragon-24
```

or

```
Use React framework to extract code from https://uiverse.io/username/component-name
```

The AI assistant will automatically call the `parse_and_extract` tool to retrieve the code.

## Project Structure

```
Uiverse_MPC/
├── app.py                  # FastMCP main application
├── browser.py              # HTML/CSS extractor
├── browser_React.py        # React extractor
├── browser_Vue.py          # Vue extractor
├── browser_Svelte.py       # Svelte extractor
├── browser_Lit.py          # Lit extractor
├── pyproject.toml          # Project configuration
├── build_exe.spec          # PyInstaller configuration
├── dist/                   # Executable output directory
│   └── UiverseExtractor.exe
└── README.md
```

## Building Executable

The project includes PyInstaller configuration to build a standalone Windows executable:

```bash
pyinstaller build_exe.spec
```

The generated `UiverseExtractor.exe` will be located in the `dist/` directory.

## Dependencies

- `mcp[cli]` >= 1.16.0 - MCP protocol support
- `fastmcp` >= 2.0.0 - FastMCP framework
- `playwright` >= 1.55.0 - Browser automation

## Development Notes

### Local Running

Run in stdio mode:

```bash
uv run app.py
```

### Adding Support for New Frameworks

1. Create a new `browser_<Framework>.py` file
2. Implement the `extract_<framework>_code(url: str) -> str` async function
3. Import and add it to the `_dispatch_extract` function in `app.py`
4. Update the `SUPPORTED_FRAMEWORKS` list

## License

Please add the appropriate license information according to your needs.

## Contributions

Issues and Pull Requests are welcome!

## Contact

For questions or suggestions, please provide feedback through Issues.