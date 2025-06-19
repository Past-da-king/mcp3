import sys
import os

# Add project root to sys.path to allow absolute imports like 'from calculon_mcp.tools...'
# This assumes calculater_mcp.py is in project_root/calculon_mcp/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT) # Insert at the beginning

# Now proceed with other imports
import logging
# This import (mcp.server.fastmcp) refers to the INSTALLED mcp library,
# NOT our local calculon_mcp package. This should resolve correctly if the
# installed mcp library is in the standard Python path and our PROJECT_ROOT
# insertion for 'calculon_mcp' does not interfere with it.
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
    from calculon_mcp.tools.arithmetic import add, subtract, multiply, divide
    from calculon_mcp.tools.advanced_math import power, sqrt, get_constant
    from calculon_mcp.tools.trigonometry import sin, cos, tan, asin_op, acos_op, atan_op
    from calculon_mcp.tools.calculus import differentiate, integrate_indefinite
    from calculon_mcp.tools.plotting import plot_expression # This also initializes PLOT_DIR from plotting.py
    logger.info("All calculation tools imported successfully.")
except ImportError as e:
    logger.error(f"Error importing local tools from 'calculon_mcp.tools': {e}. Ensure all tool modules and __init__.py files are correct, and that the project root is in PYTHONPATH.")
    # Depending on desired behavior, might raise the error or exit
    raise e


# No tool function definitions directly in this file anymore.
# They are now in their respective modules in the 'tools' subdirectory.

# The PLOT_DIR definition and os.makedirs for it have been moved to mcp/tools/plotting.py
# Imports like math, sympy, os, datetime, matplotlib, numpy are now in their respective tool modules.

if __name__ == "__main__":
    print(f"Starting CalculatorStreamableHttpServer (FastMCP application defined).")
    # The following line might cause an error if tools fail to import due to sys.path issues resolved too late,
    # or if mcp instance itself isn't created.
    # Consider moving it after the try-except block for tool imports if issues persist.
    print(f"Registered tools with MCP server: {', '.join(mcp.tools.keys())}")
    print(f"When run with 'mcp run {__file__} --transport streamable-http',")
    print(f"it will likely use Uvicorn's default host/port (e.g., 127.0.0.1:8000) or PORT/HOST env vars.")

    # Example to list discovered tools by the mcp instance:
    # This can be useful for debugging if tools are not registering.
    # for tool_name, tool_obj in mcp.tools.items():
    #     print(f"  Tool: {tool_name} -> {tool_obj.fn.__module__}.{tool_obj.fn.__name__}")

    mcp.run(transport="streamable-http")
