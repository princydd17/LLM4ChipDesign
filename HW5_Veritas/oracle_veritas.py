"""
HW5 Veritas — compare {design}_{typ}_tab.csv (BENCH truth table) to a Python reference oracle.

The simulator writes rows in *binary counting order* with the first name in `inputs` as the MSB
(see `truth_table()` in the notebook). This module matches that ordering.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple, Union

Row = List[int]


def load_tab_csv(path: Union[str, Path]) -> Tuple[List[str], List[Row]]:
    p = Path(path)
    with p.open(newline="") as f:
        r = csv.reader(f)
        header = next(r)
        rows = [[int(x) for x in row] for row in r]
    return header, rows


def split_header(header: Sequence[str], input_names: Sequence[str]) -> Tuple[List[int], List[int]]:
    """Return column indices for inputs and outputs (outputs = remaining columns in order)."""
    idx_in = [header.index(n) for n in input_names]
    rest = [i for i in range(len(header)) if i not in idx_in]
    return idx_in, rest


def validate_against_oracle(
    tab_path: Union[str, Path],
    input_names: Sequence[str],
    output_names: Sequence[str],
    expected_outputs: Callable[[Dict[str, int]], Dict[str, int]],
) -> Tuple[bool, str]:
    """
    Returns (ok, message). On failure, message includes the first mismatching row (0-based data row).
    """
    header, rows = load_tab_csv(tab_path)
    miss = [n for n in list(input_names) + list(output_names) if n not in header]
    if miss:
        return False, f"Tab CSV missing columns: {miss}. Header was: {header}"

    idx_in, idx_out = [], []
    for n in input_names:
        idx_in.append(header.index(n))
    for n in output_names:
        idx_out.append(header.index(n))

    for ri, row in enumerate(rows):
        ins = {input_names[j]: row[idx_in[j]] for j in range(len(input_names))}
        exp = expected_outputs(ins)
        for j, oname in enumerate(output_names):
            got = row[idx_out[j]]
            want = int(exp[oname])
            if got != want:
                return (
                    False,
                    f"Row {ri}: inputs={ins}  output {oname}: got {got} expected {want}",
                )
    return True, f"All {len(rows)} rows match."


# --- Reference oracles (unsigned binary; names must match your notebook I/O lists) ---


def oracle_ripple_adder(n_bits: int) -> Callable[[Dict[str, int]], Dict[str, int]]:
    """Inputs A0..A{n-1}, B0..B{n-1}, Cin. Outputs S0..S{n-1}, Cout."""

    def _go(ins: Dict[str, int]) -> Dict[str, int]:
        x = sum(ins[f"A{i}"] << i for i in range(n_bits))
        y = sum(ins[f"B{i}"] << i for i in range(n_bits))
        c = ins["Cin"]
        tot = x + y + c
        out: Dict[str, int] = {}
        for i in range(n_bits):
            out[f"S{i}"] = (tot >> i) & 1
        out["Cout"] = (tot >> n_bits) & 1
        return out

    return _go


def oracle_ripple_subtractor(n_bits: int) -> Callable[[Dict[str, int]], Dict[str, int]]:
    """
    Unsigned subtract with borrow in at LSB: A - B - Din.
    Inputs A0..A{n-1}, B0..B{n-1}, Din. Outputs S0..S{n-1}, Dout (borrow out).
    """

    def _go(ins: Dict[str, int]) -> Dict[str, int]:
        x = sum(ins[f"A{i}"] << i for i in range(n_bits))
        y = sum(ins[f"B{i}"] << i for i in range(n_bits))
        din = ins["Din"]
        tot = x - y - din
        if tot < 0:
            tot += 1 << n_bits
        bout = 1 if (x - y - din) < 0 else 0
        out: Dict[str, int] = {}
        for i in range(n_bits):
            out[f"S{i}"] = (tot >> i) & 1
        out["Dout"] = bout
        return out

    return _go


def oracle_decoder_binary_inputs(
    n_sel: int, output_names: Sequence[str]
) -> Callable[[Dict[str, int]], Dict[str, int]]:
    """
    n_sel select inputs named A0..A{n_sel-1} (LSB = A0). Outputs are one-hot in index order.
    """
    def _go(ins: Dict[str, int]) -> Dict[str, int]:
        idx = sum(ins[f"A{i}"] << i for i in range(n_sel))
        return {output_names[j]: (1 if j == idx else 0) for j in range(len(output_names))}

    return _go


def oracle_mux_2x1() -> Callable[[Dict[str, int]], Dict[str, int]]:
    """Inputs A, B, S (select). Output Y."""

    def _go(ins: Dict[str, int]) -> Dict[str, int]:
        y = ins["A"] if ins["S"] == 0 else ins["B"]
        return {"Y": y}

    return _go


def copy_run_artifacts(
    design: str,
    typ: str,
    dest: Union[str, Path],
    repo_root: Union[str, Path, None] = None,
) -> Path:
    """
    Copy generated files into artifacts/{design}_{typ}/ for submission.
    Looks for files in cwd or repo_root/HW5_Veritas.
    """
    stem = f"{design}_{typ}"
    names = [f"{stem}.cnf", f"{stem}.bench", f"{stem}.csv", f"{stem}_tab.csv", f"{stem}.v"]
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    roots = [Path.cwd()]
    if repo_root is not None:
        roots.append(Path(repo_root) / "HW5_Veritas")
    roots.append(Path(__file__).resolve().parent)

    copied = []
    for fn in names:
        src = None
        for r in roots:
            p = r / fn
            if p.is_file():
                src = p
                break
        if src is None:
            continue
        data = src.read_bytes()
        (dest / fn).write_bytes(data)
        copied.append(fn)
    if not copied:
        raise FileNotFoundError(f"No artifacts found for {stem} in {roots}")
    return dest
