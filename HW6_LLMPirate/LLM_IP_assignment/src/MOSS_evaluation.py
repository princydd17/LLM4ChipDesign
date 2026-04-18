import os
import pprint
from plagcheck.plagcheck import check, insights, share_scores

from dotenv import load_dotenv


def evaluate(orig_file,pirated_file):
    load_dotenv()

    language = "verilog"
    userid = "284865820"


    moss = check(language, userid)

    #files to add
    # moss.addFilesByWildCard("../ipFiles/encoder8to3/encoder8to3_*/topModule.v")
    # moss.addFilesByWildCard("../del/*.v")
    moss.addFile(orig_file)
    moss.addFile(pirated_file)



    moss.submit()

    # print(moss.getHomePage())

    result = moss.getResults()

    # pprint.pprint(result)

    result = result[0]

    if result['file1'].split("/")[-2] == 'pirated':
        pirated_file_id = 'file1'
        orig_file_id = 'file2'
    elif result['file2'].split("/")[-2] == 'pirated':
        pirated_file_id = 'file2'
        orig_file_id = 'file1'

    similarity_ratio = float(result["percentage_"+pirated_file_id]/100)

    return similarity_ratio



if __name__ == "__main__":
    similarity_ratio = evaluate("./tmp/files_for_GNN4IP_MOSS/tmp_"+str(0)+"_dataset_for_GNN4IP_MOSS/current_circuit/orig/topModule.v",\
    "./tmp/files_for_GNN4IP_MOSS/tmp_"+str(0)+"_dataset_for_GNN4IP_MOSS/current_circuit/pirated/topModule.v")
    # evaluate("../del/*.v","../del/*.v")
    print("similarity_ratio:",similarity_ratio)
