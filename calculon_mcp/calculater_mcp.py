import sys
import os

# Add project root to sys.path to allow absolute imports like 'from calculon_mcp.tools...'
# This assumes calculater_mcp.py is in project_root/calculon_mcp/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT) # Insert at the beginning

# Core Python imports
import logging

# Import the shared mcp instance from mcp_base
# This MUST come after sys.path modification and before tool imports
from calculon_mcp.mcp_base import mcp

# Configure basic logging for the application
# This should be done once, as early as possible.
# Tool modules will use logging.getLogger(__name__) and inherit this configuration.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Logger for this specific file (calculater_mcp.py)
logger = logging.getLogger(__name__)

# Import tools from their respective modules.
# The act of importing these modules executes the @mcp.tool() decorators within them,
# registering the tools with the 'mcp' instance imported from mcp_base.
logger.info("Importing calculation tools...")
try:
    from calculon_mcp.tools.arithmetic import add, subtract, multiply, divide
    from calculon_mcp.tools.advanced_math import power, sqrt, get_constant
    from calculon_mcp.tools.trigonometry import sin, cos, tan, asin_op, acos_op, atan_op
    from calculon_mcp.tools.calculus import differentiate, integrate_indefinite
    from calculon_mcp.tools.plotting import plot_expression
    logger.info("All calculation tools imported successfully.")
except ImportError as e:
    logger.error(f"Error importing local tools from 'calculon_mcp.tools': {e}. Ensure all tool modules and __init__.py files are correct, and that the project root is in PYTHONPATH.")
    # Depending on desired behavior, might raise the error or exit
    raise e

# The FastMCP class itself is no longer imported or instantiated here.
# All tool function definitions have been moved to their respective modules.
# PLOT_DIR and related os/datetime imports for it are now in calculon_mcp/tools/plotting.py.

if __name__ == "__main__":
    # Log the state of the mcp instance before running
    logger.info(f"Starting {mcp.name} server...")
    logger.info(f"Description: {mcp.description}")
    logger.info(f"Stateless HTTP mode (from mcp_base): {getattr(mcp, 'stateless_http', 'N/A (attribute not set)')}") # Check if stateless_http is set

    if mcp.tools:
        logger.info(f"Registered tools with MCP server: {', '.join(mcp.tools.keys())}")
        # Detailed listing of tools and their modules for debugging:
        # for tool_name, tool_obj in mcp.tools.items():
        #     logger.debug(f"  Tool: {tool_name} -> {tool_obj.fn.__module__}.{tool_obj.fn.__name__}")
    else:
        logger.warning("No tools seem to be registered with the MCP server.")

    print(f"Starting {mcp.name} (FastMCP application defined).") # Keep print for user feedback
    print(f"Registered tools: {', '.join(mcp.tools.keys()) if mcp.tools else 'None'}")
    print(f"To run, use a command like: mcp run {__file__} --transport streamable-http")
    print(f"Server will likely use Uvicorn's default host/port (e.g., 127.0.0.1:8000) or PORT/HOST env vars.")

    mcp.run(transport="streamable-http")
