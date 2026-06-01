from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os


async def main() : 
    client = MultiServerMCPClient(
        {
            'data_fetch_mcp_stdio' : {
                'transport' : 'stdio',
                'command' : 'uvx',
                'args' : ['duckduckgo-mcp-server']
            }
        }
    )

    tools = await client.get_tools()

    search_tool = tools[0]

    res = await search_tool.ainvoke({'query' : 'what is the largest state of india by land'})
    print(res)

if __name__ == "__main__":
    asyncio.run(main())