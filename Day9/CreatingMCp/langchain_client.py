from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def main() : 
    client = MultiServerMCPClient(
        {
            'data_fetch_mcp_stdio' : {
                'transport' : 'stdio',
                'command' : 'python',
                'args' : ['/workspaces/Second/CreateingMCP/stdio_mcp.py']
            }
        }
    )

    tools = await client.get_tools()
    print(tools)

if __name__ == "__main__":
    asyncio.run(main())