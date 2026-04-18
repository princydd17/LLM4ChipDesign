import subprocess, os, json, copy
from config import JPLAG_JAR


def evaluate(tmp_Jplag_eval_dir,orig_file_path,pirated_file_path,rank):
    jplag_path = JPLAG_JAR

    os.makedirs(tmp_Jplag_eval_dir,exist_ok=True)

    orig_in = copy.deepcopy(orig_file_path)
    orig_out = tmp_Jplag_eval_dir + "topModule.txt"
    pirated_in = copy.deepcopy(pirated_file_path)
    pirated_out = tmp_Jplag_eval_dir+"topModule_pirated.txt"

    # subprocess.Popen(["cp", orig_in, orig_out], stdout=subprocess.DEVNULL)
    # subprocess.Popen(["cp", pirated_in, pirated_out], stdout=subprocess.DEVNULL)
    # subprocess.call(["cp", orig_in, orig_out], stdout=subprocess.DEVNULL)
    # subprocess.call(["cp", pirated_in, pirated_out], stdout=subprocess.DEVNULL)
    os.system("cp " + orig_in + " " + orig_out)
    os.system("cp " + pirated_in + " " + pirated_out)

    # run similarity comparisons
    command = "java -jar "+ jplag_path + " "+ tmp_Jplag_eval_dir +" -l text -r results_" + str(rank) +".zip"
    run_process = subprocess.run(command, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    try:
        os.system("rm -rf " + tmp_Jplag_eval_dir)
    except Exception as e:
        print("Inner exception")
        print(e)

    return run_process


if __name__ == '__main__':
    rank = 0
    #change to path of jplag-5.0.0-jar-with-dependencies.jar
    jplag_path = JPLAG_JAR

    orig_in = "./del_Jplag_test/topModule.v"
    orig_out = orig_in[:-2]+".txt"
    pirated_in = "./del_Jplag_test/topModule.v"
    pirated_out = pirated_in[:-2]+"_pirated.txt"

    subprocess.Popen(["cp", orig_in, orig_out], stdout=subprocess.DEVNULL)
    subprocess.Popen(["cp", pirated_in, pirated_out], stdout=subprocess.DEVNULL)

    # run similarity comparisons
    command = "java -jar "+ jplag_path + " "+ "./del_Jplag_test/" +" -l text -r results_" + str(rank) +".zip"
    run_process = subprocess.run(command, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # print(run_process)
    if (run_process.stderr):
        if "error" in run_process.stderr.lower():
            print("ERROR!:")
            print(run_process.stderr)
        else:
            # unpack similarity results (currently in zip) into temporary directory
            os.makedirs("./tmp/tmp_jplag_results_" + str(rank),exist_ok=True)
            os.system("unzip -o -d ./tmp/tmp_jplag_results_" + str(rank) + " results_" + str(rank) + ".zip  > /dev/null")

            '''
            # from unpacked results, take the similarity score
            resultJson = open("tmp/tmp_jplag_results_" + str(rank) + "/overview.json")
            data = json.load(resultJson)
            similarity_score = data["top_comparisons"][0]["similarities"]["MAX"]
            print("similarity_score:",similarity_score)
            '''

            resultJson = open("tmp/tmp_jplag_results_" + str(rank) + "/topModule.txt-topModule_pirated.txt.json")
            data = json.load(resultJson)
            if 'pirated' in data['id1']:
                pirated_file_id = 'id1'
                sim_key = 'first_similarity'
            elif 'pirated' in data['id2']:
                pirated_file_id = 'id2'
                sim_key = 'second_similarity'
            else:
                print("ERROR! 'pirated' not found in any filename")

            similarity_score = data[sim_key]
            print("similarity_score:",similarity_score)

            # remove zip, print results
            # os.system("rm -f results_" + str(rank) + ".zip")
            # my_print("env_"+str(rank)+": JPLAG: similarity_score:",similarity_score)
    else:
        # unpack similarity results (currently in zip) into temporary directory
        os.makedirs("./tmp/tmp_jplag_results_" + str(rank),exist_ok=True)
        os.system("unzip -o -d ./tmp/tmp_jplag_results_" + str(rank) + " results_" + str(rank) + ".zip  > /dev/null")

        '''
        # from unpacked results, take the similarity score
        resultJson = open("tmp/tmp_jplag_results_" + str(rank) + "/overview.json")
        data = json.load(resultJson)
        similarity_score = data["top_comparisons"][0]["similarities"]["MAX"]
        print("similarity_score:",similarity_score)
        '''

        resultJson = open("tmp/tmp_jplag_results_" + str(rank) + "/topModule.txt-topModule_pirated.txt.json")
        data = json.load(resultJson)
        if 'pirated' in data['id1']:
            pirated_file_id = 'id1'
            sim_key = 'first_similarity'
        elif 'pirated' in data['id2']:
            pirated_file_id = 'id2'
            sim_key = 'second_similarity'
        else:
            print("ERROR! 'pirated' not found in any filename")

        similarity_score = data[sim_key]
        print("similarity_score:",similarity_score)


        # remove zip, print results
        # os.system("rm -f results_" + str(rank) + ".zip")
        # my_print("env_"+str(rank)+": JPLAG: similarity_score:",similarity_score)
