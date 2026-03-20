def mux2to1_golden(**kwargs):
    """
    2-to-1 multiplexer reference implementation.

    Args:
        a (int): Input a (1-bit).
        b (int): Input b (1-bit).
        sel (int): Select signal (1-bit).

    Returns:
        dict: Dictionary containing the output 'y' (1-bit).
    """
    # Check if all required inputs are present
    required_inputs = ['a', 'b', 'sel']
    if not all(input in kwargs for input in required_inputs):
        raise ValueError("Missing required input(s)")

    # Get the inputs
    a = kwargs['a']
    b = kwargs['b']
    sel = kwargs['sel']

    # Perform the multiplexing operation
    if sel == 0:
        y = a
    elif sel == 1:
        y = b
    else:
        raise ValueError("Invalid select signal value")

    # Return the output as a dictionary
    return {'y': y}