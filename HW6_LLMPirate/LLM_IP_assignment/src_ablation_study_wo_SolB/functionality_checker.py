#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:36:36 2024

@author: gohil.vasudev
"""

'''
This file is for reading a verilog netlist, converting it into a networkx graph
 and then simulating it
'''

import networkx as nx
import random

def not_gate(a):
    return int(abs(1-a[0]))
def buf_gate(a):
    return int(a[0])
def and_gate(a):
    return int(all(a))
def or_gate(a):
    return int(any(a))
def nand_gate(a):
    return int(not all(a))
def nor_gate(a):
    return int(not any(a))
def xor_gate(a):
    return sum(a)%2
def xnor_gate(a):
    return int(not xor_gate(a))

def parse_gate(gate_str):
    gate_parts = gate_str.split('(')
    gate_name = gate_parts[0].split(" ")[1].strip()
    gate_type = gate_parts[0].split(" ")[0].strip()
    inputs = gate_parts[1].split(')')[0].split(',')[1:]
    inputs = [inp.strip() for inp in inputs]
    output = gate_parts[1].split(')')[0].split(',')[0].strip()
    return gate_name, gate_type, inputs, output


def get_input_nodes(graph):
    return [node for node in graph.nodes() if graph.in_degree(node) == 0]

def get_output_nodes(graph):
    return [node for node in graph.nodes() if graph.out_degree(node) == 0]

def build_graph_and_Components_Dict(chunk):
    Components_Dict = {}
    graph = nx.DiGraph()
    for gate_str in chunk:
        gate_name, gate_type, inputs, output = parse_gate(gate_str)
        Components_Dict[gate_name] = [gate_type+"_gate", output] + [inp for inp in inputs]
        graph.add_node(gate_name)
        for inp in inputs:
            graph.add_edge(inp, gate_name)
        graph.add_edge(gate_name, output)
    return graph, Components_Dict

def build_graph_and_Components_Dict_from_circuit(circuit_str, restrict_gate_type, target_gate_types):
    Components_Dict = {}
    graph = nx.DiGraph()
    circuit_lines = circuit_str.split("\n")
    circuit_lines = [l for l in circuit_lines if l!='']
    gate_ctr = 0
    error_msg = None
    for gate_str in circuit_lines:
        gate_type = gate_str.split("=")[-1].split("(")[0].strip()
        if restrict_gate_type:
            if gate_type not in target_gate_types + ['NOT'] + ['BUF']:
                error_msg = 'The circuit contains Boolean operators other than the ' + ", ".join(target_gate_types) + ' operator(s).'
                return None, None, error_msg
        gate_name = "my_gate_"+str(gate_ctr)
        gate_ctr+=1
        inputs = gate_str.split("(")[-1].split(')')[0].split(',')
        inputs = [inp.strip() for inp in inputs]
        output = gate_str.split("=")[0].strip()
        Components_Dict[gate_name] = [gate_type.lower()+"_gate", output] + [inp for inp in inputs]
        graph.add_node(gate_name)
        for inp in inputs:
            graph.add_edge(inp, gate_name)
        graph.add_edge(gate_name, output)
    return graph, Components_Dict, error_msg


def simulate_logic(Components_Dict,graph,node_values):
    # node_values = {}
    for node in nx.topological_sort(graph):
        # if node in input_nodes:
        #     node_values[node] = random.choice([0, 1])
        # elif node in Components_Dict:
        if node in Components_Dict:
            ips = Components_Dict[node][2:]
            op = Components_Dict[node][1]
            node_values[op] = globals()[Components_Dict[node][0]]([node_values[i] for i in ips])
    return node_values

def check_netlist_functionality(chunk,chunk_rephrased,num_test_vectors):
    graph_orig, Components_Dict_orig = build_graph_and_Components_Dict(chunk)
    graph_rephrased, Components_Dict_rephrased = build_graph_and_Components_Dict(chunk_rephrased)


    input_nodes_orig = get_input_nodes(graph_orig)
    input_nodes_rephrased = get_input_nodes(graph_rephrased)
    if set(input_nodes_orig) != set(input_nodes_rephrased):
        # print("ERROR! Rephrased inputs are not the same as original inputs")
        functional_status = "Error running simulation. ERROR! Rephrased inputs are not the same as original inputs"
        return functional_status

    output_nodes_orig = get_output_nodes(graph_orig)
    output_nodes_rephrased = get_output_nodes(graph_rephrased)
    if set(output_nodes_orig) != set(output_nodes_rephrased):
        # print("ERROR! Rephrased outputs are not the same as original outputs")
        functional_status = "Error running simulation. ERROR! Rephrased outputs are not the same as original outputs"
        return functional_status

    functionally_equivalent = True
    for n in range(num_test_vectors):
        # if functionally_equivalent == False:
        #     functional_status = "Error running simulation. The chunks are not equivalent"
        #     return functional_status
        node_values_orig = {}
        node_values_rephrased = {}
        for inp in input_nodes_orig:
            val = random.choice([0,1])
            node_values_orig[inp] = val
            node_values_rephrased[inp] = val
        # node_values = random.choices([0,1],k=len(input_nodes))
        ## Simulation

        node_values_orig = simulate_logic(Components_Dict_orig, graph_orig, node_values_orig)
        node_values_rephrased = simulate_logic(Components_Dict_rephrased, graph_rephrased, node_values_rephrased)

        if node_values_orig != node_values_rephrased:
            # print("ERROR! Rephrased chunk is not functionally equivalent to the original chunk")
            functionally_equivalent = False
            functional_status = "Error running simulation. ERROR! Rephrased chunk is not functionally equivalent to the original chunk"
            return functional_status
        # else:
        #     print("Rephrased chunk is functionally equivalent to the original chunk")
    if functionally_equivalent == True:
        functional_status = "Simulation successful. Chunks are functionally equivalent"

    return functional_status


def check_LLM_circuit_functionality(template,LLM_circuit,num_test_vectors,target_gate_types):
    graph_orig, Components_Dict_orig, error_msg = build_graph_and_Components_Dict_from_circuit(template,False,None)
    graph_rephrased, Components_Dict_rephrased, error_msg = build_graph_and_Components_Dict_from_circuit(LLM_circuit, True, target_gate_types)
    if error_msg != None:
        functional_status = 'Error parsing circuit. ERROR! Rephrased circuit contains Boolean operators other than the ' + ", ".join(target_gate_types) + ' operator(s).'
        return functional_status

    input_nodes_orig = get_input_nodes(graph_orig)
    input_nodes_rephrased = get_input_nodes(graph_rephrased)
    if set(input_nodes_orig) != set(input_nodes_rephrased):
        functional_status = "Error running simulation. ERROR! Rephrased inputs are not the same as original inputs"
        return functional_status

    output_nodes_orig = get_output_nodes(graph_orig)
    output_nodes_rephrased = get_output_nodes(graph_rephrased)
    if set(output_nodes_orig) != set(output_nodes_rephrased):
        functional_status = "Error running simulation. ERROR! Rephrased outputs are not the same as original outputs"
        return functional_status

    functionally_equivalent = True
    for n in range(num_test_vectors):
        node_values_orig = {}
        node_values_rephrased = {}
        for inp in input_nodes_orig:
            val = random.choice([0,1])
            node_values_orig[inp] = val
            node_values_rephrased[inp] = val
        ## Simulation
        node_values_orig = simulate_logic(Components_Dict_orig, graph_orig, node_values_orig)
        node_values_rephrased = simulate_logic(Components_Dict_rephrased, graph_rephrased, node_values_rephrased)

        if not all(node_values_orig.get(key) == node_values_rephrased.get(key) for key in output_nodes_orig): # Comparing only the output node because the intermediate nodes may be different
        # if node_values_orig != node_values_rephrased:
            functionally_equivalent = False
            functional_status = "Error running simulation. ERROR! Rephrased circuit is not functionally equivalent to the original circuit"
            return functional_status
    if functionally_equivalent == True:
        functional_status = "Simulation successful. The two circuits are functionally equivalent"

    return functional_status


def check_LLM_circuit_functionality_for_ablation_study_wo_SolB(template,LLM_circuit,num_test_vectors,target_gate_types):
    graph_orig, Components_Dict_orig, error_msg = build_graph_and_Components_Dict_from_circuit(template,False,None)
    graph_rephrased, Components_Dict_rephrased, error_msg = build_graph_and_Components_Dict_from_circuit(LLM_circuit, False, None)
    # print(graph_orig.nodes())
    # print(graph_rephrased.nodes())
    # exit()
    if error_msg != None:
        functional_status = 'Error parsing circuit. ERROR! Rephrased circuit contains Boolean operators other than the ' + ", ".join(target_gate_types) + ' operator(s).'
        return functional_status

    input_nodes_orig = get_input_nodes(graph_orig)
    input_nodes_rephrased = get_input_nodes(graph_rephrased)
    if set(input_nodes_orig) != set(input_nodes_rephrased):
        functional_status = "Error running simulation. ERROR! Rephrased inputs are not the same as original inputs"
        return functional_status

    output_nodes_orig = get_output_nodes(graph_orig)
    output_nodes_rephrased = get_output_nodes(graph_rephrased)
    if set(output_nodes_orig) != set(output_nodes_rephrased):
        functional_status = "Error running simulation. ERROR! Rephrased outputs are not the same as original outputs"
        return functional_status
    # print("Reached here")
    functionally_equivalent = True
    for n in range(num_test_vectors):
        node_values_orig = {}
        node_values_rephrased = {}
        for inp in input_nodes_orig:
            val = random.choice([0,1])
            node_values_orig[inp] = val
            node_values_rephrased[inp] = val
        ## Simulation
        try:
            node_values_orig = simulate_logic(Components_Dict_orig, graph_orig, node_values_orig)
        except:
            return "Error running simulation. The Boolean format of the original circuit contains a cycle."
        # print("Reached here too")
        node_values_rephrased = simulate_logic(Components_Dict_rephrased, graph_rephrased, node_values_rephrased)
        # print("Reached here also")

        if not all(node_values_orig.get(key) == node_values_rephrased.get(key) for key in output_nodes_orig): # Comparing only the output node because the intermediate nodes may be different
        # if node_values_orig != node_values_rephrased:
            functionally_equivalent = False
            functional_status = "Error running simulation. ERROR! Rephrased circuit is not functionally equivalent to the original circuit"
            return functional_status
    if functionally_equivalent == True:
        functional_status = "Simulation successful. The two circuits are functionally equivalent"

    return functional_status


if __name__ == '__main__':

    template = 'Y = AND(A1, A2, A3)'
    LLM_circuit = 'Y_intermediate1 = NOR(A1, A1)\nY_intermediate2 = NOR(A2, A2)\nY_intermediate3 = NOR(A3, A3)\nY = NOR(Y_intermediate1, Y_intermediate2, Y_intermediate3)'
    num_test_vectors = 2**10
    target_gate_types = ['NOR']
    functional_status = check_LLM_circuit_functionality(template,LLM_circuit,num_test_vectors,target_gate_types)
    print(functional_status)

    '''

    chunk = ['and g270 ( new_n378_, new_n377_, new_n325_, new_n331_ )',
     'or g271 ( N431, new_n378_, new_n372_, new_n374_ )',
     'not g272 ( new_n380_, new_n319_ )',
     'not g273 ( new_n381_, new_n331_ )',
     'not g274 ( new_n382_, new_n338_ )',
     'not g275 ( new_n383_, new_n342_ )',
     'and g276 ( new_n384_, new_n361_, new_n382_, new_n383_ )',
     'or g277 ( new_n385_, new_n377_, new_n384_, new_n381_ )',
     'and g278 ( new_n386_, new_n385_, new_n325_ )',
     'or g279 ( N432, new_n386_, new_n380_ )']


    graph_orig, Components_Dict_orig = build_graph_and_Components_Dict(chunk)
    graph_rephrased, Components_Dict_rephrased = build_graph_and_Components_Dict(chunk)


    input_nodes_orig = get_input_nodes(graph_orig)
    input_nodes_rephrased = get_input_nodes(graph_rephrased)
    if set(input_nodes_orig) != set(input_nodes_rephrased):
        print("ERROR! Rephrased inputs are not the same as original inputs")

    output_nodes_orig = get_output_nodes(graph_orig)
    output_nodes_rephrased = get_output_nodes(graph_rephrased)
    if set(output_nodes_orig) != set(output_nodes_rephrased):
        print("ERROR! Rephrased outputs are not the same as original outputs")

    node_values_orig = {}
    node_values_rephrased = {}
    for inp in input_nodes_orig:
        val = random.choice([0,1])
        node_values_orig[inp] = val
        node_values_rephrased[inp] = val
    # node_values = random.choices([0,1],k=len(input_nodes))
    ## Simulation

    node_values_orig = simulate_logic(Components_Dict_orig, graph_orig, node_values_orig)
    node_values_rephrased = simulate_logic(Components_Dict_rephrased, graph_rephrased, node_values_rephrased)

    if node_values_orig != node_values_rephrased:
        print("ERROR! Rephrased chunk is not functionally equivalent to the original chunk")
    else:
        print("Rephrased chunk is functionally equivalent to the original chunk")

    # print("Input values:")
    # for node, value in node_values_orig.items():
    #     if node in input_nodes_orig:
    #         print(f"{node}: {value}")

    # print("Output values:")
    # for node, value in node_values_orig.items():
    #     if node in output_nodes_orig:
    #         print(f"{node}: {value}")
    '''
