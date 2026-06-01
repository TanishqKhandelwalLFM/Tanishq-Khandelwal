import os
from mcp.client.stdio import stdio_client
from mcp import ClientSession , StdioServerParameters , client
import asyncio

mcp_server_Script = os.path.join((os.path.dirname(os.path.abspath(__file__))),'stdio_mcp.py')
print(mcp_server_Script)

server_parameters = StdioServerParameters(
    command = 'python',
    args = [str(mcp_server_Script)],
    env = {}
)


async def main():
    async with stdio_client(server_parameters) as (read,write) : 
        async with ClientSession(read,write) as session :
             
            await session.initialize()

            tools = await session.list_tools()

            result = await session.call_tool('process' , arguments = {'path' : '/path/to/data'})
            print(result)


if __name__ == "__main__":
    asyncio.run(main())

