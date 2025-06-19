import logging
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import sympy
from calculon_mcp.mcp_base import mcp # Import from new mcp_base

logger = logging.getLogger(__name__)

# Define and create plot directory
# Adjusted path: mcp/tools/plotting.py -> ../../static/plots
PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)
logger.info(f"Plot directory for plotting.py set to: {PLOT_DIR}")

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
        local_dict = {variable_str: x_sym, 'e': sympy.E, 'pi': sympy.pi}
        for func_name in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']: # Common functions for sympify
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

        x_vals = np.linspace(min_val, max_val, 300)

        y_vals = None # Initialize y_vals
        try:
            other_symbols = expr.free_symbols - {x_sym}
            if other_symbols:
                substitutions = {}
                for s in other_symbols:
                    if s.name == 'e': substitutions[s] = sympy.E
                    elif s.name == 'pi': substitutions[s] = sympy.pi
                if substitutions:
                    expr = expr.subs(substitutions)

                other_symbols = expr.free_symbols - {x_sym}
                if other_symbols:
                    logger.error(f"Expression contains unassigned variables: {other_symbols}. Cannot plot.")
                    return f"Error: Expression contains unassigned variables: {', '.join(str(s) for s in other_symbols)}. Please define them or ensure they are part of the main variable '{variable_str}'."

            if not expr.free_symbols:
                 y_val_const = float(expr.evalf())
                 y_vals = np.full_like(x_vals, y_val_const)
            else:
                f_numpy = sympy.lambdify(x_sym, expr, modules=['numpy'])
                y_vals = f_numpy(x_vals)

        except Exception as lambdify_eval_e:
            logger.warning(f"Lambdify/Numpy evaluation failed: {lambdify_eval_e}. Falling back to subs/evalf.")
            y_vals_num = [expr.subs({x_sym: val}).evalf() for val in x_vals]
            y_vals = np.array([float(y) for y in y_vals_num])

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals)
        ax.set_xlabel(variable_str, fontsize=12)
        ax.set_ylabel(f"f({variable_str})", fontsize=12) # Using a generic f(variable) for Y label
        ax.set_title(f"Plot of f({variable_str}) = {expression_str}", fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"plot_{variable_str}_{timestamp}.png"
        filepath = os.path.join(PLOT_DIR, filename)

        plt.savefig(filepath)
        plt.close(fig)

        plot_url = f"/static/plots/{filename}"
        logger.info(f"Tool 'plot_expression' result: Plot saved at {filepath}, URL: {plot_url}")
        return plot_url

    except (sympy.SympifyError, TypeError, ValueError) as e:
        logger.error(f"Error in plot_expression tool (parsing, type, or value error): {e}")
        return f"Error during plotting (check expression, variable, or range): {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in plot_expression tool: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return f"Error during plotting: {str(e)}"
