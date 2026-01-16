import asyncio
from fastmcp import Client

client = Client("http://localhost:8704/mcp")

import json

from tqdm import tqdm

async def list_devices():
    """List all connected devices and return the device list"""
    async with client:
        result = await client.call_tool("list_connected_devices", {})
        # Extract the actual device list from the CallToolResult object
        devices = result.data if hasattr(result, 'data') else result
        print("Connected devices:", devices)
        return devices

async def ask_agent(device_id: str, task: str, max_steps: int = 20):
    """
    Ask the agent to perform a task on the specified device.
    
    Args:
        device_id: ID of the device (get from list_devices)
        task: The task description
        max_steps: Maximum number of steps (default: 20)
    """
    async with client:
        result = await client.call_tool("ask_agent", {
            "device_id": device_id,
            "task": task,
            "max_steps": max_steps
        })
        print("\n=== Task Execution Result ===")
        # Extract the actual data from CallToolResult
        result_data = result.data if hasattr(result, 'data') else result
        print(json.dumps(result_data, indent=4, ensure_ascii=False))
        return result_data


async def async_list_tools():
    """List all available tools from the MCP server"""
    async with client:
        tools = await client.list_tools()
        # Convert Tool objects to dictionaries for JSON serialization
        tools_dict = [tool.model_dump() if hasattr(tool, 'model_dump') else tool.__dict__ for tool in tools]
        print("Supported tools:\n", json.dumps(tools_dict, indent=4, ensure_ascii=False))


async def main():
    """Main function to demonstrate the workflow"""
    # Step 1: List available tools
    print("=== Step 1: Listing available tools ===")
    await async_list_tools()
    
    # Step 2: List connected devices
    print("\n=== Step 2: Listing connected devices ===")
    devices = await list_devices()
    
    if not devices:
        print("No devices connected! Please connect a device and try again.")
        return
    
    # Step 3: Execute task on the first device
    device_id = devices[0]
    print(f"\n=== Step 3: Executing task on device {device_id} ===")
    task = "打开淘宝，搜索苹果手机，加进购物车"
    await ask_agent(device_id=device_id, task=task, max_steps=30)


if __name__ == "__main__":
    asyncio.run(main())
