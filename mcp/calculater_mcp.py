# calculator_mcp_server_streamablehttp.py (Simplified run for Uvicorn defaults)
import logging
import math
from mcp.server.fastmcp import FastMCP

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

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

@mcp.tool()
def sin(angle: float, unit: str = "radians") -> float | str:
    """
    Calculates the sine of an angle. Angle can be in 'radians' or 'degrees'.

    Args:
        angle (float): The angle value.
        unit (str): The unit of the angle, 'radians' or 'degrees'. Defaults to 'radians'.

    Returns:
        float: The sine of the angle.
        str: An error message if the unit is invalid.
    """
    logger.info(f"Tool 'sin' called with angle={angle}, unit={unit}")
    unit_lower = unit.lower()
    radian_angle = angle
    if unit_lower == "degrees":
        radian_angle = math.radians(angle)
    elif unit_lower != "radians":
        logger.error(f"Tool 'sin' error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'.")
        return f"Error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'."

    result = math.sin(radian_angle)
    logger.info(f"Tool 'sin' result: {result}")
    return result

@mcp.tool()
def cos(angle: float, unit: str = "radians") -> float | str:
    """
    Calculates the cosine of an angle. Angle can be in 'radians' or 'degrees'.

    Args:
        angle (float): The angle value.
        unit (str): The unit of the angle, 'radians' or 'degrees'. Defaults to 'radians'.

    Returns:
        float: The cosine of the angle.
        str: An error message if the unit is invalid.
    """
    logger.info(f"Tool 'cos' called with angle={angle}, unit={unit}")
    unit_lower = unit.lower()
    radian_angle = angle
    if unit_lower == "degrees":
        radian_angle = math.radians(angle)
    elif unit_lower != "radians":
        logger.error(f"Tool 'cos' error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'.")
        return f"Error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'."

    result = math.cos(radian_angle)
    logger.info(f"Tool 'cos' result: {result}")
    return result

@mcp.tool()
def tan(angle: float, unit: str = "radians") -> float | str:
    """
    Calculates the tangent of an angle. Angle can be in 'radians' or 'degrees'.

    Args:
        angle (float): The angle value.
        unit (str): The unit of the angle, 'radians' or 'degrees'. Defaults to 'radians'.

    Returns:
        float: The tangent of the angle.
        str: An error message if the unit is invalid.
    """
    logger.info(f"Tool 'tan' called with angle={angle}, unit={unit}")
    unit_lower = unit.lower()
    radian_angle = angle
    if unit_lower == "degrees":
        radian_angle = math.radians(angle)
    elif unit_lower != "radians":
        logger.error(f"Tool 'tan' error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'.")
        return f"Error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'."

    result = math.tan(radian_angle)
    logger.info(f"Tool 'tan' result: {result}")
    return result

@mcp.tool()
def asin_op(value: float, unit: str = "radians") -> float | str:
    """
    Calculates the arcsine (inverse sine) of a value. Result is in 'radians' or 'degrees'.

    Args:
        value (float): The value whose arcsine is to be calculated. Must be between -1 and 1.
        unit (str): The unit for the result, 'radians' or 'degrees'. Defaults to 'radians'.

    Returns:
        float: The arcsine of the value in the specified unit.
        str: An error message if the value is out of domain or unit is invalid.
    """
    logger.info(f"Tool 'asin_op' called with value={value}, unit={unit}")
    if not (-1.0 <= value <= 1.0):
        logger.error("Tool 'asin_op' error: Input value for asin must be between -1 and 1.")
        return "Error: Input value for asin must be between -1 and 1."

    result_rad = math.asin(value)
    unit_lower = unit.lower()

    if unit_lower == "degrees":
        result = math.degrees(result_rad)
    elif unit_lower == "radians":
        result = result_rad
    else:
        logger.error(f"Tool 'asin_op' error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'.")
        return f"Error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'."

    logger.info(f"Tool 'asin_op' result: {result} {unit_lower}")
    return result

@mcp.tool()
def acos_op(value: float, unit: str = "radians") -> float | str:
    """
    Calculates the arccosine (inverse cosine) of a value. Result is in 'radians' or 'degrees'.

    Args:
        value (float): The value whose arccosine is to be calculated. Must be between -1 and 1.
        unit (str): The unit for the result, 'radians' or 'degrees'. Defaults to 'radians'.

    Returns:
        float: The arccosine of the value in the specified unit.
        str: An error message if the value is out of domain or unit is invalid.
    """
    logger.info(f"Tool 'acos_op' called with value={value}, unit={unit}")
    if not (-1.0 <= value <= 1.0):
        logger.error("Tool 'acos_op' error: Input value for acos must be between -1 and 1.")
        return "Error: Input value for acos must be between -1 and 1."

    result_rad = math.acos(value)
    unit_lower = unit.lower()

    if unit_lower == "degrees":
        result = math.degrees(result_rad)
    elif unit_lower == "radians":
        result = result_rad
    else:
        logger.error(f"Tool 'acos_op' error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'.")
        return f"Error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'."

    logger.info(f"Tool 'acos_op' result: {result} {unit_lower}")
    return result

@mcp.tool()
def atan_op(value: float, unit: str = "radians") -> float | str:
    """
    Calculates the arctangent (inverse tangent) of a value. Result is in 'radians' or 'degrees'.

    Args:
        value (float): The value whose arctangent is to be calculated.
        unit (str): The unit for the result, 'radians' or 'degrees'. Defaults to 'radians'.

    Returns:
        float: The arctangent of the value in the specified unit.
        str: An error message if the unit is invalid.
    """
    logger.info(f"Tool 'atan_op' called with value={value}, unit={unit}")
    result_rad = math.atan(value)
    unit_lower = unit.lower()

    if unit_lower == "degrees":
        result = math.degrees(result_rad)
    elif unit_lower == "radians":
        result = result_rad
    else:
        logger.error(f"Tool 'atan_op' error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'.")
        return f"Error: Invalid unit '{unit}'. Must be 'radians' or 'degrees'."

    logger.info(f"Tool 'atan_op' result: {result} {unit_lower}")
    return result

if __name__ == "__main__":
    print(f"Starting CalculatorStreamableHttpServer (FastMCP application defined).")
    print(f"When run with 'mcp run calculator_mcp_server_streamablehttp.py --transport streamable-http',")
    print(f"it will likely use Uvicorn's default host/port (e.g., 127.0.0.1:8000) or PORT/HOST env vars.")
    mcp.run(transport="streamable-http")