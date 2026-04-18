import networkx as nx
import glob
import os
import multiprocessing as mp
import numpy as np
import pickle
import copy
from config import DATASET_PATH

def is_gate_line(line):
    keywords = ["not", "and", "or", "nand", "nor", "xor", "xnor", "buf"]
    if line.split(" ")[0] in keywords:
        return True
    else:
        return False

# def parse_gate(gate_str):
#     # nand NAND2_22  ( KeyWire_0[10], N122, N17 ) 
#     gate_parts = gate_str.split('(')
#     gate_name = gate_parts[0].split(" ")[1].strip()
#     gate_type = gate_parts[0].split(" ")[0].strip()
#     inputs = gate_parts[1].split(')')[0].split(',')[1:]
#     inputs = [inp.strip() for inp in inputs]
#     output = gate_parts[1].split(')')[0].split(',')[0].strip()
#     return gate_name, gate_type, inputs, output

# def build_graph_and_Components_Dict(chunk):
#     Components_Dict = {}
#     graph = nx.DiGraph()
#     for gate_str in chunk:
#         gate_name, gate_type, inputs, output = parse_gate(gate_str)
#         Components_Dict[gate_name] = [gate_type+"_gate", output] + [inp for inp in inputs]
#         graph.add_node(gate_name)
#         for inp in inputs:
#             graph.add_edge(inp, gate_name)
#         graph.add_edge(gate_name, output)
#     return graph, Components_Dict


def build_graph_and_Components_Dict(file_contents):
    Components_Dict = {}
    graph = nx.DiGraph()

    lines = file_contents.split(";")
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n"," ") for line in lines]
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            continue
        if is_gate_line(line):
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            gate_type = line.split()[0]# + "_" + str(line.count(","))
            gate_name = line.split()[1]
            op = line.split()[3].strip(",").strip()
            num_ips = line.count(",")
            ips = [line.split()[4+j].strip().strip(",").strip() for j in range(num_ips)]

            Components_Dict[gate_name] = [gate_type+"_gate", op] + [inp for inp in ips]
            graph.add_node(gate_name)
            for inp in ips:
                graph.add_edge(inp, gate_name)
            graph.add_edge(gate_name, op)
    return graph, Components_Dict

def func(variant):
    with open(variant,'r') as f:
            file_contents = f.read()
    graph, Components_Dict = build_graph_and_Components_Dict(file_contents)
    # print(variant)
    try:
        longest_path_len = nx.dag_longest_path_length(graph)
        num_gates = len(Components_Dict)
    except:
        longest_path_len = None
        num_gates = len(Components_Dict)
    return longest_path_len, num_gates

if __name__ == '__main__':
    designs = ['c432','c499','c880','IBEX','AES','GPS','MOR1KX']
    variants = []
    for design in designs:
        variants.extend(glob.glob(os.path.join(DATASET_PATH, design.upper(), "*", "*")))
    
    # det_tool = 'GNN4IP'
    # det_tool = 'Jplag'
    # det_tool = 'Sim'
    master_percent_change_in_min_longest_path_lengths = {}
    master_percent_change_in_min_num_gates = {}
    det_tools = ['GNN4IP', 'Jplag', 'Sim']
    for det_tool in det_tools:
        master_percent_change_in_min_longest_path_lengths[det_tool] = {}
        master_percent_change_in_min_num_gates[det_tool] = {}
        print(f"Against {det_tool}")
        longest_path_lengths = {}
        num_gates = {}

        no_threads=len(variants)
        # args = []
        # for i in range(len(variants)):
        #     args.append([i,variants[i],det_tools,mapping_file,mapping_strategy,random_sample_num])
        with mp.Pool(processes=no_threads) as pool:
            results = list(pool.imap(func, variants, chunksize=1))
        
        # for variant in variants:
        #     with open(variant,'r') as f:
        #         file_contents = f.read()
        #     graph, Components_Dict = build_graph_and_Components_Dict(file_contents)
        #     longest_path_len = nx.dag_longest_path_length(graph)
        #     longest_path_lengths[variant.split("/")[-2]] = longest_path_len
        for i in range(len(variants)):
            longest_path_lengths[variants[i].split("/")[-2]] = results[i][0]
            num_gates[variants[i].split("/")[-2]] = results[i][1]
        
        # print("longest_path_lengths")
        # print(longest_path_lengths)


        successful_circuits_longest_path_lengths={}
        successful_circuits_num_gates = {}
        successful_circuits_avg_longest_path_lengths={}
        successful_circuits_min_longest_path_lengths={}
        successful_circuits_min_num_gates={}
        successful_circuits = []
        for variant in variants:
            variant_name = variant.split("/")[-2]
            if variant_name.split("-")[0] in ['c432','c499','c880']:
                tmp_successful_circuits = glob.glob(os.path.join("successful_circuits", "against_"+det_tool, variant_name, "*.v"))
                for circ in tmp_successful_circuits:
                    if int(circ.split("/")[-1].split("_")[2])<1720000000:
                        successful_circuits.append(circ)
                        # print(int(circ.split("/")[-1].split("_")[2]))
            else:
                successful_circuits.extend(glob.glob(os.path.join("successful_circuits", "against_"+det_tool, variant_name, "*.v")))
        
        no_threads=32
        with mp.Pool(processes=no_threads) as pool:
            results = list(pool.imap(func, successful_circuits, chunksize=1))
        for i in range(len(successful_circuits)):
            if results[i][0] != None:
                variant_name = successful_circuits[i].split("/")[-2]
                if variant_name not in successful_circuits_longest_path_lengths:
                    successful_circuits_longest_path_lengths[variant_name] = []
                    successful_circuits_num_gates[variant_name] = []
                successful_circuits_longest_path_lengths[variant_name].append(results[i][0])
                successful_circuits_num_gates[variant_name].append(results[i][1])
        for variant_name in successful_circuits_longest_path_lengths:
            successful_circuits_avg_longest_path_lengths[variant_name] = np.average(successful_circuits_longest_path_lengths[variant_name])
            successful_circuits_min_longest_path_lengths[variant_name] = min(successful_circuits_longest_path_lengths[variant_name])
            successful_circuits_min_num_gates[variant_name] = min(successful_circuits_num_gates[variant_name])
        # print("successful_circuits_avg_longest_path_lengths")
        # print(successful_circuits_avg_longest_path_lengths)
        # print("successful_circuits_min_longest_path_lengths")
        # print(successful_circuits_min_longest_path_lengths)

        percent_change_in_min_longest_path_lengths = {}
        percent_change_in_min_num_gates = {}
        for variant_name in successful_circuits_min_longest_path_lengths:
            percent_change_in_min_longest_path_lengths[variant_name] = ((successful_circuits_min_longest_path_lengths[variant_name] - longest_path_lengths[variant_name])*100)/(longest_path_lengths[variant_name])
            percent_change_in_min_num_gates[variant_name] = ((successful_circuits_min_num_gates[variant_name] - num_gates[variant_name])*100)/(num_gates[variant_name])
        
        print("percent_change_in_min_longest_path_lengths")
        print(percent_change_in_min_longest_path_lengths)
        print("percent_change_in_min_num_gates")
        print(percent_change_in_min_num_gates)
        master_percent_change_in_min_longest_path_lengths[det_tool] = copy.deepcopy(percent_change_in_min_longest_path_lengths)
        for variant_name in percent_change_in_min_longest_path_lengths:
            master_percent_change_in_min_longest_path_lengths[det_tool][variant_name] = [master_percent_change_in_min_longest_path_lengths[det_tool][variant_name], num_gates[variant_name]]
        master_percent_change_in_min_num_gates[det_tool] = copy.deepcopy(percent_change_in_min_num_gates)
        for variant_name in percent_change_in_min_num_gates:
            master_percent_change_in_min_num_gates[det_tool][variant_name] = [master_percent_change_in_min_num_gates[det_tool][variant_name], num_gates[variant_name]]
        # print("average:", np.average(list(percent_change_in_min_longest_path_lengths.values())))
        arr = []
        arr_wo_c499 = []
        w_arr = []
        w_arr_wo_c499 = []
        for variant_name in percent_change_in_min_longest_path_lengths:
            if "c499" not in variant_name:
                arr_wo_c499.append(percent_change_in_min_longest_path_lengths[variant_name])
                w_arr_wo_c499.append(num_gates[variant_name])    
            arr.append(percent_change_in_min_longest_path_lengths[variant_name])
            w_arr.append(num_gates[variant_name])
        print("average:", np.average(arr))
        print("average w/o c499:", np.average(arr_wo_c499))
        print("weighted average:", np.average(arr,weights=w_arr))
        print("weighted average w/o c499:", np.average(arr_wo_c499,weights=w_arr_wo_c499))

        
        # print("percent_change_in_min_num_gates")
        # print(percent_change_in_min_num_gates)
        # print(np.average(list(percent_change_in_min_num_gates.values())))
    with open("./master_percent_change_in_min_longest_path_lengths.pkl",'wb') as f:
        pickle.dump(master_percent_change_in_min_longest_path_lengths,f)
    with open("./master_percent_change_in_min_num_gates.pkl",'wb') as f:
        pickle.dump(master_percent_change_in_min_num_gates,f)