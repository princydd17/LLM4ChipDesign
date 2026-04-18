import glob, time, pickle, copy, os, subprocess, random, sys
from MOSS_evaluation import evaluate as moss_evaluate
# from sim_evaluation import evaluate as sim_evaluate
from sim_evaluation import evaluate_sim_text as sim_evaluate_text
from Jplag_evaluation import evaluate as jplag_evaluate
from config import DATASET_PATH, GNN4IP_SCRIPT, GNN4IP_YAML, GNN4IP_MODEL, ABC_EXECUTABLE, NANGATE_LIB, NANGATE_LIB_REDUCED
sys.path.insert(0,"../")
from all_GNN4IP_files.utils.convert_NanGate_to_generic import convert_to_generic  # for GNN4IP
from all_GNN4IP_files.utils.convert_generic_to_NanGate import convert_to_NanGate  # for GNN4IP
import multiprocessing as mp
import json

def is_gate_line(line):
    keywords = ["not", "and", "or", "nand", "nor", "xor", "xnor", "buf"]
    if line.split(" ")[0] in keywords:
        return True
    else:
        return False

def my_print(*args, **kwargs):
    elapsed_time = time.time() - start_time
    log_message = f"[{elapsed_time:.2f}s] {' '.join(map(str, args))}"
    # Print to the console
    print(log_message, **kwargs)

def get_mapped_circuit(orig_file_contents,cached_circuit_mapping,mapping_strategy,rank):
    new_lines = []
    new_wires = []
    lines = orig_file_contents.split(";")
    # Remove whitespace and empty lines
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line.replace("\n"," ") for line in lines]
    for line in lines:
        # line_counter+=1
        if line.startswith(("module ", "input ", "output ", "wire ", "endmodule")):
            new_lines.append(line)
            continue
        if is_gate_line(line):
            keep_line_same = False
            # line = line.replace("(", " ( ")
            # line = line.replace(")", " ) ")
            # gate_type = line.split(" ")[0] + "_" + str(line.count(","))
            # gate_name = line.split()[1].strip()
            # op = line.split()[3].strip(",").strip()
            # num_ips = line.count(",")
            # ips = [line.split()[4+j].strip().strip(",").strip() for j in range(num_ips)]
            gate_type = line.split()[0] + "_" + str(line.count(","))
            if len(list(cached_circuit_mapping[gate_type].keys()))>0:
                line = line.replace("(", " ( ")
                line = line.replace(")", " ) ")
                gate_type = line.split(" ")[0] + "_" + str(line.count(","))
                gate_name = line.split()[1].strip()
                op = line.split()[3].strip(",").strip()
                num_ips = line.count(",")
                ips = [line.split()[4+j].strip().strip(",").strip() for j in range(num_ips)]
                if mapping_strategy == 'random':
                    target_mapping_gate = random.choice(list(cached_circuit_mapping[gate_type].keys()))
                else:
                    if mapping_strategy.split("_")[0] == gate_type.split("_")[0].upper():
                        keep_line_same = True
                    elif mapping_strategy in list(cached_circuit_mapping[gate_type].keys()):
                        target_mapping_gate = copy.deepcopy(mapping_strategy)
                    else:
                        target_mapping_gate = random.choice(list(cached_circuit_mapping[gate_type].keys()))
                # target_mapping_gate = list(cached_circuit_mapping[gate_type].keys())[0]
                # mapped_l = cached_circuit_mapping[gate_type][target_mapping_gate]
                if keep_line_same:
                    new_lines.append(line)
                else:
                    mapped_circuit_str = cached_circuit_mapping[gate_type][target_mapping_gate][0]
                    nets = []
                    mapped_lines = mapped_circuit_str.split("\n")
                    for l in mapped_lines:
                        l = l.strip().strip(";")
                        tmp_inputs = l.split("(")[-1].split(')')[0].split(',')
                        tmp_inputs = [inp.strip() for inp in tmp_inputs]
                        tmp_output = l.split("=")[0].strip()
                        nets.extend(tmp_inputs)
                        nets.append(tmp_output)
                    nets = list(set(nets))
                    inter_net_cnt = 0
                    for net in nets:
                        if net == 'Y':
                            if "Y = " in mapped_circuit_str:
                                mapped_circuit_str = mapped_circuit_str.replace("Y = ",op + " = ")
                            elif "Y=" in mapped_circuit_str:
                                mapped_circuit_str = mapped_circuit_str.replace("Y=",op + "=")
                            elif "Y =" in mapped_circuit_str:
                                mapped_circuit_str = mapped_circuit_str.replace("Y =",op + " =")
                            elif "Y= " in mapped_circuit_str:
                                mapped_circuit_str = mapped_circuit_str.replace("Y= ",op + "= ")
                            else:
                                print("ERROR! The mapping does not follow the correct template:")
                                print(mapped_circuit_str)
                        else:
                            if net in ["A"+str(i) for i in range(1,50)]:
                                # mapped_circuit_str = mapped_circuit_str.replace(net,ips[int(net.split("A")[-1])-1])
                                if "("+net+"," in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace("("+net+",", "("+ips[int(net.split("A")[-1])-1]+",")
                                if " "+net+"," in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace(" "+net+",", " "+ips[int(net.split("A")[-1])-1]+",")
                                if " "+net+")" in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace(" "+net+")", " "+ips[int(net.split("A")[-1])-1]+")")
                                if "("+net+")" in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace("("+net+")", "("+ips[int(net.split("A")[-1])-1]+")")
                                # elif net+")" in mapped_circuit_str:
                                #     mapped_circuit_str = mapped_circuit_str.replace(net+")",ips[int(net.split("A")[-1])-1]+")")
                            else:
                                wire_name = gate_name + "_inter_net_" + str(inter_net_cnt)# net
                                inter_net_cnt+=1
                                # mapped_circuit_str = mapped_circuit_str.replace(net,wire_name)
                                if "("+net+"," in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace("("+net+",", "("+wire_name+",")
                                if " "+net+"," in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace(" "+net+",", " "+wire_name+",")
                                if " "+net+")" in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace(" "+net+")", " "+wire_name+")")
                                if "("+net+")" in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace("("+net+")", "("+wire_name+")")
                                if net + " = " in mapped_circuit_str:
                                    mapped_circuit_str = mapped_circuit_str.replace(net+" = ", wire_name+" = ")
                                new_wires.append(wire_name)
                    # new_str = ''
                    mapped_lines = mapped_circuit_str.split("\n")
                    cnt = 0
                    for l in mapped_lines:
                        l = l.strip().strip(";")
                        tmp_inputs = l.split("(")[-1].split(')')[0].split(',')
                        tmp_inputs = [inp.strip() for inp in tmp_inputs]
                        tmp_output = l.split("=")[0].strip()
                        tmp_gate_type = l.split("=")[-1].split("(")[0].strip()
                        if tmp_gate_type in ['AND', 'OR', 'NAND', 'NOR']:
                            if len(tmp_inputs) == 1:
                                tmp_inp_0 = tmp_inputs[0]
                                tmp_inputs = [tmp_inp_0,tmp_inp_0]
                        new_str = tmp_gate_type.lower() + " " + gate_name+"_"+str(cnt) + " ( " + tmp_output + ", " + ", ".join(tmp_inputs) + " )"
                        cnt+=1
                        new_lines.append(new_str)
                        # new_str += l
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    if len(new_wires)>0:
        for i in range(len(new_lines)):
            line = new_lines[i]
            if line.split()[0] == 'wire':
                new_lines[i] = line + ";\n" + "wire " + ", ".join(new_wires)
                break
                # new_lines[i] = line + ", " + ", ".join(new_wires)

    file_contents = ";\n".join(new_lines)

    return file_contents

def create_ABC_commands(Nangate_LLM_converted_circuit_path,resyn_circuit_path):
    command_str = f'read_lib {NANGATE_LIB}; '
    command_str+= "read -m " + Nangate_LLM_converted_circuit_path + "; "
    command_str+= 'strash;  rewrite; balance; refactor; '
    #command_str+= 'read_lib -w /home/grads/g/gohil.vasudev/Documents/Research/RL/AI_vs_AI/abc/' + action_to_library[action] + '; '
    command_str+= f'read_lib {NANGATE_LIB_REDUCED}; '
    command_str+= "map; "
    command_str+= 'write ' + resyn_circuit_path

    return command_str

def evaluate_vlog_GNN4IP(generic_version_of_current_circuit,GNN4IP_thresh,rank,timestamp):
    out = subprocess.run(f"python3 \
    {GNN4IP_SCRIPT} \
    --yaml_path {GNN4IP_YAML} \
    --raw_dataset_path ./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/ \
    --model_path {GNN4IP_MODEL} \
    --graph_type DFG \
    --LLM_env_id " + str(rank), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # my_print(out)

    if 'error' in out.stderr.lower():
        my_print("env_"+str(rank)+": GNN4IP: ERROR! Evaluation did not go through")#, will try again next time")
        my_print(out)
        similarity_score = None
        # exit()
    else:
        out = out.stdout#.decode("utf-8")
        similarity_score = float(out.strip())
        my_print("env_"+str(rank)+": GNN4IP: similarity_score:",similarity_score)
        # self.f = open("./tmp_mp/files_for_GNN4IP/tmp_"+str(self.rank)+"/training_log.log",'a+')
        # self.f.write("GNN4IP: env_"+str(self.rank)+": similarity_score: " + str(similarity_score)+"\n")
        # self.f.write("GNN4IP: env_"+str(self.rank)+": reward: " + str(reward)+"\n")
        # self.f.close()
        if similarity_score<GNN4IP_thresh:
            #save_circ_name = "./mp_successful_circuits/against_GNN4IP/"+self.generic_version_of_current_circuit.split("/")[-2]+"/env_"+str(self.rank)+"_"+str(time.time()).replace(".","_")+".v"
            os.makedirs("./successful_circuits/against_GNN4IP/"+generic_version_of_current_circuit.split("/")[-2]+"/",exist_ok=True)
            save_circ_name = "./successful_circuits/against_GNN4IP/"+generic_version_of_current_circuit.split("/")[-2]+"/env_"+str(rank)+"_"+str(timestamp).replace(".","_") + "_similarity_score_minus_"+str(-similarity_score)+ ".v"
            # self.f = open("./tmp_mp/files_for_GNN4IP/tmp_"+str(self.rank)+"/training_log.log",'a+')
            # self.f.write("GNN4IP: env_"+str(self.rank)+": Found circuit that fools GNN4IP! " + save_circ_name+ "\n")
            # self.f.close()

            # subprocess.run(["cp", "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"\
            # , save_circ_name], stdout=subprocess.DEVNULL)
            os.system("cp ./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v " + save_circ_name)
            # my_print("env_"+str(rank)+": GNN4IP: Found circuit that fools GNN4IP! " + save_circ_name + "\n")

    # print()
    # print()
    return similarity_score

def evaluate_vlog_MOSS(generic_version_of_current_circuit,MOSS_thresh,rank,timestamp,mapping_file,mapping_strategy,random_sample_num):
    orig_file_path = "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/topModule.v"
    pirated_file_path = "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"

    ### For saving the files to evaluate with MOSS later
    curr_LLM = mapping_file.split("/")[1].split(".")[0].split("_")[3]
    curr_variant = generic_version_of_current_circuit.split("/")[-2]
    os.makedirs("./saved_circuits_for_MOSS/"+curr_LLM+"/"+curr_variant+"/",exist_ok=True)
    tmp_name_pirated = "./saved_circuits_for_MOSS/"+curr_LLM+"/"+curr_variant+"/" + "pirated_mapping_strat_"+mapping_strategy+"_random_sample_num_"+str(random_sample_num)+".v"
    tmp_name_orig = "./saved_circuits_for_MOSS/"+curr_LLM+"/"+curr_variant+"/" + "orig.v"
    os.system("cp " + pirated_file_path + " " + tmp_name_pirated)
    if not os.path.exists(tmp_name_orig):
        os.system("cp " + orig_file_path + " " + tmp_name_orig)
    return None

    try:
        similarity_score = moss_evaluate(orig_file_path,pirated_file_path)
        my_print("env_"+str(rank)+": MOSS: similarity_score:",similarity_score)
        if similarity_score<MOSS_thresh:
            os.makedirs("./successful_circuits/against_MOSS/"+generic_version_of_current_circuit.split("/")[-2]+"/",exist_ok=True)
            save_circ_name = "./successful_circuits/against_MOSS/"+generic_version_of_current_circuit.split("/")[-2]+"/env_"+str(rank)+"_"+str(timestamp).replace(".","_") + "_similarity_score_"+str(similarity_score)+ ".v"
            # subprocess.run(["cp", "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"\
            # , save_circ_name], stdout=subprocess.DEVNULL)
            os.system("cp " + pirated_file_path + " " + save_circ_name)
        #     my_print("env_"+str(rank)+": MOSS: Found circuit that fools MOSS! " + save_circ_name + "\n")
    except:
        my_print("env_"+str(rank)+": MOSS evaluation failed (probably due to query limit)")
        similarity_score = None

    # print()
    # print()
    return similarity_score

def evaluate_vlog_Sim(generic_version_of_current_circuit,Sim_thresh,rank,timestamp):
    orig_file_path = "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/topModule.v"
    pirated_file_path = "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"
    try:
        # run_process = sim_evaluate(orig_file_path,pirated_file_path)
        run_process = sim_evaluate_text(orig_file_path,pirated_file_path)
        # print(run_process)
        if (run_process.stderr):
            my_print("ERROR!:")
            my_print(run_process.stderr)
            similarity_score = None
        else:
            out = run_process.stdout#.decode("utf-8")
            if "consists for" in out:
                # print(out.split("\n"))
                similarity_score = float(out.split("\n")[-2].split("consists for")[-1].split("%")[0].strip())/100
                my_print("env_"+str(rank)+": Sim: similarity_score:",similarity_score)
                if similarity_score<Sim_thresh:
                    os.makedirs("./successful_circuits/against_Sim/"+generic_version_of_current_circuit.split("/")[-2]+"/",exist_ok=True)
                    save_circ_name = "./successful_circuits/against_Sim/"+generic_version_of_current_circuit.split("/")[-2]+"/env_"+str(rank)+"_"+str(timestamp).replace(".","_") + "_similarity_score_"+str(similarity_score)+ ".v"
                    # subprocess.run(["cp", "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"\
                    # , save_circ_name], stdout=subprocess.DEVNULL)
                    os.system("cp " + pirated_file_path + " " + save_circ_name)
                #     my_print("env_"+str(rank)+": MOSS: Found circuit that fools MOSS! " + save_circ_name + "\n")
            else:
                my_print("ERROR!:")
                my_print(out)
                similarity_score = None
    except Exception as e:
        my_print(e)
        my_print("env_"+str(rank)+": Sim evaluation failed")
        similarity_score = None

    # print()
    # print()
    return similarity_score

def evaluate_vlog_Jplag(generic_version_of_current_circuit,Jplag_thresh,rank,timestamp):
    orig_file_path = "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/topModule.v"
    pirated_file_path = "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"
    tmp_Jplag_eval_dir = "/".join(orig_file_path.split("/")[:-2])+"/del_Jplag_eval/"

    try:
        run_process = jplag_evaluate(tmp_Jplag_eval_dir,orig_file_path,pirated_file_path,rank)

        if (run_process.stderr):
            if "error" in run_process.stderr.lower():
                print("ERROR!:")
                print(run_process.stderr)
                similarity_score = None
            else:
                # unpack similarity results (currently in zip) into temporary directory
                os.makedirs(tmp_Jplag_eval_dir,exist_ok=True)
                os.system("unzip -o -d " + tmp_Jplag_eval_dir + " results_" + str(rank) + ".zip  > /dev/null")
                os.system("rm -f results_" + str(rank) + ".zip")

                resultJson = open(tmp_Jplag_eval_dir + "topModule.txt-topModule_pirated.txt.json")
                data = json.load(resultJson)
                if 'pirated' in data['id1']:
                    pirated_file_id = 'id1'
                    sim_key = 'first_similarity'
                elif 'pirated' in data['id2']:
                    pirated_file_id = 'id2'
                    sim_key = 'second_similarity'
                else:
                    my_print("ERROR! 'pirated' not found in any filename")

                similarity_score = data[sim_key]
                my_print("env_"+str(rank)+": Jplag: similarity_score:",similarity_score)
                if similarity_score<Jplag_thresh:
                    os.makedirs("./successful_circuits/against_Jplag/"+generic_version_of_current_circuit.split("/")[-2]+"/",exist_ok=True)
                    save_circ_name = "./successful_circuits/against_Jplag/"+generic_version_of_current_circuit.split("/")[-2]+"/env_"+str(rank)+"_"+str(timestamp).replace(".","_") + "_similarity_score_"+str(similarity_score)+ ".v"
                    # subprocess.run(["cp", "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"\
                    # , save_circ_name], stdout=subprocess.DEVNULL)
                    os.system("cp " + pirated_file_path + " " + save_circ_name)
                #     my_print("env_"+str(rank)+": MOSS: Found circuit that fools MOSS! " + save_circ_name + "\n")
        else:
            # unpack similarity results (currently in zip) into temporary directory
            os.makedirs(tmp_Jplag_eval_dir,exist_ok=True)
            os.system("unzip -o -d " + tmp_Jplag_eval_dir + " results_" + str(rank) + ".zip  > /dev/null")
            os.system("rm -f results_" + str(rank) + ".zip")

            resultJson = open(tmp_Jplag_eval_dir + "topModule.txt-topModule_pirated.txt.json")
            data = json.load(resultJson)
            if 'pirated' in data['id1']:
                pirated_file_id = 'id1'
                sim_key = 'first_similarity'
            elif 'pirated' in data['id2']:
                pirated_file_id = 'id2'
                sim_key = 'second_similarity'
            else:
                my_print("ERROR! 'pirated' not found in any filename")

            similarity_score = data[sim_key]
            my_print("env_"+str(rank)+": Jplag: similarity_score:",similarity_score)
            if similarity_score<Jplag_thresh:
                os.makedirs("./successful_circuits/against_Jplag/"+generic_version_of_current_circuit.split("/")[-2]+"/",exist_ok=True)
                save_circ_name = "./successful_circuits/against_Jplag/"+generic_version_of_current_circuit.split("/")[-2]+"/env_"+str(rank)+"_"+str(timestamp).replace(".","_") + "_similarity_score_"+str(similarity_score)+ ".v"
                # subprocess.run(["cp", "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"\
                # , save_circ_name], stdout=subprocess.DEVNULL)
                os.system("cp " + pirated_file_path + " " + save_circ_name)
            #     my_print("env_"+str(rank)+": MOSS: Found circuit that fools MOSS! " + save_circ_name + "\n")

    except Exception as e:
        my_print(e)
        my_print("env_"+str(rank)+": Jplag evaluation failed")
        similarity_score = None
    try:
        os.system("rm -rf " + tmp_Jplag_eval_dir)
    except Exception as e:
        print("Outer exception")
        print(e)
    return similarity_score

def func(lst):
    [rank, variant, det_tools,mapping_file,mapping_strategy,random_sample_num] = lst
    GNN4IP_successful = None
    GNN4IP_similarity_score = None
    MOSS_successful = None
    MOSS_similarity_score = None
    Sim_successful = None
    Sim_similarity_score = None
    Jplag_successful = None
    Jplag_similarity_score = None
    generic_version_of_current_circuit = copy.deepcopy(variant)+"/topModule.v"

    with open(generic_version_of_current_circuit,'r') as f:
        orig_file_contents = f.read()
    # orig_file_contents = copy.deepcopy(file_contents)

    # os.makedirs("./successful_circuits/against_GNN4IP/"+generic_version_of_current_circuit.split("/")[-2]+"/",exist_ok=True)
    # my_print("env_" + str(rank)+": Current_circuit: " + generic_version_of_current_circuit)

    os.makedirs("./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/",exist_ok=True)

    os.system("rm -rf " + "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/topModule.v")
    os.system("rm -rf " + "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v")

    # subprocess.Popen(["cp", generic_version_of_current_circuit, "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/topModule.v"], stdout=subprocess.DEVNULL)
    os.system("cp " + generic_version_of_current_circuit + " ./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/topModule.v")


    LLM_converted_file_contents = get_mapped_circuit(orig_file_contents,cached_circuit_mapping,mapping_strategy,rank)
    # my_print("env_"+str(rank)+": Rephrasing done")

    #### If NOT using resynthesis
    if not using_resynthesis:
        os.makedirs("./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/",exist_ok=True)
        with open("./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v",'w') as f:
            f.write(LLM_converted_file_contents)

    #### If using resynthesis
    if using_resynthesis:
        # with open("./tmp/files_for_GNN4IP/current_circuit_LLM_converted_circuit.v",'w') as f:
        #     f.writelines(LLM_converted_file_contents)

        # my_print("env_" + str(rank)+": Transformed circuit")

        Nangate_LLM_converted_circuit_path = "./tmp/files_for_GNN4IP/current_circuit_NanGate_LLM_converted_circuit.v"
        convert_to_NanGate(LLM_converted_file_contents,Nangate_LLM_converted_circuit_path)
        # my_print("env_" + str(rank)+": Converted to NanGate")

        resyn_circuit_path = "./tmp/files_for_GNN4IP/current_circuit_resyn.v"
        ABC_command_str = create_ABC_commands(Nangate_LLM_converted_circuit_path,resyn_circuit_path)
        abc_out = subprocess.run([f'{ABC_EXECUTABLE} -q "' + ABC_command_str + '"'],shell=True , capture_output=True, text=True)#, stdout=subprocess.DEVNULL)
        if abc_out.stderr != '':
            print(abc_out)
            my_print("GNN4IP: env_"+str(rank)+": ERROR! ABC did not go through")
            exit()
        # my_print("env_" + str(rank)+": Synthesis done")
        time.sleep(5)
        # my_print("After sleep")


        resyn_circuit_generic_path = "./tmp/files_for_GNN4IP/current_circuit_resyn_generic.v"
        convert_to_generic(resyn_circuit_path,resyn_circuit_generic_path)
        # my_print("env_" + str(rank)+": Converted back to generic")


        os.makedirs("./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/",exist_ok=True)
        subprocess.run(["cp", resyn_circuit_generic_path, "./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v"], stdout=subprocess.DEVNULL)



    timestamp = time.time()

    if "GNN4IP" in det_tools:
        my_print("env_" + str(rank)+": Starting GNN4IP evaluation")
        GNN4IP_similarity_score = evaluate_vlog_GNN4IP(generic_version_of_current_circuit,GNN4IP_thresh,rank,timestamp)
        if GNN4IP_similarity_score == None:
            # pass
            GNN4IP_successful = False
        elif GNN4IP_similarity_score<GNN4IP_thresh:
            # pass
            GNN4IP_successful = True
            # GNN4IP_successful_count+=1
        else:
            GNN4IP_successful = False
        if using_resynthesis:
            os.system("rm -rf " + Nangate_LLM_converted_circuit_path)
            os.system("rm -rf " + resyn_circuit_path)
            os.system("rm -rf " + resyn_circuit_generic_path)
    # return [GNN4IP_successful]

    if "MOSS" in det_tools:
        my_print("env_" + str(rank)+": Starting MOSS evaluation")
        MOSS_similarity_score = evaluate_vlog_MOSS(generic_version_of_current_circuit,MOSS_thresh,rank,timestamp,mapping_file,mapping_strategy,random_sample_num)
        if MOSS_similarity_score == None:
            MOSS_successful = None
        elif MOSS_similarity_score<MOSS_thresh:
            # pass
            MOSS_successful = True
            # MOSS_successful_count+=1
        else:
            MOSS_successful = False

    if "SIM" in det_tools:
        my_print("env_" + str(rank)+": Starting Sim evaluation")
        Sim_similarity_score = evaluate_vlog_Sim(generic_version_of_current_circuit,Sim_thresh,rank,timestamp)
        if Sim_similarity_score == None:
            Sim_successful = None
        elif Sim_similarity_score<Sim_thresh:
            # pass
            Sim_successful = True
            # MOSS_successful_count+=1
        else:
            Sim_successful = False

    if "Jplag" in det_tools:
        my_print("env_" + str(rank)+": Starting Jplag evaluation")
        Jplag_similarity_score = evaluate_vlog_Jplag(generic_version_of_current_circuit,Jplag_thresh,rank,timestamp)
        if Jplag_similarity_score == None:
            Jplag_successful = None
        elif Jplag_similarity_score<Jplag_thresh:
            # pass
            Jplag_successful = True
            # MOSS_successful_count+=1
        else:
            Jplag_successful = False

    return [[GNN4IP_successful,MOSS_successful,Sim_successful,Jplag_successful],
            [GNN4IP_similarity_score,MOSS_similarity_score,Sim_similarity_score,Jplag_similarity_score]]


if __name__ == "__main__":
    start_time = time.time()
    MOSS_thresh = 0.2
    GNN4IP_thresh = 0
    Sim_thresh = 0.3
    Jplag_thresh = 0.3
    num_random_samples = 5
    rank = 0
    using_resynthesis = False
    mapping_strategies = ['random', 'NAND', 'NOR', 'OR_NOT', 'AND_NOT']
    det_tools = ['GNN4IP','MOSS','SIM','Jplag']# ['GNN4IP','Sim','Jplag'] #'MOSS',

    designs = ['c432','c499','c880']

    mapping_files = ["./cached_circuit_mapping_CoPilot_precise.pkl",\
                    # "./cached_circuit_mapping_GPT3dot5_old_prompt.pkl",\
                    "./cached_circuit_mapping_GPT3dot5.pkl",\
                    "./cached_circuit_mapping_GPT4.pkl",\
                    "./cached_circuit_mapping_Claude.pkl",\
                    "./cached_circuit_mapping_Gemini.pkl",\
                    "./cached_circuit_mapping_llama3.pkl",\
                    "./cached_circuit_mapping_codellama7b.pkl",\
                    "./cached_circuit_mapping_codellama13b.pkl",\
                    ]

    # mapping_file = "./cached_circuit_mapping_CoPilot_"+str(conv_style)+".pkl"
    # mapping_file = "./cached_circuit_mapping_GPT3dot5_new_prompt.pkl"
    # mapping_file = "./cached_circuit_mapping_GPT3dot5_old_prompt.pkl"
    # mapping_file = "./cached_circuit_mapping_GPT4.pkl"
    # mapping_file = "./cached_circuit_mapping_Claude.pkl"

    master_results_file_name = "./master_results.pkl"

    if not os.path.exists(master_results_file_name):
        master_results = {}
        # for mapping_file in mapping_files:
        #     master_results[mapping_file.split(".")[0]] = {}
        with open(master_results_file_name,'wb') as f:
            pickle.dump(master_results,f)
    with open(master_results_file_name,'rb') as f:
        master_results = pickle.load(f)

    for mapping_file in mapping_files:
        with open(mapping_file,'rb') as f:
            cached_circuit_mapping = pickle.load(f)
        my_print("Mapping file: " + mapping_file)
        master_results[mapping_file.split("/")[1].split(".")[0]] = {}
        print()

        total_design_count = 0
        functional_count = 0
        GNN4IP_successful_count = 0
        MOSS_successful_count = 0
        Sim_successful_count = 0

        variants = []
        for design in designs:
            variants.extend(glob.glob(os.path.join(DATASET_PATH, design.upper(), "*")))

        for mapping_strategy in mapping_strategies:
            my_print("Mapping strategy:", mapping_strategy)
            master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy] = {}
            print()

            for random_sample_num in range(num_random_samples):
                # print(variants[0])
                my_print("Random sample num:", random_sample_num)
                print()

                no_threads=len(variants)
                args = []
                for rank in range(len(variants)):
                    args.append([rank,variants[rank],det_tools,mapping_file,mapping_strategy,random_sample_num])
                with mp.Pool(processes=no_threads) as pool:
                    results = list(pool.imap(func, args, chunksize=1))
                # my_print(results)
                successes = [result[0] for result in results]
                similarity_scores = [result[1] for result in results]
                my_print("Successes:", successes)
                my_print("Similarity scores:", similarity_scores)

                for idx in range(len(variants)):
                    variant_name = variants[idx].split("/")[-1]
                    if variant_name not in master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy]:
                        master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy][variant_name] = {}
                        for det_tool in det_tools:
                            if det_tool not in master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy][variant_name]:
                                master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy][variant_name][det_tool] = []

                for det_tool in det_tools:
                    if det_tool == 'GNN4IP':
                        GNN4IP_similarity_scores = [v[0] for v in similarity_scores]
                        for idx in range(len(GNN4IP_similarity_scores)):
                            variant_name = variants[idx].split("/")[-1]
                            master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy][variant_name][det_tool].append(GNN4IP_similarity_scores[idx])
                        my_print("Total successful count of " + mapping_strategy + " mapping strategy against " +det_tool+" (thresh="+str(GNN4IP_thresh)+"): " + str(sum([v[0] for v in successes])) + " out of " + str(len(successes)))
                    # elif det_tool == 'MOSS':
                    #     MOSS_similarity_scores = [v[1] for v in similarity_scores]
                    #     for idx in range(len(MOSS_similarity_scores)):
                    #         variant_name = variants[idx].split("/")[-1]
                    #         master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy][variant_name][det_tool].append(MOSS_similarity_scores[idx])
                    #     my_print("Total successful count of " + mapping_strategy + " mapping strategy against " +det_tool+" (thresh="+str(MOSS_thresh)+"): " + str(sum([v[1] for v in successes])) + " out of " + str(len(successes)))
                    elif det_tool == 'SIM':
                        Sim_similarity_scores = [v[2] for v in similarity_scores]
                        for idx in range(len(Sim_similarity_scores)):
                            variant_name = variants[idx].split("/")[-1]
                            master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy][variant_name][det_tool].append(Sim_similarity_scores[idx])
                        my_print("Total successful count of " + mapping_strategy + " mapping strategy against " +det_tool+" (thresh="+str(Sim_thresh)+"): " + str(sum([v[2] for v in successes])) + " out of " + str(len(successes)))
                    elif det_tool == 'Jplag':
                        Jplag_similarity_scores = [v[3] for v in similarity_scores]
                        for idx in range(len(Jplag_similarity_scores)):
                            variant_name = variants[idx].split("/")[-1]
                            master_results[mapping_file.split("/")[1].split(".")[0]][mapping_strategy][variant_name][det_tool].append(Jplag_similarity_scores[idx])
                        my_print("Total successful count of " + mapping_strategy + " mapping strategy against " +det_tool+" (thresh="+str(Jplag_thresh)+"): " + str(sum([v[3] for v in successes])) + " out of " + str(len(successes)))
                # my_print("Total successful count of " + mapping_strategy + " mapping strategy against GNN4IP: " + str(sum([v[0] for v in successes])) + " out of " + str(len(successes)))
                # my_print("Total successful count against MOSS: " + str(sum([v[1] for v in successes])))
                print()
                print()
    with open(master_results_file_name,'wb') as f:
        pickle.dump(master_results,f)
