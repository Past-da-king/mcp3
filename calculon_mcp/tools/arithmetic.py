import logging
from calculon_mcp.mcp_base import mcp # Import from new mcp_base

logger = logging.getLogger(__name__)

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
    logger.info(f"Tool 'add' called with a={a}, b={b}")
    result = a + b
    logger.info(f"Tool 'add' result: {result}")
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
    logger.info(f"Tool 'subtract' called with a={a}, b={b}")
    result = a - b
    logger.info(f"Tool 'subtract' result: {result}")
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
    logger.info(f"Tool 'multiply' called with a={a}, b={b}")
    result = a * b
    logger.info(f"Tool 'multiply' result: {result}")
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
    logger.info(f"Tool 'divide' called with numerator={numerator}, denominator={denominator}")
    if denominator == 0:
        logger.info("Tool 'divide' error: Division by zero.")
        return "Error: Cannot divide by zero."
    result = numerator / denominator
    logger.info(f"Tool 'divide' result: {result}")
    return result
