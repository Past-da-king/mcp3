# calculator_mcp_server_streamablehttp.py (Refactored to import tools)
import logging
from mcp.server.fastmcp import FastMCP

# Configure basic logging
# This is important for the MCP server itself and if any direct logging is needed in this file.
# Tool modules will have their own loggers but might inherit this config if not separately configured.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__) # Logger for this specific file

# 1. Create an MCP server instance
# This instance is used by the tool decorators in the submodules.
mcp = FastMCP(
    name="CalculatorStreamableHttpServer",
    description="An MCP server using Streamable HTTP, providing a comprehensive suite of calculation tools.",
    stateless_http=True
)

# 2. Import tools from their respective modules
# The act of importing these modules will execute the @mcp.tool() decorators within them,
# registering the tools with the 'mcp' instance defined above.

logger.info("Importing calculation tools...")
try:
    from .tools.arithmetic import add, subtract, multiply, divide
    from .tools.advanced_math import power, sqrt, get_constant
    from .tools.trigonometry import sin, cos, tan, asin_op, acos_op, atan_op
    from .tools.calculus import differentiate, integrate_indefinite
    from .tools.plotting import plot_expression # This also initializes PLOT_DIR from plotting.py
    logger.info("All calculation tools imported successfully.")
except ImportError as e:
    logger.error(f"Error importing tools: {e}. Ensure all tool modules and __init__.py files are correct.")
    # Depending on desired behavior, might raise the error or exit
    raise e


# No tool function definitions directly in this file anymore.
# They are now in their respective modules in the 'tools' subdirectory.

# The PLOT_DIR definition and os.makedirs for it have been moved to mcp/tools/plotting.py
# Imports like math, sympy, os, datetime, matplotlib, numpy are now in their respective tool modules.

if __name__ == "__main__":
    print(f"Starting CalculatorStreamableHttpServer (FastMCP application defined).")
    print(f"Registered tools with MCP server: {', '.join(mcp.tools.keys())}")
    print(f"When run with 'mcp run {__file__} --transport streamable-http',")
    print(f"it will likely use Uvicorn's default host/port (e.g., 127.0.0.1:8000) or PORT/HOST env vars.")

    # Example to list discovered tools by the mcp instance:
    # This can be useful for debugging if tools are not registering.
    # for tool_name, tool_obj in mcp.tools.items():
    #     print(f"  Tool: {tool_name} -> {tool_obj.fn.__module__}.{tool_obj.fn.__name__}")

    mcp.run(transport="streamable-http")
