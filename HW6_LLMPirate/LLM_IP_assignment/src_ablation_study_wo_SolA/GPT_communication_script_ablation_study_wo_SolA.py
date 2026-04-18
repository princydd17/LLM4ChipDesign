#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:22:49 2024

@author: gohil.vasudev
"""


import os, copy, time, glob, pickle
import sys
sys.path.insert(0, '../src')
from config import DATASET_PATH
import re
import random
import requests
from tqdm import tqdm
from functionality_checker import check_LLM_circuit_functionality, check_LLM_circuit_functionality_for_ablation_study_wo_SolA
from characterize_circuit import characterize_generic_netlist, create_LLM_circuit_query_template, convert_circuit_to_Boolean_format, convert_circuit_from_Boolean_format
from circuit_decomposer import final_decompose_expression
import openai
import subprocess

class ChatGPT3p5():
    """ChatGPT Large Language Model."""

    def __init__(self):
        # openai.api_key="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"
        # key_for_LLMPirate_revision
        openai.api_key="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"

    def generate(self, messages, seed=None,temperature=0.7):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            seed=seed, # For deterministic outputs
            temperature=temperature  # For deterministic outputs
        )
        return response.choices[0].message.content

def my_continue_conversation(message):
    # Conversation
    print("You: ", end="",flush=True)
    for word in message:
        print(word, end="", flush=True)
    print("\n")

    print("GPT 3.5:", end="", flush=True)
    my_response = ""
    messages.append({"role": "user", "content": message})
    response = model.generate(messages)
    messages.append({"role": "assistant", "content": response})
    print(response, end="", flush=True)
    my_response+=response
    print("\n")

    # response = await sydney.ask(message)
    # print(response, end="", flush=True)
    # print("\n")
    return my_response

def get_circuit_from_response(response):
    LLM_circuit = ""
    if "```" in response:
        lines = response.split("```")[1].split("\n")
        lines = [l for l in lines if l!='']
        for line in lines:
            if ("=" in line) and (not line.startswith("wire ")): # Added the second condition because sometimes CoPilot generates "wire N1 = ..." statements
                tmp_expression = line.split("=")[-1].strip().strip(";")# line.strip().strip(";").split("=")[-1].strip()
                if(("AND " in tmp_expression) or ("OR " in tmp_expression) or ("NAND " in tmp_expression) or ("NOR " in tmp_expression) or ("XOR " in tmp_expression) or ("XNOR " in tmp_expression)):
                    return "Incorrect format"
                tmp_op_net = line.split("=")[0].strip()
                decomposed_lines_str = final_decompose_expression(tmp_expression,tmp_op_net)
                LLM_circuit+=decomposed_lines_str+"\n"
                # LLM_circuit+= line.strip().strip(";")+"\n"
            # else:
            #     my_print("ERROR! Unable to parse the response")
            #     exit()
        LLM_circuit = LLM_circuit[:-1]
    elif "=" in response:
        lines = response.split("\n")
        for line in lines:
            if ("=" in line) and (not line.startswith("wire ")): # Added the second condition because sometimes CoPilot generates "wire N1 = ..." statements
                tmp_expression = line.split("=")[-1].strip().strip(";") # line.strip().strip(";").split("=")[-1].strip()
                if(("AND " in tmp_expression) or ("OR " in tmp_expression) or ("NAND " in tmp_expression) or ("NOR " in tmp_expression) or ("XOR " in tmp_expression) or ("XNOR " in tmp_expression)):
                    return "Incorrect format"
                tmp_op_net = line.split("=")[0].strip()
                decomposed_lines_str = final_decompose_expression(tmp_expression,tmp_op_net)
                LLM_circuit+=decomposed_lines_str+"\n"
                # LLM_circuit+= line.strip().strip(";")+"\n"
        LLM_circuit = LLM_circuit[:-1]
    else:
        my_print("ERROR! Unable to parse the response")
        exit()
    return LLM_circuit

def get_circuit_response_for_ablation_study_wo_SolA(response):
    LLM_circuit = ""
    if "```" in response:
        lines = response.split("```")[1].split("\n")
        lines = [l for l in lines if l!='']
    elif ("module " in response) and ("endmodule" in response):
        lines = response.split("endmodule")[0].split("module ")[1].split("\n")
        lines = [l for l in lines if l!='']
        LLM_circuit = 'module '
        for line in lines:
            LLM_circuit+=line+"\n"
        LLM_circuit += "endmodule"
        return LLM_circuit
    # elif "=" in response:
    #     lines = response.split("\n")
    else:
        my_print("ERROR! Unable to parse the response")
        return "Incorrect format"
    for line in lines:
        LLM_circuit+=line+"\n"
    return LLM_circuit
    


def my_print(*args, **kwargs):
    elapsed_time = time.time() - start_time
    log_message = f"[{elapsed_time:.2f}s] {' '.join(map(str, args))}"
    # Print to the console
    print(log_message, **kwargs)



if __name__ == "__main__":
    start_time = time.time()

    model = ChatGPT3p5()
    MOSS_thresh = 0.2
    GNN4IP_thresh = 0

    designs = ['c880','c432','c499']
    rank = 0
    num_test_vectors = 2**10

    total_design_count = 0
    functional_count = 0
    GNN4IP_successful_count = 0
    MOSS_successful_count = 0
    # all_gate_types = ['and_2', 'and_3', 'and_4', 'and_5', 'and_8', 'and_9', 'buf_1', 'nand_2', 'nand_3', 'nand_4', 'nor_2', 'nor_3', 'nor_4', 'not_1', 'or_2', 'or_3', 'or_4', 'xnor_2', 'xor_2']
    # circuit_query_templates = create_LLM_circuit_query_template(all_gate_types)
    # target_mapping_gates_dict = {'and':[['NOR'], ['NAND'], ['OR','NOT']],\
    #                         'or':[['NOR'], ['NAND'], ['AND','NOT']],\
    #                         'nor':[['NAND'], ['AND','NOT'], ['OR','NOT']],\
    #                         'nand':[['NOR'], ['AND','NOT'], ['OR','NOT']],\
    #                         'xor':[['NOR'], ['NAND']],\
    #                         'xnor':[['NOR'], ['NAND']],\
    #                         }
    

    # if not os.path.exists("./cached_circuit_mapping_GPT3dot5.pkl"):
    #     cached_circuit_mapping = {}
    #     for gate_type in all_gate_types:
    #         cached_circuit_mapping[gate_type] = {}
    #     with open("./cached_circuit_mapping_GPT3dot5.pkl",'wb') as f:
    #         pickle.dump(cached_circuit_mapping,f)
    # with open("./cached_circuit_mapping_GPT3dot5.pkl",'rb') as f:
    #     cached_circuit_mapping = pickle.load(f)


    variants = []
    for design in designs:
        variants.extend(glob.glob(os.path.join(DATASET_PATH, design.upper(), "*")))
    
    for idx in range(len(variants)):
        variant_name = variants[idx].split("/")[-1]
        # generic_version_of_current_circuit = copy.deepcopy(variants[idx])+"/topModule.v"
        my_print("Current variant: " + variants[idx])
        with open(variants[idx]+"/topModule.v",'r') as f:
            file_contents = f.read()
        circ_in_Boolean_format, remaining_orig_lines = convert_circuit_to_Boolean_format(file_contents)
        # circ_in_Boolean_format = 'N854 = NOT(KeyNOTWire_0[13])\nN855 = NOT(N846)\nN856 = NOT(N847)\nN857 = NOT(N848)\nN858 = NOT(N849)\nN859 = NOR(N417, N851)\nN860 = NOR(N332, N852)\nN861 = NOR(N333, N853)'
        try:
            messages = []

            message = "Can you refactor this Verilog circuit following these instructions? 1) Ensure that the final functionality remains the same but the Boolean operators are different. 2) Just give me the new circuit and nothing else.\n"
            # message +=circ_in_Boolean_format
            message+= file_contents

            # print(message)
            # print("\n")

            num_trials = 1
            max_num_trials = 5
            while num_trials<=max_num_trials:
                format_error = False
                my_print("Trial number " + str(num_trials))
                response = my_continue_conversation(message)
                # response = copy.deepcopy(circ_in_Boolean_format)
                my_print("Got response")
                # print(response)
                # print("\n")

                # LLM_circuit = get_circuit_from_response(response)
                LLM_circuit = get_circuit_response_for_ablation_study_wo_SolA(response)
                my_print("Got LLM circuit")
                if "Incorrect format" in LLM_circuit:
                    my_print("Incorrect Formatting.")
                    message = "This is not the correct format. Can you try again. Just give me the new circuit and nothing else."
                    # message+= template
                    num_trials+=1
                    format_error = True
                
                else:
                    LLM_circ_in_Boolean_format, LLM_remaining_lines = convert_circuit_to_Boolean_format(LLM_circuit)
                    # circ_in_orig_format_file_contents = convert_circuit_from_Boolean_format(LLM_circuit,remaining_orig_lines)
                    # my_print("Converted circuit")
                    # print(circ_in_orig_format_file_contents)
                    # exit()
                
                
                    # functional_status = check_LLM_circuit_functionality(template,LLM_circuit,num_test_vectors,target_mapping_gates)
                    functional_status = check_LLM_circuit_functionality_for_ablation_study_wo_SolA(circ_in_Boolean_format,LLM_circ_in_Boolean_format,num_test_vectors,None)
                
                # if (("error parsing circuit" in functional_status.lower()) and (format_error == False)):
                #     my_print(functional_status)
                #     message = 'This is not correct because the refactored circuit contains Boolean operators other than the ' + ", ".join(target_mapping_gates) + ' operator(s). Can you try again? Below is the original circuit:\n'
                #     message+= template
                #     num_trials+=1
                if (format_error == False) and ("the boolean format of the original circuit contains a cycle" in functional_status.lower()):
                    my_print(functional_status)
                    exit()

                if (format_error == False) and ("error running simulation" in functional_status.lower()):
                    my_print(functional_status)
                    message = "This is not correct because the functionality is not the same as the original circuit. Can you try again?"
                    # message+= template
                    num_trials+=1
                elif (format_error == False) and ("simulation successful" in functional_status.lower()):
                    my_print(functional_status)
                    break
                
            
            if "simulation successful" in functional_status.lower():
                my_print("Found successful rephrased circuit for " + variant_name + ". It is as follows:")
                # print(circ_in_orig_format_file_contents)
                print(LLM_circuit)
                my_print("Caching it for future use")
                # exit()
                # if "_".join(target_mapping_gates) in cached_circuit_mapping[gate_type]:
                #     cached_circuit_mapping[gate_type]["_".join(target_mapping_gates)].append(LLM_circuit)
                # else:
                #     cached_circuit_mapping[gate_type]["_".join(target_mapping_gates)] = [LLM_circuit]
                # with open("./cached_circuit_mapping_GPT3dot5.pkl",'wb') as f:
                #     pickle.dump(cached_circuit_mapping,f)
            else:
                my_print("NOTE: Tried " + str(max_num_trials) + " times but no success in generating functionally equivalent circuit. Moving on to the next gate type.")
                # exit()
        except Exception as ex:
            my_print("Something went wrong: ")
            my_print(ex)
            # exit()



    '''
    for gate_type in all_gate_types:#['and_2']:#[1:2]:
        if gate_type not in ['not_1', 'buf_1'] and int(gate_type.split("_")[-1])<=5: # because there is no point in changing simple not gates and buffers
            for target_mapping_gates in target_mapping_gates_dict[gate_type.split("_")[0]]:
                try:
                    messages = []
                    template = circuit_query_templates[gate_type]
                    my_print("Current gate_type: " + gate_type)
                    my_print("Target mapping gates:", target_mapping_gates)
                    if len(target_mapping_gates)==1:
                        mapping_gate_rule_str = "Use only the " + target_mapping_gates[0] + " Boolean operator."
                    else:
                        mapping_gate_rule_str = "Use only " + " and/or ".join(target_mapping_gates) + " Boolean operators."
                    # message = "Can you refactor this Verilog circuit following these instructions? 1) Use only the "+target_mapping_gate+" Boolean operator. 2) Ensure that the final functionality remains the same. 3) Just give me the new circuit and nothing else. 4) Generate your response in the following format: Y = <gate type> (<inputs>). 5) Generate each gate in a new line and add intermediate operands if necessary.\n"
                    # message = "Can you refactor this Verilog circuit following these instructions? 1) Use only the "+target_mapping_gate+" Boolean operator. 2) Ensure that the final functionality remains the same. 3) Just give me the new circuit and nothing else. 4) Generate your response in the following format: <output> = <gate type> (<inputs>). 5) Generate each gate in a new line and add intermediate operands if necessary.\n"
                    # message = "Can you refactor this Verilog circuit following these instructions? 1) " + mapping_gate_rule_str + " 2) Ensure that the final functionality remains the same. 3) Just give me the new circuit and nothing else. 4) Generate your response in the following format: <output> = <gate type> (<inputs>). 5) Generate each gate in a new line and add intermediate operands if necessary.\n" # This prompt is a good starting point. It works reasonably well
                    message = "Can you refactor this Verilog circuit following these instructions? 1) " + mapping_gate_rule_str + " 2) Ensure that the final functionality remains the same. 3) Just give me the new circuit and nothing else. 4) Generate your response in the following format: <output> = <gate type> (<inputs>).\n"  # This prompt is a also good starting point. It works reasonably well and it also works for and_3 gates
                    # message = "Can you refactor this Verilog circuit following these instructions? 1) " + mapping_gate_rule_str + " 2) Ensure that the final functionality remains the same. 3) Just give me the new circuit and nothing else. 4) Generate your response in the following format: <output> = <gate type> (<inputs>). 5) Each line should contain only one Boolean operator.\n"
                    message += template

                    num_trials = 1
                    max_num_trials = 5
                    while num_trials<=max_num_trials:
                        format_error = False
                        my_print("Trial number " + str(num_trials))
                        response = my_continue_conversation(message)

                        LLM_circuit = get_circuit_from_response(response)
                        if "Incorrect format" in LLM_circuit:
                            my_print("Incorrect Formatting.")
                            message = "This is not the correct format. Can you try again in this format: <output> =  <gate type> (<inputs>)? Use only "+ ", ".join(target_mapping_gates) + " operator(s). Below is the original circuit:\n"
                            message+= template
                            num_trials+=1
                            format_error = True
                        
                        functional_status = check_LLM_circuit_functionality(template,LLM_circuit,num_test_vectors,target_mapping_gates)
                        if (("error parsing circuit" in functional_status.lower()) and (format_error == False)):
                            my_print(functional_status)
                            message = 'This is not correct because the refactored circuit contains Boolean operators other than the ' + ", ".join(target_mapping_gates) + ' operator(s). Can you try again? Below is the original circuit:\n'
                            message+= template
                            num_trials+=1
                        elif (("error running simulation" in functional_status.lower()) and (format_error == False)):
                            my_print(functional_status)
                            message = "This is not correct because the functionality is not the same as the original circuit. Can you try again? Below is the original circuit:\n"
                            message+= template
                            num_trials+=1
                        elif (("simulation successful" in functional_status.lower()) and (format_error == False)):
                            my_print(functional_status)
                            break

                    if "simulation successful" in functional_status.lower():
                        my_print("Found successful rephrased circuit for the " + gate_type + " gate using " + ", ".join(target_mapping_gates) + " Boolean operator(s). It is as follows:")
                        print(LLM_circuit)
                        my_print("Caching it for future use")
                        if "_".join(target_mapping_gates) in cached_circuit_mapping[gate_type]:
                            cached_circuit_mapping[gate_type]["_".join(target_mapping_gates)].append(LLM_circuit)
                        else:
                            cached_circuit_mapping[gate_type]["_".join(target_mapping_gates)] = [LLM_circuit]
                        with open("./cached_circuit_mapping_GPT3dot5.pkl",'wb') as f:
                            pickle.dump(cached_circuit_mapping,f)
                    else:
                        my_print("NOTE: Tried " + str(max_num_trials) + " times but no success in generating functionally equivalent circuit for the " + gate_type + " gate using " + ", ".join(target_mapping_gates) + " Boolean operator(s). Moving on to the next gate type.")
                except Exception as ex:
                    my_print("Something went wrong: ")
                    my_print(ex)
    '''