# Screenshot MCP Server for Langflow

An MCP (Model Context Protocol) server that provides screenshot capabilities for Langflow and other AI assistants.

## Features

- Take screenshots of the current workscreen
- Return screenshots as base64-encoded images  
- Save screenshots to file paths
- Support for PNG and JPEG formats
- FastMCP implementation for better performance
- Resource endpoints for direct access

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### MCP Server

Run the MCP server:
```bash
python screenshot_mcp_server.py
```

The server provides these tools:
- `take_screenshot(format)`: Captures screen and returns base64 data URL
- `save_screenshot(file_path, format)`: Saves screenshot to specified file path  
- `get_screenshot_info()`: Returns server information and capabilities

Resources available:
- `screenshot://current`: Current screenshot as base64
- `screenshot://info`: Server information

### Langflow Integration

1. **Using MCP Server**: Configure Langflow to connect to the MCP server using the provided `langflow_config.json`

2. **Using Custom Component**: Copy `langflow_screenshot_component.py` to your Langflow custom components directory

## Configuration

### For Langflow MCP Integration
```json
{
  "mcpServers": {
    "screenshot": {
      "command": "python",
      "args": ["screenshot_mcp_server.py"],
      "env": {},
      "description": "Screenshot capture server for Langflow"
    }
  }
}
```

### For Claude Desktop
```json
{
  "mcpServers": {
    "screenshot": {
      "command": "python",
      "args": ["/path/to/screenshot_mcp_server.py"]
    }
  }
}
```

## Example Usage in Langflow

1. Add the screenshot MCP server to your Langflow configuration
2. Use the `take_screenshot` tool in your flows to capture screens
3. Process the returned base64 image data in subsequent components
4. Combine with vision models for screen analysis workflows