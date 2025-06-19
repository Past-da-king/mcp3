# calculator_mcp_server_streamablehttp.py (Simplified run for Uvicorn defaults)
import logging
import math
import sympy
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from mcp.server.fastmcp import FastMCP

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

# Define and create plot directory
# Assumes calculater_mcp.py is in mcp/ and static/plots/ is at project_root/static/plots
PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)
logger.info(f"Plot directory set to: {PLOT_DIR}")

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

@mcp.tool()
def differentiate(expression_str: str, variable_str: str) -> str:
    """
    Symbolically differentiates an expression with respect to a variable.
    Expression and variable must be strings.

    Args:
        expression_str (str): The mathematical expression to differentiate (e.g., "x**2 + sin(x)").
        variable_str (str): The variable to differentiate with respect to (e.g., "x").

    Returns:
        str: The differentiated expression as a string, or an error message.
    """
    logger.info(f"Tool 'differentiate' called with expression='{expression_str}', variable='{variable_str}'")
    try:
        # Attempt to create a symbol for the variable
        # We should handle cases where variable_str might not be a valid symbol name
        # or if it conflicts with existing sympy functions if not careful with sympify's context.
        var_symbols = sympy.symbols(variable_str)

        # If variable_str is a comma-separated list of variables, symbols() returns a tuple.
        # We assume a single variable for differentiation for simplicity here.
        if isinstance(var_symbols, tuple):
            if len(var_symbols) == 1:
                x = var_symbols[0]
            else:
                logger.error("Differentiate tool currently supports differentiation with respect to a single variable only.")
                return "Error: Differentiation with respect to multiple variables simultaneously is not supported. Please specify one variable."
        else:
            x = var_symbols

        # Provide a basic local context for sympify, including the symbol itself.
        # This allows expressions like "x**2" to be parsed correctly.
        # Add other common math functions/constants if needed and if they don't clash.
        # For many common functions like sin, cos, exp, sympy's sympify will parse them automatically.
        local_dict = {variable_str: x, 'e': sympy.E, 'pi': sympy.pi}

        expr = sympy.sympify(expression_str, locals=local_dict)

        # Ensure the expression contains the variable of differentiation
        if x not in expr.free_symbols:
            # This check is useful but might be too strict if the variable is part of a constant's definition
            # that gets simplified away before this check. However, for typical use cases it's good.
            logger.warning(f"Variable '{variable_str}' not found in expression '{expression_str}' or expression is constant with respect to it.")
            # Depending on desired behavior, could return 0 if var not in free_symbols,
            # but warning and proceeding is also an option as sympy.diff will handle it.
            # For now, we'll let sympy.diff produce 0 if that's the case.

        derivative_expr = sympy.diff(expr, x)
        result_str = str(derivative_expr)
        logger.info(f"Tool 'differentiate' result: {result_str}")
        return result_str
    except (sympy.SympifyError, TypeError, ValueError) as e:
        logger.error(f"Error in differentiate tool (parsing or type error): {e}")
        return f"Error during differentiation (check expression or variable): {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in differentiate tool: {e}")
        return f"Error during differentiation: {str(e)}"

@mcp.tool()
def integrate_indefinite(expression_str: str, variable_str: str) -> str:
    """
    Symbolically integrates an expression indefinitely with respect to a variable.
    Expression and variable must be strings. Includes the constant of integration "C".

    Args:
        expression_str (str): The mathematical expression to integrate (e.g., "2*x + cos(x)").
        variable_str (str): The variable to integrate with respect to (e.g., "x").

    Returns:
        str: The integrated expression (antiderivative) as a string, with "+ C", or an error message.
    """
    logger.info(f"Tool 'integrate_indefinite' called with expression='{expression_str}', variable='{variable_str}'")
    try:
        var_symbols = sympy.symbols(variable_str)
        if isinstance(var_symbols, tuple):
            if len(var_symbols) == 1:
                x = var_symbols[0]
            else:
                logger.error("Integrate tool currently supports integration with respect to a single variable only.")
                return "Error: Integration with respect to multiple variables simultaneously is not supported. Please specify one variable."
        else:
            x = var_symbols

        local_dict = {variable_str: x, 'e': sympy.E, 'pi': sympy.pi}
        expr = sympy.sympify(expression_str, locals=local_dict)

        # It's good practice to ensure the variable is in the expression for clarity,
        # though integrate will handle constants correctly.
        # if x not in expr.free_symbols:
        #    logger.warning(f"Variable '{variable_str}' not found in expression '{expression_str}'. The expression might be treated as a constant.")

        integral_expr = sympy.integrate(expr, x)

        # Add the constant of integration, C
        # Create a sympy symbol for C to ensure it's treated as a symbol in the string output
        C = sympy.Symbol("C")
        result_with_C = integral_expr + C
        result_str = str(result_with_C)

        logger.info(f"Tool 'integrate_indefinite' result: {result_str}")
        return result_str
    except (sympy.SympifyError, TypeError, ValueError) as e:
        logger.error(f"Error in integrate_indefinite tool (parsing or type error): {e}")
        return f"Error during integration (check expression or variable): {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in integrate_indefinite tool: {e}")
        return f"Error during integration: {str(e)}"

@mcp.tool()
def plot_expression(expression_str: str, variable_str: str, min_val_str: str, max_val_str: str) -> str:
    """
    Plots a mathematical expression over a given range and returns a URL to the image.
    Expression, variable, and min/max values must be strings.

    Args:
        expression_str (str): The mathematical expression to plot (e.g., "x**2 - sin(x)").
        variable_str (str): The variable in the expression (e.g., "x").
        min_val_str (str): The minimum value of the range for the variable (e.g., "-10").
        max_val_str (str): The maximum value of the range for the variable (e.g., "10").

    Returns:
        str: A URL to the saved plot image (e.g., "/static/plots/plot_timestamp.png") or an error message.
    """
    logger.info(
        f"Tool 'plot_expression' called with expression='{expression_str}', variable='{variable_str}', "
        f"min_val='{min_val_str}', max_val='{max_val_str}'"
    )
    try:
        x_sym = sympy.symbols(variable_str)
        # Sympyfy with a basic local context including the symbol itself and common constants
        local_dict = {variable_str: x_sym, 'e': sympy.E, 'pi': sympy.pi}
        # Add common sympy functions to prevent them from being treated as undefined symbols
        # This is important if the expression string uses functions like "sin" or "cos"
        for func_name in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']:
            local_dict[func_name] = getattr(sympy, func_name, None)

        expr = sympy.sympify(expression_str, locals=local_dict)

        try:
            min_val = float(min_val_str)
            max_val = float(max_val_str)
        except ValueError:
            logger.error("Invalid min/max values: must be numbers.")
            return "Error: min_val and max_val must be valid numbers."

        if min_val >= max_val:
            logger.error("Invalid range: min_val must be less than max_val.")
            return "Error: min_val must be less than max_val."

        # Generate data for plotting
        # Increased points for smoother curve, especially for complex functions
        x_vals = np.linspace(min_val, max_val, 300)

        # Lambdify the sympy expression for faster numerical evaluation
        # Note: Using "numpy" module for lambdify allows it to work with numpy arrays directly
        # This is generally much faster than iterating and substituting with .evalf()
        # Ensure all functions in the sympy expression are recognized by numpy or are sympy functions that lambdify can handle.
        # Common sympy functions (sin, cos, exp, etc.) are usually fine.
        # For more complex sympy-specific functions, this might need adjustment or fall back to subs/evalf.
        try:
            # Check for free symbols other than the plotting variable
            other_symbols = expr.free_symbols - {x_sym}
            if other_symbols:
                # Attempt to substitute common constants if they appear as free symbols due to parsing
                substitutions = {}
                for s in other_symbols:
                    if s.name == 'e': substitutions[s] = sympy.E
                    elif s.name == 'pi': substitutions[s] = sympy.pi
                if substitutions:
                    expr = expr.subs(substitutions)

                # Re-check after substitution
                other_symbols = expr.free_symbols - {x_sym}
                if other_symbols:
                    logger.error(f"Expression contains unassigned variables: {other_symbols}. Cannot plot.")
                    return f"Error: Expression contains unassigned variables: {', '.join(str(s) for s in other_symbols)}. Please define them or ensure they are part of the main variable '{variable_str}'."

            # If the expression becomes a constant after substitutions (e.g. "pi" or "2+3")
            if not expr.free_symbols: # No variable in expression, it's a constant
                 y_val_const = float(expr.evalf())
                 y_vals = np.full_like(x_vals, y_val_const)
            else:
                # Proceed with lambdify if there's a variable
                # Using 'numpy' module for lambdify for array inputs
                # For functions like sympy.Heaviside, sympy.DiracDelta, etc., they might need specific handling
                # or might not be directly translatable to numpy. For common functions, it's okay.
                f_numpy = sympy.lambdify(x_sym, expr, modules=['numpy'])
                y_vals = f_numpy(x_vals)

        except Exception as lambdify_eval_e:
            logger.warning(f"Lambdify/Numpy evaluation failed: {lambdify_eval_e}. Falling back to subs/evalf.")
            # Fallback for functions not handled well by lambdify's numpy conversion
            y_vals_num = [expr.subs({x_sym: val}).evalf() for val in x_vals]
            y_vals = np.array([float(y) for y in y_vals_num])


        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6)) # Slightly larger figure size
        ax.plot(x_vals, y_vals)
        ax.set_xlabel(variable_str, fontsize=12)
        ax.set_ylabel(expression_str, fontsize=12) # Using expression_str might be too long, consider a shorter label or none
        ax.set_title(f"Plot of f({variable_str}) = {expression_str}", fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout() # Adjust layout to prevent labels from being cut off

        # Save plot to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"plot_{variable_str}_{timestamp}.png" # More descriptive filename
        filepath = os.path.join(PLOT_DIR, filename)

        plt.savefig(filepath)
        plt.close(fig)  # Important to free memory

        plot_url = f"/static/plots/{filename}"
        logger.info(f"Tool 'plot_expression' result: Plot saved at {filepath}, URL: {plot_url}")
        return plot_url

    except (sympy.SympifyError, TypeError, ValueError) as e:
        logger.error(f"Error in plot_expression tool (parsing, type, or value error): {e}")
        return f"Error during plotting (check expression, variable, or range): {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in plot_expression tool: {e}")
        # It's good to log the traceback for unexpected errors
        import traceback
        logger.error(traceback.format_exc())
        return f"Error during plotting: {str(e)}"

if __name__ == "__main__":
    print(f"Starting CalculatorStreamableHttpServer (FastMCP application defined).")
    print(f"When run with 'mcp run calculator_mcp_server_streamablehttp.py --transport streamable-http',")
    print(f"it will likely use Uvicorn's default host/port (e.g., 127.0.0.1:8000) or PORT/HOST env vars.")
    mcp.run(transport="streamable-http")