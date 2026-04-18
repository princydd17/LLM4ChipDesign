import subprocess
import glob
import os

def check_compilability(circ_compile,pirated_circ_path,orig_circ_path,testbench_path):
    compiled = False
    proc = subprocess.run(["iverilog", "-o", circ_compile, pirated_circ_path,orig_circ_path,testbench_path],capture_output=True,universal_newlines=True)
    if proc.returncode != 0:
        status = "Error compiling testbench"
        print(status)
        print(proc.stderr)
    elif proc.stderr != "":
        status = "Warnings compiling testbench"
        print(status)
        print(proc.stderr)
    else:
        status = "Compilation successful"
        compiled = True
        print(status)
    return compiled

def check_functionality(compiled_file):
    ran = False
    proc = subprocess.run(["vvp", compiled_file],capture_output=True,universal_newlines=True)
    # op_string = proc.stdout
    if "mismatch" in proc.stdout.lower():
        status = 'Error running simulation'
        print(status)
        print(proc.stdout)
    elif "all tests passed" in proc.stdout.lower():
        status = "Simulation successful"
        print(status)
        ran = True
    return ran

def convert_v_2_c(file1, file2, top):
    run_process = subprocess.run(["./v2c", file1, "--module", top, file2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if (run_process.stderr):
        print("Error:")
        print(run_process.stderr)

def run_c_executable(pattern_1, pattern_2, lang):

    files_1 = glob.glob(pattern_1)
    files_2 = glob.glob(pattern_2)
    executable = "./" + lang

    for file_1 in files_1:
        for file_2 in files_2:
            run_process = subprocess.run([executable, "-peu", file_1, "|", file_2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            if (run_process.stderr):
                print("Error:")
                print(run_process.stderr)
            else:
                print(run_process.stdout)


compile_circ = "encoder8to3_2"
file_verilog_original = "ipFiles/encoder8to3/encoder8to3_2/topModule.v"
file_verilog_pirated = "ipFiles/encoder8to3/encoder8to3_2/topModule-pirated.v"
testbench = "ipFiles/encoder8to3/encoder8to3_2/testbench.v"

compiled = check_compilability(compile_circ, file_verilog_pirated, file_verilog_original, testbench)

ran = check_functionality(compile_circ)

if(compiled == True):
    os.remove(compile_circ)

if(compiled == True and ran == True):
    file_c_original = "compare1/main.c"
    top_module = "top"
    convert_v_2_c(file_verilog_original, file_c_original, top_module)

    file_c_pirated = "compare2/main.c"
    top_module = "top_pirated"
    convert_v_2_c(file_verilog_pirated, file_c_pirated, top_module)

    language = "sim_c"

    run_c_executable(file_c_pirated, file_c_original, language)

    os.remove("compare1/main.c")
    os.remove("compare2/main.c")
else:
    print("Code given was incorrect")