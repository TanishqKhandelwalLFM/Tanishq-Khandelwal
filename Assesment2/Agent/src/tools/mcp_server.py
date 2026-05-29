from mcp.server.fastmcp import FastMCP

from src.tools.calculator import calculator

mcp = FastMCP("CalculatorServer")


@mcp.tool()
def calculate(a: float, b: float, operation: str):
    return calculator(a, b, operation)


if __name__ == "__main__":
    mcp.run()