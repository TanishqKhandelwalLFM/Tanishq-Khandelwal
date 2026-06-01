from fastmcp import FastMCP 

mcp = FastMCP()


@mcp.tool()
def fetch() : 
    ''' use this tool to fetch data '''
    return {"message" : 'hello'}

@mcp.tool()
def process(path : str):
    ''' use this tool to process data '''
    return {'data' : 'processed data'}



if __name__ == '__main__' :
    mcp.run(transport='streamable-http' , host="0.0.0.0" ,port = 8050)


