def is_gate_line(line):
    keywords = ["not", "and", "or", "nand", "nor", "xor", "xnor", "buf"]
    if line.split(" ")[0] in keywords:
        return True
    else:
        return False

def convert_to_assign(file_contents,output_file_name):
    lines = file_contents.split(";")
    # Remove whitespace and empty lines
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n"," ") for line in lines]
    new_lines = []
    xnor_inter_wires_to_add = []
    for line in lines:
        # line_counter+=1
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            new_lines.append(line)
            continue
        if is_gate_line(line):
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            gate_type = line.split(" ")[0] + "_" + str(line.count(","))
            # gate_name = line.split()[1].strip()
            op = line.split()[3].strip(",").strip()
            num_ips = line.count(",")
            ips = [line.split()[4+j].strip().strip(",").strip() for j in range(num_ips)]

            # if gate_type.split("_")[0] not in ['and', 'nand', 'nor', 'or', 'not', 'buf', 'xor', 'xnor']:
            #     print("Found unknown gate type:", gate_type)
            # else:
            if gate_type.split("_")[0] == 'and':
                new_str = "assign " + op + " = " + " && ".join(ips)
            elif gate_type.split("_")[0] == 'nand':
                # new_str = "assign " + op + " = " + " ~(" + " && ".join(ips) + ")"
                # new_str = "assign " + op + " = " + " !(" + " && ".join(ips) + ")"
                new_ips = ["!"+ip for ip in ips]
                new_str = "assign " + op + " = "  + " && ".join(new_ips)
            elif gate_type.split("_")[0] == 'or':
                new_str = "assign " + op + " = " + " || ".join(ips)
            elif gate_type.split("_")[0] == 'nor':
                # new_str = "assign " + op + " = " + " ~(" + " || ".join(ips) + ")"
                # new_str = "assign " + op + " = " + " !(" + " || ".join(ips) + ")"
                new_ips = ["!"+ip for ip in ips]
                new_str = "assign " + op + " = "  + " || ".join(new_ips)
            elif gate_type.split("_")[0] == 'xor':
                new_str = "assign " + op + " = " +  " ^ ".join(ips)
            elif gate_type.split("_")[0] == 'xnor':
                # new_str = "assign " + op + " = " + " ~(" + " ^ ".join(ips) + ")"
                # new_str = "assign " + op + " = " + " !(" + " ^ ".join(ips) + ")"
                # new_str = "assign " + op + " = " + " ^~ ".join(ips)
                new_str = "assign " + op+"_inter" + " = " + " ^ ".join(ips) + ";\n"
                xnor_inter_wires_to_add.append(op+"_inter")
                new_str+= "assign " + op + " = " + " !" + op+"_inter"
            elif gate_type.split("_")[0] == 'not':
                # new_str = "assign " + op + " = " + " ~" + ips[0]
                new_str = "assign " + op + " = " + " !" + ips[0]
            elif gate_type.split("_")[0] == 'buf':
                new_str = "assign " + op + " = " + op
            else:
                print("ERROR! Found unknown gate type:", gate_type)
            new_lines.append(new_str)
        else:
            new_lines.append(line)
    if len(xnor_inter_wires_to_add)>0:
        for i in range(len(new_lines)):
            line = new_lines[i]
            if line.split()[0] == 'wire':
                new_lines[i] = line + ";\n" + "wire " + ", ".join(xnor_inter_wires_to_add)
                break
    file_contents = ";\n".join(new_lines)
    with open(output_file_name,'w') as f:
        f.writelines(file_contents)
if __name__ == '__main__':
    with open("./del/topModule.v",'r') as f:
        file_contents = f.read()
    output_file_name = "./del/topModule_assigns.v"
    convert_to_assign(file_contents,output_file_name)
