import copy
import re

# Boolean equation line: lhs = GATE(arg1, arg2, ...) — used when converting LLM output back to Verilog
_BOOL_EQ_LINE = re.compile(
    r"^\s*([\w\[\].]+)\s*=\s*([A-Za-z_]\w*)\s*\(\s*([^)]*)\s*\)\s*;?\s*$"
)


def is_gate_line(line):
    keywords = ["not", "and", "or", "nand", "nor", "xor", "xnor", "buf"]
    if line.split(" ")[0] in keywords:
        return True
    else:
        return False
    # keywords = ["not ", "and ", "or ", "nand ", "nor ", "xor ", "xnor "]
    # for keyword in keywords:
    #     if keyword in line:
    #         return True
    # return False

def characterize_generic_netlist(file_contents):
    # with open(filename, 'r') as file:
    #     lines = file.readlines()
    # with open(filename,'r') as file:
    #     file_content = file.read()
    lines = file_contents.split(";")
    # Remove whitespace and empty lines
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n"," ") for line in lines]

    gate_types_and_count = {}

    for line in lines:
        # line_counter+=1
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            continue
        if is_gate_line(line):
            gate_type = line.split(" ")[0] + "_" + str(line.count(","))
            if gate_type not in gate_types_and_count:
                gate_types_and_count[gate_type] = 1
            else:
                gate_types_and_count[gate_type] +=1
    sorted_gate_types_and_count = dict(sorted(gate_types_and_count.items(), key=lambda x:x[1],reverse=True))
    return sorted_gate_types_and_count

def create_LLM_assign_query_template(sorted_gate_types_and_count):
    query_templates = {}
    for gate_type in sorted_gate_types_and_count:
        input_vars = ['A'+str(i+1) for i in range(int(gate_type.split("_")[1]))]
        output_var = "Y"
        if gate_type.split("_")[0] == 'not':
            template = "assign " + output_var + " = ~" + input_vars[0] + ";"
        elif gate_type.split("_")[0] == 'and':
            template = "assign " + output_var + " = " + " & ".join(input_vars) + ";"
        elif gate_type.split("_")[0] == 'or':
            template = "assign " + output_var + " = " + " | ".join(input_vars) + ";"
        elif gate_type.split("_")[0] == 'nand':
            template = "assign " + output_var + " = ~(" + " & ".join(input_vars) + ");"
        elif gate_type.split("_")[0] == 'nor':
            template = "assign " + output_var + " = ~(" + " | ".join(input_vars) + ");"
        elif gate_type.split("_")[0] == 'xor':
            template = "assign " + output_var + " = " + " ^ ".join(input_vars) + ";"
        elif gate_type.split("_")[0] == 'xnor':
            template = "assign " + output_var + " = ~(" + " ^ ".join(input_vars) + ");"
        elif gate_type.split("_")[0] == 'buf':
            template = "assign " + output_var + " = " + input_vars[0] + ";"
        else:
            print("ERROR! Found unknown gate type " + gate_type + " when generating the query template for the LLM")
            exit()
        query_templates[gate_type] = template
    return query_templates

def create_LLM_circuit_query_template(sorted_gate_types_and_count):
    query_templates = {}
    for gate_type in sorted_gate_types_and_count:
        input_vars = ['A'+str(i+1) for i in range(int(gate_type.split("_")[1]))]
        output_var = "Y"
        if gate_type.split("_")[0] == 'not':
            # template = "assign " + output_var + " = ~" + input_vars[0] + ";"
            template = output_var + " = NOT("+input_vars[0] +")"
        elif gate_type.split("_")[0] == 'and':
            # template = "assign " + output_var + " = " + " & ".join(input_vars) + ";"
            template = output_var + " = " + "AND(" + ", ".join(input_vars) +")"
        elif gate_type.split("_")[0] == 'or':
            # template = "assign " + output_var + " = " + " | ".join(input_vars) + ";"
            template = output_var + " = " + "OR(" + ", ".join(input_vars) +")"
        elif gate_type.split("_")[0] == 'nand':
            # template = "assign " + output_var + " = ~(" + " & ".join(input_vars) + ");"
            template = output_var + " = " + "NAND(" + ", ".join(input_vars) +")"
        elif gate_type.split("_")[0] == 'nor':
            # template = "assign " + output_var + " = ~(" + " | ".join(input_vars) + ");"
            template = output_var + " = " + "NOR(" + ", ".join(input_vars) +")"
        elif gate_type.split("_")[0] == 'xor':
            # template = "assign " + output_var + " = " + " ^ ".join(input_vars) + ";"
            template = output_var + " = " + "XOR(" + ", ".join(input_vars) +")"
        elif gate_type.split("_")[0] == 'xnor':
            # template = "assign " + output_var + " = ~(" + " ^ ".join(input_vars) + ");"
            template = output_var + " = " + "XNOR(" + ", ".join(input_vars) +")"
        elif gate_type.split("_")[0] == 'buf':
            # template = "assign " + output_var + " = " + input_vars[0] + ";"
            template = output_var + " = BUF("+input_vars[0] +")"
        else:
            print("ERROR! Found unknown gate type " + gate_type + " when generating the query template for the LLM")
            exit()
        query_templates[gate_type] = template
    return query_templates

def replace_gates_with_rephrased_assign_statements(file_contents,target_gate_type,assign_string):
    lines = file_contents.split(";")
    # Remove whitespace and empty lines
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n"," ") for line in lines]

    for i in range(len(lines)):
        line = lines[i]
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            continue
        if is_gate_line(line):
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            gate_type = line.split(" ")[0] + "_" + str(line.count(","))
            if gate_type == target_gate_type:
                # op = line.split(" ")[3].strip(",").strip()
                op = line.split()[3].strip(",").strip()
                num_ips = line.count(",")
                # ips = [line.split(" ")[4+j].strip().strip(",").strip() for j in range(num_ips)]
                ips = [line.split()[4+j].strip().strip(",").strip() for j in range(num_ips)]
                new_str = assign_string.replace("Y",op)
                for ip_idx in range(len(ips)):
                    new_str = new_str.replace("A"+str(ip_idx+1), ips[ip_idx])
                lines[i] = copy.deepcopy(new_str.strip(";"))
    return lines


def replace_gates_with_rephrased_gates(file_contents,target_gate_type,new_gates_str):
    lines = file_contents.split(";")
    # Remove whitespace and empty lines
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n"," ") for line in lines]

    new_lines = []
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            new_lines.append(line)
            continue
        if is_gate_line(line):
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            gate_type = line.split(" ")[0] + "_" + str(line.count(","))
            if gate_type == target_gate_type:
                # op = line.split(" ")[3].strip(",").strip()
                op = line.split()[3].strip(",").strip()
                num_ips = line.count(",")
                # ips = [line.split(" ")[4+j].strip().strip(",").strip() for j in range(num_ips)]
                ips = [line.split()[4+j].strip().strip(",").strip() for j in range(num_ips)]
                new_str = new_gates_str.replace("Y",op)
                for ip_idx in range(len(ips)):
                    new_str = new_str.replace("A"+str(ip_idx+1), ips[ip_idx])
                tmp_lines = new_str.split(";\n")
                for tmp_str in tmp_lines:
                    tmp_str = tmp_str.strip(";")
                    new_lines.append(tmp_str)
            else:
                new_lines.append(lines[i])
    return new_lines


def convert_circuit_to_Boolean_format(file_contents):
    """Extract gate-level Boolean equations; keep module/io/wire header for stitch-back."""
    lines = file_contents.split(";")
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n", " ") for line in lines]
    remaining_orig_lines = ""
    new_lines = ""
    for line in lines:
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            if line.startswith(("module ", "input ", "output ", "wire ")):
                remaining_orig_lines += line + "\n"
            continue
        if is_gate_line(line):
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            gate_type = line.split(" ")[0]
            op = line.split()[3].strip(",").strip()
            num_ips = line.count(",")
            ips = [line.split()[4 + j].strip().strip(",").strip() for j in range(num_ips)]
            new_str = op + " = " + gate_type.upper() + "(" + ", ".join(ips) + ")\n"
            new_lines += new_str
    return new_lines, remaining_orig_lines


def convert_circuit_from_Boolean_format(LLM_circuit, remaining_orig_lines):
    """
    Turn Boolean equations back into generic Verilog gate lines.
    Skips prose, markdown fences, and any line that is not `lhs = GATE(args)`.
    """
    new_lines = remaining_orig_lines
    ctr = 0
    for raw in LLM_circuit.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("```"):
            continue
        if line.startswith("#"):
            continue
        if "#" in line:
            line = line.split("#", 1)[0].strip()
        if not line:
            continue
        m = _BOOL_EQ_LINE.match(line)
        if not m:
            continue
        op, gate_type, args_str = m.group(1), m.group(2), m.group(3)
        ips = [a.strip() for a in args_str.split(",") if a.strip()]
        if not ips:
            continue
        new_str = (
            gate_type.lower()
            + " U"
            + str(ctr)
            + " ("
            + op
            + ", "
            + ", ".join(ips)
            + ");\n"
        )
        ctr += 1
        new_lines += new_str
    new_lines += "endmodule"
    return new_lines


# def characterize_generic_netlist_and_generate_query_templates(file_contents):
#     return create_LLM_assign_query_template(characterize_generic_netlist(file_contents))


if __name__ == '__main__':
    import os
    from config import DATASET_PATH
    
    generic_version_of_current_circuit = os.path.join(DATASET_PATH, "C432", "c432-BE280", "topModule.v")
    with open(generic_version_of_current_circuit,'r') as f:
        file_contents = f.read()
    sorted_gate_types_and_count = characterize_generic_netlist(file_contents)
    print(sorted_gate_types_and_count)
    # for key in sorted_gate_types_and_count:
    #     print(key, ":", sorted_gate_types_and_count[key])
    query_templates = create_LLM_assign_query_template(sorted_gate_types_and_count)
    print(query_templates)

    lines = replace_gates_with_rephrased_assign_statements(file_contents,"nand_2","assign Y = ~(A1 & A2);")
    print(";\n".join(lines))
