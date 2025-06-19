import logging
import math
from mcp.calculater_mcp import mcp # Absolute import

logger = logging.getLogger(__name__)

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
