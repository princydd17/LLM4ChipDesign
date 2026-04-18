
def is_gate_line(line):
    keywords = ["not", "and", "or", "nand", "nor", "xor", "xnor", "buf"]
    if line.split(" ")[0] in keywords:
        return True
    else:
        return False

def convert_to_NanGate(file_contents,output_file_name):
    lines = file_contents.split(";")
    # Remove whitespace and empty lines
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n"," ") for line in lines]
    new_lines = []
    for line in lines:
        # line_counter+=1
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            new_lines.append(line)
            continue
        if is_gate_line(line):
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            gate_type = line.split(" ")[0] + "_" + str(line.count(","))
            gate_name = line.split()[1].strip()
            op = line.split()[3].strip(",").strip()
            num_ips = line.count(",")
            ips = [line.split()[4+j].strip().strip(",").strip() for j in range(num_ips)]
            if gate_type.split("_")[0] in ['and', 'or', 'nand', 'nor']:
                new_str = gate_type.split("_")[0].upper() +str(num_ips)+"_X1 " + gate_name + " ( "
                new_str += ", ".join([f".A{n+1}({ips[n]})" for n in range(num_ips)])
                new_str+= f", .ZN({op}) )"
            elif gate_type.split("_")[0] in ['xor']:
                new_str = gate_type.split("_")[0].upper() +str(num_ips)+"_X1 " + gate_name + " ( "
                new_str += f".A({ips[0]}), .B({ips[1]}), .Z({op}) )"
            elif gate_type.split("_")[0] in ['xnor']:
                new_str = gate_type.split("_")[0].upper() +str(num_ips)+"_X1 " + gate_name + " ( "
                new_str += f".A({ips[0]}), .B({ips[1]}), .ZN({op}) )"
            elif gate_type.split("_")[0] in ['not']:
                new_str = "INV_X1 " + gate_name + " ( "
                new_str += f".A({ips[0]}), .ZN({op}) )"
            elif gate_type.split("_")[0] in ['buf']:
                new_str = "BUF_X1 " + gate_name + " ( "
                new_str += f".A({ips[0]}), .Z({op}) )"
            else:
                print("ERROR!! Found unknown gate")
            new_lines.append(new_str)
        else:
            new_lines.append(line)
    file_contents = ";\n".join(new_lines)
    with open(output_file_name,'w') as f:
        f.writelines(file_contents)
