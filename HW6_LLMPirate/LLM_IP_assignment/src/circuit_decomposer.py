
def parse_expression(expr):
    """
    Parse the expression into its constituent parts and operator.

    This function assumes the expression is well-formed and starts with an operator followed by a parenthesis.

    Returns the operator and a list of operands.
    """
    # Identify the main operator (assuming it's up to the first '(')
    op_end = expr.find('(')
    operator = expr[:op_end].strip()

    # Process the inside of the parentheses to split operands
    operands = []
    balance = 0
    current_operand = []
    for char in expr[op_end + 1:-1]:  # Skip the outermost parentheses
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if char == ',' and balance == 0:
            operands.append(''.join(current_operand).strip())
            current_operand = []
        else:
            current_operand.append(char)
    operands.append(''.join(current_operand).strip())  # Add the last operand

    return operator, operands

def decompose_expression(expr, var_count=[0]):
    """
    Decompose the given Boolean expression into simpler expressions with one operator each.

    Args:
    - expr: The Boolean expression to decompose.
    - var_count: A list with a single element used to keep track of the temporary variable count.

    Returns:
    - A list of strings, each representing a step in the decomposition.
    - The final expression or variable representing the result of the decomposed expression.
    """
    if '(' not in expr:  # Simple case, no decomposition needed
        return [], expr

    operator, operands = parse_expression(expr)
    decomposed_lines = []
    processed_operands = []

    for operand in operands:
        if '(' in operand:  # Complex operand, decompose further
            inner_decomposed, inner_result = decompose_expression(operand, var_count)
            decomposed_lines += inner_decomposed
            processed_operands.append(inner_result)
        else:
            processed_operands.append(operand)

    # Generate a new temp variable for this operation's result
    temp_var = f'my_N{var_count[0]}'
    var_count[0] += 1
    operation_expr = f'{temp_var} = {operator}({", ".join(processed_operands)})'
    decomposed_lines.append(operation_expr)

    return decomposed_lines, temp_var

def final_decompose_expression(expression,op_net):
    decomposed_lines, final_result = decompose_expression(expression)
    decomposed_lines_str = "\n".join(decomposed_lines)
    decomposed_lines_str = decomposed_lines_str.replace(final_result,op_net)
    return decomposed_lines_str

if __name__ == '__main__':
    # Example usage
    expression = "NOR(NOR(A1, A1), NOR(NOR(A2, A2), NOR(A3, A3)))"
    expression = "NAND(NOR(A1, A1), NOR(NOR(A2, A2), NOR(A3, A3)))"
    expression = "NAND(NOR(A1, A1), NOR(NOR(A2, A2, NOT(A3)), NOR(A3, A3), NOT(A1)))"
    # expression = "NAND(A1, A1)\nNOR(NOR(A2,A2),A3)" # Doesn't work
    expression = "NAND(A1, A2)"
    expression = "NOT (OR (NOT (A1), NOT (A2)))"
    decomposed_lines_str = final_decompose_expression(expression,'Y')
    # decomposed_lines, final_result = decompose_expression(expression)
    # decomposed_lines_str = "\n".join(decomposed_lines)
    # decomposed_lines_str = decomposed_lines_str.replace(final_result,"Y")
    print(decomposed_lines_str)
    # for line in decomposed_lines:
    #     print(line)
    # print(f'Y = {final_result}')
