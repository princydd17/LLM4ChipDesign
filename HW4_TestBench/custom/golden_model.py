
def priority_encoder4_golden(**kwargs):
    """4-bit priority encoder golden model.

    Takes kwargs['d'] as an integer (masked to 4 bits) and returns:
      - valid: 1-bit (1 if any bit in d is 1)
      - enc: 2-bit integer index of MSB set (d[3] highest priority)
    """
    if 'd' not in kwargs:
        raise ValueError("Missing required input 'd'")

    d = int(kwargs['d']) & 0xF

    valid = 1 if d != 0 else 0
    if d & 0x8:
        enc = 3
    elif d & 0x4:
        enc = 2
    elif d & 0x2:
        enc = 1
    else:
        enc = 0

    return {'valid': int(valid), 'enc': int(enc)}
