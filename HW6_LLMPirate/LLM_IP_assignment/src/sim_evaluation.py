import subprocess
import glob
import os, copy
from config import V2C_EXECUTABLE, get_sim_executable
# from convert_generic_netlist_to_assigns import convert_to_assign


def convert_v_2_c(file1, file2, top):
    run_process = subprocess.run([V2C_EXECUTABLE, file1, "--module", top, file2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if (run_process.stderr):
        print("Error:")
        print(run_process.stderr)

def run_c_executable(pattern_1, pattern_2, lang):

    files_1 = glob.glob(pattern_1)
    files_2 = glob.glob(pattern_2)
    # executable = "./" + lang
    executable = get_sim_executable(lang)

    for file_1 in files_1:
        for file_2 in files_2:
            run_process = subprocess.run([executable, "-peu", file_1, "|", file_2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            return run_process
            # if (run_process.stderr):
            #     print("ERROR!:")
            #     print(run_process.stderr)
            # else:
            #     print(run_process.stdout)


def evaluate(orig_file_path,pirated_file_path):
    orig_in = copy.deepcopy(orig_file_path)
    orig_out = orig_in[:-2]+"_assigns.v"
    pirated_in = copy.deepcopy(pirated_file_path)
    pirated_out = pirated_in[:-2]+"_assigns.v"

    convert_to_assign(orig_in,orig_out)
    convert_to_assign(pirated_in,pirated_out)

    file_c_original = orig_out[:-2]+".c" #"./del_sim_test/main_orig.c"
    top_module = "top"
    convert_v_2_c(orig_out, file_c_original, top_module)

    file_c_pirated = pirated_out[:-2]+".c" #"./del_sim_test/main_pirated.c"
    top_module = "top"
    convert_v_2_c(pirated_out, file_c_pirated, top_module)

    #language = "sim_c"
    language = "sim_text"

    run_process = run_c_executable(file_c_pirated, file_c_original, language)
    os.remove(orig_out)
    os.remove(pirated_out)
    os.remove(file_c_original)
    os.remove(file_c_pirated)
    return run_process

    # similarity_score = None
    # if (run_process.stderr):
    #     print("ERROR!:")
    #     print(run_process.stderr)
    # else:
    #     out = run_process.stdout#.decode("utf-8")
    #     if "consists for" in out:
    #         # print(out.split("\n"))
    #         similarity_score = float(out.split("\n")[-2].split("consists for")[-1].split("%")[0].strip())/100
    #     else:
    #         print("ERROR!:")
    #         print(out)
    #     # print(run_process.stdout)
    #
    # os.remove(orig_out)
    # os.remove(pirated_out)
    # os.remove(file_c_original)
    # os.remove(file_c_pirated)
    # return similarity_score

def evaluate_sim_text(orig_file_path,pirated_file_path):
    #language = "sim_c"
    language = "sim_text"

    run_process = run_c_executable(orig_file_path, pirated_file_path, language)
    return run_process



if __name__ == '__main__':
    '''
    # rank = 0
    # run_process = evaluate("./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/orig/topModule.v","./tmp/files_for_GNN4IP/tmp_"+str(rank)+"_dataset_for_GNN4IP/current_circuit/pirated/topModule.v")
    # print(run_process)


    # file_verilog_original = "ipFiles/encoder8to3/encoder8to3_2/topModule.v"
    # file_verilog_pirated = "ipFiles/encoder8to3/encoder8to3_2/topModule-pirated.v"

    # file_verilog_original = "./del_sim_test/topModule.v"
    # file_verilog_pirated = "./del_sim_test/topModule.v"
    orig_in = "./del_sim_test/topModule.v"
    orig_out = "./del_sim_test/topModule_orig_assigns.v"
    pirated_in = "./del_sim_test/topModule.v"
    pirated_out = "./del_sim_test/topModule_pirated_assigns.v"

    convert_to_assign(orig_in,orig_out)
    convert_to_assign(pirated_in,pirated_out)

    file_c_original = "./del_sim_test/main_orig.c"
    top_module = "top"
    convert_v_2_c(orig_out, file_c_original, top_module)

    file_c_pirated = "./del_sim_test/main_pirated.c"
    top_module = "top"
    convert_v_2_c(pirated_out, file_c_pirated, top_module)

    language = "sim_c"

    run_process = run_c_executable(file_c_pirated, file_c_original, language)
    if (run_process.stderr):
        print("ERROR!:")
        print(run_process.stderr)
    else:
        out = run_process.stdout#.decode("utf-8")
        if "consists for" in out:
            # print(out.split("\n"))
            similarity_score = float(out.split("\n")[-2].split("consists for")[-1].split("%")[0].strip())/100
            print("similarity_score:",similarity_score)
        else:
            print("ERROR!:")
            print(out)
        # print(run_process.stdout)

    # os.remove("compare1/main.c")
    # os.remove("compare2/main.c")
    '''

    # orig_in = "./del_sim_test/c432-BE280_topModule.v"
    # orig_in = "./del_sim_test/c499-CS1280_topModule.v"
    orig_in = "./del_sim_test_for_rebuttal/file1.v"
    # pirated_in = "./del_sim_test/c499-CS1280_topModule.v"
    # pirated_in = "./del_sim_test/c432-BE280_topModule.v"
    pirated_in = "./del_sim_test_for_rebuttal/file2.v"


    language = "sim_text"

    run_process = run_c_executable(orig_in, pirated_in, language)
    if (run_process.stderr):
        print("ERROR!!:")
        print(run_process)
        # print(run_process.stderr)
    else:
        out = run_process.stdout#.decode("utf-8")
        if "consists for" in out:
            # print(out.split("\n"))
            similarity_score = float(out.split("\n")[-2].split("consists for")[-1].split("%")[0].strip())/100
            print("similarity_score:",similarity_score)
        else:
            print("ERROR!:")
            print(out)
