import glob, time, pickle, copy, os, subprocess, random, sys
from config import DATASET_PATH, ABC_EXECUTABLE, NANGATE_LIB, NANGATE_LIB_REDUCED
from all_GNN4IP_files.utils.convert_NanGate_to_generic import convert_to_generic  # for GNN4IP
from all_GNN4IP_files.utils.convert_generic_to_NanGate import convert_to_NanGate  # for GNN4IP

def my_print(*args, **kwargs):
    elapsed_time = time.time() - start_time
    log_message = f"[{elapsed_time:.2f}s] {' '.join(map(str, args))}"
    # Print to the console
    print(log_message, **kwargs)


def create_ABC_commands(Nangate_LLM_converted_circuit_path,resyn_circuit_path):
    command_str = f'read_lib {NANGATE_LIB}; '
    command_str+= "read -m " + Nangate_LLM_converted_circuit_path + "; "
    command_str+= 'strash;  rewrite; balance; refactor; '
    #command_str+= 'read_lib -w /home/grads/g/gohil.vasudev/Documents/Research/RL/AI_vs_AI/abc/' + action_to_library[action] + '; '
    command_str+= f'read_lib {NANGATE_LIB_REDUCED}; '
    command_str+= "map; "
    command_str+= 'write ' + resyn_circuit_path

    return command_str

def resyn(circ):
    rank = 0
    with open(circ,'r') as f:
        lines = f.read()
    Nangate_LLM_converted_circuit_path = "./tmp/files_for_GNN4IP/current_circuit_NanGate_LLM_converted_circuit.v"
    convert_to_NanGate(lines,Nangate_LLM_converted_circuit_path)
    # my_print("env_" + str(rank)+": Converted to NanGate")

    resyn_circuit_path = "./tmp/files_for_GNN4IP/current_circuit_resyn.v"
    ABC_command_str = create_ABC_commands(Nangate_LLM_converted_circuit_path,resyn_circuit_path)
    abc_out = subprocess.run([f'{ABC_EXECUTABLE} -q "' + ABC_command_str + '"'],shell=True , capture_output=True, text=True)#, stdout=subprocess.DEVNULL)
    if abc_out.stderr != ''::
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


if __name__ == "__main__":
    start_time = time.time()
    designs = ['c432','c499','c880','IBEX','AES','GPS','MOR1KX']
    variants = []
    for design in designs:
        variants.extend(glob.glob(os.path.join(DATASET_PATH, design.upper(), "*", "*")))
    
    det_tool = 'GNN4IP'
    # det_tool = 'Jplag'
    # det_tool = 'Sim'

    print(f"Against {det_tool}")

    successful_circuits = []
    for variant in variants:
        variant_name = variant.split("/")[-2]
        if variant_name.split("-")[0] in ['c432','c499','c880']:
            tmp_successful_circuits = glob.glob(os.path.join("successful_circuits", "against_"+det_tool, variant_name, "*.v"))
            for circ in tmp_successful_circuits:
                if int(circ.split("/")[-1].split("_")[2])<1720000000:
                    successful_circuits.append(circ)
        else:
            successful_circuits.extend(glob.glob(os.path.join("successful_circuits", "against_"+det_tool, variant_name, "*.v")))
    
