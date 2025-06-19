import logging
from mcp.server.fastmcp import FastMCP # From installed MCP library

# It's generally better to configure logging once in the main executable script
# rather than in a base library file, to give the application more control.
# So, we will not call logging.basicConfig() here.
# Individual modules should get their loggers via logging.getLogger(__name__).

mcp = FastMCP(
    name="CalculonMCP",
    description="An MCP server providing advanced calculation and plotting tools for Calculon AI.",
    stateless_http=True # Added for consistency with original server config
)

# Optional: Logger for mcp_base.py itself, if it needs to log anything.
# logger = logging.getLogger(__name__)
# logger.info("FastMCP instance 'mcp' created in mcp_base.py.")
