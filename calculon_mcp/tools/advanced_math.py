import logging
import math
from calculon_mcp.calculater_mcp import mcp # Updated absolute import

logger = logging.getLogger(__name__)

@mcp.tool()
def power(base: float, exponent: float) -> float:
    """
    Calculates the power of a base to an exponent.

    Args:
        base (float): The base number.
        exponent (float): The exponent.

    Returns:
        float: The result of base raised to the exponent.
    """
    logger.info(f"Tool 'power' called with base={base}, exponent={exponent}")
    result = base ** exponent
    logger.info(f"Tool 'power' result: {result}")
    return result

@mcp.tool()
def sqrt(number: float) -> float | str:
    """
    Calculates the square root of a number.

    Args:
        number (float): The number to calculate the square root of.

    Returns:
        float: The square root of the number.
        str: An error message if the number is negative.
    """
    logger.info(f"Tool 'sqrt' called with number={number}")
    if number < 0:
        logger.error("Tool 'sqrt' error: Cannot calculate square root of a negative number.")
        return "Error: Cannot calculate square root of a negative number."
    result = math.sqrt(number)
    logger.info(f"Tool 'sqrt' result: {result}")
    return result

@mcp.tool()
def get_constant(name: str) -> float | str:
    """
    Returns the value of a mathematical constant.

    Args:
        name (str): The name of the constant (pi or e).

    Returns:
        float: The value of the constant.
        str: An error message if the constant name is unknown.
    """
    logger.info(f"Tool 'get_constant' called with name={name}")
    name_lower = name.lower()
    if name_lower == "pi":
        logger.info(f"Tool 'get_constant' result: {math.pi}")
        return math.pi
    elif name_lower == "e":
        logger.info(f"Tool 'get_constant' result: {math.e}")
        return math.e
    else:
        logger.warning(f"Tool 'get_constant' error: Unknown constant '{name}'.")
        return f"Error: Unknown constant '{name}'."
