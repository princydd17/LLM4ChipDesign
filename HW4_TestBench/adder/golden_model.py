def adder4bit_golden(**kwargs):
    """
    4-bit unsigned adder reference implementation.

    Args:
        a (int): 4-bit unsigned input a.
        b (int): 4-bit unsigned input b.

    Returns:
        dict: Dictionary containing the sum and carry outputs.
    """
    # Check if inputs are valid
    if not (0 <= kwargs['a'] <= 15 and 0 <= kwargs['b'] <= 15):
        raise ValueError("Inputs must be 4-bit unsigned integers")

    # Perform addition
    sum_value = kwargs['a'] + kwargs['b']

    # Calculate carry
    carry = 1 if sum_value > 15 else 0

    # Calculate sum (wrap around if sum_value > 15)
    sum_value = sum_value % 16

    # Return outputs as a dictionary
    return {'sum': sum_value, 'carry': carry}

# Example usage:
inputs = {'a': 5, 'b': 7}
outputs = adder4bit_golden(**inputs)
print(f"Sum: {outputs['sum']}, Carry: {outputs['carry']}")