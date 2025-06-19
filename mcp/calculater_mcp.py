# calculator_mcp_server_streamablehttp.py (Simplified run for Uvicorn defaults)
from mcp.server.fastmcp import FastMCP

# 1. Create an MCP server instance
mcp = FastMCP(
    name="CalculatorStreamableHttpServer",
    description="An MCP server using Streamable HTTP, providing basic arithmetic calculation tools.",
    stateless_http=True
)

# ... (TOOL DEFINITIONS - add, subtract, multiply, divide - same as before) ...
@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Adds two numbers together.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    """
    print(f"[Server Log StreamHTTP] Tool 'add' called with a={a}, b={b}")
    result = a + b
    print(f"[Server Log StreamHTTP] Tool 'add' result: {result}")
    return result
@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    Subtracts the second number from the first number.

    Args:
        a (float): The number to subtract from.
        b (float): The number to subtract.

    Returns:
        float: The result of a minus b.
    """
    print(f"[Server Log StreamHTTP] Tool 'subtract' called with a={a}, b={b}")
    result = a - b
    print(f"[Server Log StreamHTTP] Tool 'subtract' result: {result}")
    return result
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    print(f"[Server Log StreamHTTP] Tool 'multiply' called with a={a}, b={b}")
    result = a * b
    print(f"[Server Log StreamHTTP] Tool 'multiply' result: {result}")
    return result
@mcp.tool()
def divide(numerator: float, denominator: float) -> float | str:
    """
    Divides the numerator by the denominator.

    Args:
        numerator (float): The number to be divided.
        denominator (float): The number to divide by.

    Returns:
        float: The result of the division if denominator is not zero.
        str: An error message if denominator is zero.
    """
    print(f"[Server Log StreamHTTP] Tool 'divide' called with numerator={numerator}, denominator={denominator}")
    if denominator == 0:
        print("[Server Log StreamHTTP] Tool 'divide' error: Division by zero.")
        return "Error: Cannot divide by zero."
    result = numerator / denominator
    print(f"[Server Log StreamHTTP] Tool 'divide' result: {result}")
    return result

if __name__ == "__main__":
    print(f"Starting CalculatorStreamableHttpServer (FastMCP application defined).")
    print(f"When run with 'mcp run calculator_mcp_server_streamablehttp.py --transport streamable-http',")
    print(f"it will likely use Uvicorn's default host/port (e.g., 127.0.0.1:8000) or PORT/HOST env vars.")
    mcp.run(transport="streamable-http")