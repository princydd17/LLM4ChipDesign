#import networkx as nx

def NanGate_to_generic_gates(gt):
    if gt[:3] == 'AND':
        return "and"
    elif gt[:4] == 'NAND':
        return "nand"
    elif gt[:2] == 'OR':
        return "or"
    elif gt[:3] == 'NOR':
        return "nor"
    elif gt[:3] == 'INV':
        return "not"
    elif gt[:4] == 'XOR2':
        return "xor"
    elif gt[:5] == 'XNOR2':
        return "xnor"
    elif gt[:3] == 'BUF':
        return "buf"
    else:
        print("ERROR!! Found unknown gate")


'''
def parse_NanGate_mapped_netlist(v_file_path):
    with open(v_file_path,'r') as f:
        file_contents = f.read()
    lines = file_contents.split(";")
    for i in range(len(lines)):
            lines[i] = lines[i].strip()

    for i in range(len(lines)):
        if "input " in lines[i]:
            inp_ln = i
        if "output " in lines[i]:
            op_ln = i
        if "wire " in lines[i]:
            wire_ln = i
        if "endmodule" in lines[i]:
            end_ln = i

    inputs = [i.strip() for i in lines[inp_ln].split("input ")[1].split(",")]
    outputs = [i.strip() for i in lines[op_ln].split("output ")[1].split(",")]
    wires = [i.strip() for i in lines[wire_ln].split("wire ")[1].split(",")]
    wires = list(set(wires).difference(set(inputs+outputs)))

    Components_Dict = {}
    for i in range(wire_ln+1,end_ln):
        if ("," in lines[i]) and ("(" in lines[i]) and (")" in lines[i]):
            instance_name = lines[i].split(" ")[1]
            gate_type = lines[i].split(" ")[0]
            Components_Dict[instance_name] = [gate_type]
            num_ports = lines[i].count(".")
            for j in range(num_ports):
                Components_Dict[instance_name].append(lines[i].split(" ")[j+3][lines[i].split(" ")[j+3].index("(")+1:lines[i].split(" ")[j+3].index(")")])


    G = nx.DiGraph()
    G.add_nodes_from(inputs)
    G.add_nodes_from(outputs)
    G.add_nodes_from(wires)
    G.add_nodes_from(list(Components_Dict.keys()))

    for node in Components_Dict:
        ips = Components_Dict[node][1:-1]
        output = Components_Dict[node][-1]
        for i in ips:
            G.add_edge(i,node)
        G.add_edge(node,output)

    return G, inputs, wires, outputs, Components_Dict
'''

def convert_to_generic(v_file_path,output_file_name):
    with open(v_file_path,'r') as f:
        file_contents = f.read()
    lines = file_contents.split(";")
    for i in range(len(lines)):
            lines[i] = lines[i].strip()

    for i in range(len(lines)):
        if "input " in lines[i]:
            inp_ln = i
        if "output " in lines[i]:
            op_ln = i
        if "wire " in lines[i]:
            wire_ln = i
        if "endmodule" in lines[i]:
            end_ln = i

    inputs = [i.strip() for i in lines[inp_ln].split("input ")[1].split(",")]
    outputs = [i.strip() for i in lines[op_ln].split("output ")[1].split(",")]
    wires = [i.strip() for i in lines[wire_ln].split("wire ")[1].split(",")]
    wires = list(set(wires).difference(set(inputs+outputs)))

    Components_Dict = {}
    for i in range(wire_ln+1,end_ln):
        if ("," in lines[i]) and ("(" in lines[i]) and (")" in lines[i]):
            instance_name = lines[i].split(" ")[1]
            gate_type = lines[i].split(" ")[0]
            Components_Dict[instance_name] = [gate_type]
            num_ports = lines[i].count(".")
            for j in range(num_ports):
                Components_Dict[instance_name].append(lines[i].split(" ")[j+3][lines[i].split(" ")[j+3].index("(")+1:lines[i].split(" ")[j+3].index(")")])

    out_v_lines = 'module ' + 'top' + " ( " + ', '.join(inputs + outputs) + " );\n"
    out_v_lines += 'input ' + ", ".join(inputs) + ";\n"
    out_v_lines += 'output ' + ", ".join(outputs) + ";\n"
    out_v_lines += 'wire ' + ", ".join(wires) + ";\n\n"
    for node in Components_Dict:
        ips = Components_Dict[node][1:-1]
        op = Components_Dict[node][-1]
        gt = Components_Dict[node][0]
        generic_gt = NanGate_to_generic_gates(gt)
        out_v_lines+= generic_gt + " " + node + " ( " + op + ", " + ", ".join(ips) + " );\n"
    out_v_lines+='endmodule'


    with open(output_file_name,'w') as f:
        f.writelines(out_v_lines)
    #return "./tmp/orig_with_resyn_cone_generic.v"

'''
def convert_to_generic(inputs, wires, outputs, Components_Dict):
    out_v_lines = 'module ' + 'top' + " ( " + ', '.join(inputs + outputs) + " );\n"
    out_v_lines += 'input ' + ", ".join(inputs) + ";\n"
    out_v_lines += 'output ' + ", ".join(outputs) + ";\n"
    out_v_lines += 'wire ' + ", ".join(wires) + ";\n\n"
    for node in Components_Dict:
        ips = Components_Dict[node][1:-1]
        op = Components_Dict[node][-1]
        gt = Components_Dict[node][0]
        generic_gt = NanGate_to_generic_gates(gt)
        out_v_lines+= generic_gt + " " + node + " ( " + op + ", " + ", ".join(ips) + " );\n"
    out_v_lines+='endmodule'
    return out_v_lines
'''


if __name__ == '__main__':
    #G, inputs, wires, outputs, Components_Dict = parse_NanGate_mapped_netlist("./tmp_NanGate.v")
    # out_v_lines = convert_to_generic(inputs, wires, outputs, Components_Dict)
    out_v_lines = convert_to_generic("./mor1kx_final.v","./mor1kx_final_generic.v")
    #print(out_v_lines)
    