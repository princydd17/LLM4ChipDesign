# HW_ROME

This folder contains the ROME homework submission artifacts.

## Required deliverables

- `rome_submission.ipynb`
- Generated RTL folders for the provided mux hierarchy demo
- Generated RTL folders for the new extension hierarchy
- `ROME_Report.pdf`

## Part I: Provided mux hierarchy

Run the provided `ROME_demo.ipynb` and generate:

- `mux2to1`
- `mux4to1`
- `mux8to1`

For each module, include:

- final `.v` file
- self-checking testbench `*tb.v`
- `log_iter_*.txt` files from the notebook feedback loop

Verification evidence should show that each module reaches successful testbench execution and prints `passed!`.

## Part II: New hierarchical design

Create a new hierarchical design with at least 3 modules total, including a top module.

Assignment requirements:

- the top module must instantiate at least 2 previously generated submodules
- the design must not be a monolithic rewrite
- every module must have a self-checking testbench
- each successful testbench must print a final line containing `passed!`

Suggested example from the assignment:

- `half_adder`
- `full_adder`
- `adder4`
- `adder8`

For each module, include:

- final `.v` file
- self-checking testbench `*tb.v`
- `log_iter_*.txt` files

## Part III: Debugging documentation

For at least 1 module from Part II, document at least 3 iterations:

- what failed
- what you changed in the prompt or code
- what the outcome was

Include the important `iverilog` or `vvp` output snippets that motivated the fix, and end with a final passing run.

## Report requirements

`ROME_Report.pdf` should include:

- model used
- key generation settings, if changed
- hierarchical decomposition
- module list and interfaces
- which modules instantiate which
- final prompt for the top module
- final prompt for 1 representative submodule
- concise iteration table for Part III
- confirmation that all testbenches pass
- final `iverilog` and `vvp` commands used

## Submission reminders

- submit through the GitHub repo only
- reuse the existing homework repo
- put all required deliverables inside `HW_ROME/`
- invite `weihuax6@gmail.com` as a collaborator if not already invited

## Important checks

- the notebook should run top-to-bottom except for adding the API key in the designated place
- do not commit any API keys or secrets
- use the assignment PDF checklist before submitting
