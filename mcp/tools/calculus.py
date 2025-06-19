import logging
import sympy
from mcp.calculater_mcp import mcp # Absolute import

logger = logging.getLogger(__name__)

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
        var_symbols = sympy.symbols(variable_str)

        if isinstance(var_symbols, tuple):
            if len(var_symbols) == 1:
                x = var_symbols[0]
            else:
                logger.error("Differentiate tool currently supports differentiation with respect to a single variable only.")
                return "Error: Differentiation with respect to multiple variables simultaneously is not supported. Please specify one variable."
        else:
            x = var_symbols

        local_dict = {variable_str: x, 'e': sympy.E, 'pi': sympy.pi}

        expr = sympy.sympify(expression_str, locals=local_dict)

        if x not in expr.free_symbols:
            logger.warning(f"Variable '{variable_str}' not found in expression '{expression_str}' or expression is constant with respect to it.")

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

        integral_expr = sympy.integrate(expr, x)

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
