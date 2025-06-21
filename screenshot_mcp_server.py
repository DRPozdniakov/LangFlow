#!/usr/bin/env python3
"""
FastMCP Screenshot Server for Langflow Integration
"""

import base64
import io
import logging
import os
from typing import Optional

from PIL import ImageGrab
from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("screenshot_server")

# Store latest screenshot
latest_screenshot_data = None

@mcp.resource("screenshot://latest")
async def get_latest_screenshot():
    """Get the latest screenshot as binary data via MCP resource."""
    global latest_screenshot_data
    if latest_screenshot_data is None:
        raise Exception("No screenshot available. Take a screenshot first.")
    return latest_screenshot_data

@mcp.tool()
async def take_screenshot(format: str = "png") -> str:
    """Take a screenshot and store it as a resource. Access via screenshot://latest

    Args:
        format: Image format for the screenshot (png or jpeg)
    """
    global latest_screenshot_data
    try:
        # Validate format
        format_type = format.upper()
        if format_type not in ["PNG", "JPEG", "JPG"]:
            format_type = "PNG"
        
        if format_type == "JPG":
            format_type = "JPEG"
        
        logger.info(f"Taking screenshot in {format_type} format")
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Convert to bytes and store
        img_buffer = io.BytesIO()
        screenshot.save(img_buffer, format=format_type)
        latest_screenshot_data = img_buffer.getvalue()
        
        width, height = screenshot.size
        size_kb = len(latest_screenshot_data) / 1024
        
        logger.info(f"Screenshot captured successfully: {width}x{height}, {size_kb:.1f}KB")
        return f"Screenshot taken ({width}x{height}, {size_kb:.1f}KB). Access via resource: screenshot://latest"
        
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        raise Exception(f"Failed to capture screenshot: {str(e)}")

@mcp.tool()
async def save_screenshot(file_path: str, format: str = "png") -> str:
    """Take a screenshot and save it to a file path.

    Args:
        file_path: Path where to save the screenshot
        format: Image format for the screenshot (png or jpeg)
    """
    try:
        # Validate format
        format_type = format.upper()
        if format_type not in ["PNG", "JPEG", "JPG"]:
            format_type = "PNG"
        
        if format_type == "JPG":
            format_type = "JPEG"
        
        full_path = os.path.join(os.getcwd(), "data", file_path)
        logger.info(f"Taking screenshot and saving to {full_path} in {format_type} format")
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Save to file
        screenshot.save(file_path, format=format_type)
        
        logger.info(f"Screenshot saved successfully to {file_path}")
        return f"Screenshot saved to {file_path}"
        
    except Exception as e:
        logger.error(f"Error saving screenshot: {e}")
        raise Exception(f"Failed to save screenshot: {str(e)}")

@mcp.tool()
async def get_screenshot_info() -> dict:
    """Get information about screenshot capabilities.

    Returns:
        Dictionary with screenshot server information
    """
    try:
        # Take a test screenshot to get dimensions
        screenshot = ImageGrab.grab()
        width, height = screenshot.size
        
        return {
            "server_name": "screenshot_server",
            "supported_formats": ["png", "jpeg"],
            "screen_resolution": f"{width}x{height}",
            "status": "ready"
        }
        
    except Exception as e:
        logger.error(f"Error getting screenshot info: {e}")
        return {
            "server_name": "screenshot_server",
            "supported_formats": ["png", "jpeg"],
            "screen_resolution": "unknown",
            "status": "error",
            "error": str(e)
        }

def main():
    """Main entry point for the server."""
    logger.info("Starting Screenshot MCP Server")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()