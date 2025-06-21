# Statistics MCP Server for Langflow

## Solution Concept

With Vibe coding it is easy to lose the track how adequate is your code and miss some useless artefacts inside the code. That is as well good when there is some external assessment, which is in our case TurinTech, which can provide to code assistant some metrics. Ideally it can be done as Langflow MCP and integrated into Claude code for example. As well as Mistral models can be used overall for any inferences.

An MCP (Model Context Protocol) server that provides statistics capabilities for Langflow and other AI assistants.


## Features

- Take statistics of the current workscreen
- Return statistics as base64-encoded images  
- Save statistics to file paths
- Support for PNG and JPEG formats
- FastMCP implementation for better performance
- Resource endpoints for direct access

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create `.env` file):
```bash

```

## Usage

### MCP Server

Run the MCP server:
```bash
python statistics_mcp_server.py
```

The server provides these tools:
- `take_statistics(format)`: Captures screen and returns base64 data URL
- `save_statistics(file_path, format)`: Saves statistics to specified file path  
- `get_statistics_info()`: Returns server information and capabilities

Resources available:
- `statistics://current`: Current statistics as base64
- `statistics://info`: Server information

### Langflow Integration

1. **Using MCP Server**: Configure Langflow to connect to the MCP server using the provided `configs/mcp_configs.json`

2. **Using Custom Component**: Copy `langflow_statistics_component.py` to your Langflow custom components directory

## Configuration

### For Langflow MCP Integration
```json
{
  "mcpServers": {
    "statistics": {
      "command": "python",
      "args": ["statistics_mcp_server.py"],
      "env": {},
      "description": "Statistics capture server for Langflow"
    }
  }
}
```

### For Claude Desktop
```json
{
  "mcpServers": {
    "statistics": {
      "command": "python",
      "args": ["/path/to/statistics_mcp_server.py"]
    }
  }
}
```

## Deploy Instructions

1. Load `configs/langflow_chart.json` into Langflow and configure it as an MCP server
2. Set your desired git repository in the git MCP configuration
3. Build and run `statistics_mcp_server.py` using uv:
   ```bash
   uv run statistics_mcp_server.py
   ```
4. Connect the resulting MCP to MCP Servers

## Example Usage in Langflow

1. Add the statistics MCP server to your Langflow configuration
2. Use the `take_statistics` tool in your flows to capture screens
3. Process the returned base64 image data in subsequent components
4. Combine with vision models for screen analysis workflows