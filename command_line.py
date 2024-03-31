#!/usr/bin/python3

import pandas as pd

import argparse

#function to parse the boolean on confidence and score printout

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Please provide a Boolean value expected. Any of the following (yes, true, t, y,  1) are defaulted as True. While, (no, false, f, n, 0) are defaulted to False')

        
# Parsing the command line input provided by user. The various arguments must be given in specific data type. Also, they present default value when not provided by user 
parser = argparse.ArgumentParser() 

parser.add_argument("-m", "--miRNA", help="This will find the diseases associated with the given miRNA", type=str, required=False, default="")

parser.add_argument("-d", "--disease", help="This will find the miRNAs associated with the given disease. Bear in mind that if the name of disease is made of multiple words, please use quotation mark at the beginning and at the end ", type=str, required=False, default = "")

parser.add_argument("-sb", "--scoreBoolean", help="the programme will print the gene to disease score, if True. Otherwise, the scores will not be printed, if False", default=False, type=str2bool, required=False)

parser.add_argument("-cb", "--confBoolean", help="the programme will print the miRNA to gene confidence, if True. Otherwise, the confidence will not be printed, if False", default=False, type=str2bool, required=False)

parser.add_argument("-s", "--score_disease", help="This will only select rows with a gene to disease association score above the given number ", default= 0.81, type=float, required=False)

parser.add_argument("-c", "--conf_gene", help="This will only select rows with a miRNA to gene association confidence above the given number ", default= 81 , type=float, required=False)

parser.add_argument("-sm", "--miRNA_partial", help="This will find all the miRNAs that contain the provided string in the name ", default="", type=str, required=False)

parser.add_argument("-sd", "--disease_partial", help="This will find all the disease that contain the provided string in the name ", default="", type=str, required=False)

args = parser.parse_args()

gene_conf = 80

miRNA = args.miRNA


disease = args.disease

BooleanScore = args.scoreBoolean 

BooleanConf = args.confBoolean 

#function to check the value of confidence and score 

def score_confidence_checking():
    #Disease score
    if (args.score_disease >=0.81) and args.score_disease <=1:
        disease_score = args.score_disease
    else:
        raise ValueError('disease score must be between 0.81 and 1')
        ## Gene confidence
    if (args.conf_gene >=81) and args.conf_gene <=100:
        gene_conf = args.conf_gene
    else:
        raise ValueError('Gene confidence must be between 81 and 100')
    return disease_score, gene_conf
        

# Call the checking function and assig the values 
disease_score, gene_conf = score_confidence_checking()


miRNA_partial = args.miRNA_partial

disease_partial = args.disease_partial


miRNA_disease = pd.read_csv("microRNA_to_disease_no duplicates.csv")

# find association. Based on input from user,the function will print the correct output. Functionality function at the bottom determines what functionality to use 

def mirna_gene_disease():
    # if mirna argument given finds diseases
    if miRNA != "":
        mirna_diseases = miRNA_disease.loc[(miRNA_disease["miRNA"] == miRNA) & (miRNA_disease["confidence"] >= gene_conf ) & (miRNA_disease["score"] >= disease_score), ["diseaseName", "Gene", "score", "confidence"]]
        ## Return statement when no diseases are found
        if mirna_diseases.shape[0] == 0:
            raise Exception("No miRNA/disease association has been found with the miRNA given. Please check the spelling and try again")
        mirna_diseases.set_index(["diseaseName"], inplace=True)
        
    # if disease argument given finds miRNA
    if disease !="":
        print("yes disease", disease)
        mirna_diseases = miRNA_disease.loc[(miRNA_disease["diseaseName"].str.upper() == disease.upper()) & (miRNA_disease["confidence"] >= gene_conf ) & (miRNA_disease["score"] >= disease_score), ["miRNA", "Gene", "score", "confidence"]]
    
        if mirna_diseases.shape[0] == 0:
            raise Exception("No miRNAs association has been found with the disease given. Please check the spelling and try again")
        mirna_diseases.set_index(["miRNA"], inplace=True)
    
    ## Sort the printout based on if scores and/or confidence are required
    #The printout for when the user does not request the score, nor the confidence
    if (BooleanScore == False) and (BooleanConf == False):
        print("neither the gene confidence, or the disease scores will be printed")
        mirna_diseases = mirna_diseases.drop(columns=['score', 'confidence'])
        mirna_diseases_markdown = mirna_diseases.to_markdown(index=True)
        print(mirna_diseases_markdown)
        return

        
    #The printout for when the user  requests the score, but not the confidence    
    if (BooleanScore == True) and (BooleanConf == False):
        print("The Gene to disease score will be printed ")
        mirna_diseases = mirna_diseases.drop(columns=['confidence'])
        mirna_diseases_markdown = mirna_diseases.to_markdown(index=True)
        print(mirna_diseases_markdown)
        return
        
    
    #The printout for when the user  requests  the confidence, but not the score
    
    if BooleanScore == False and BooleanConf == True:
        print("Only the miRNA to gene assocaiotion confidence will be printed ")
        mirna_diseases = mirna_diseases.drop(columns=['confidence'])
        mirna_diseases_markdown = mirna_diseases.to_markdown(index=True)
        print(mirna_diseases_markdown)
        return
        
        
     # The user wants both confidence and score 
    if BooleanScore == True and BooleanConf == True :
        mirna_diseases_markdown = mirna_diseases.to_markdown(index=True)
        print(mirna_diseases_markdown)       
   
   
#Partial miRNA/disease match. The function will return all miRNA that contains the given part of the name (either miRNa / disease depending on user input )


# find association. Based on input from user,the function will print the correct output. Functionality function at the bottom determines what functionality to use 

def find_miRNA_disease_partials():
    if miRNA_partial != "": # That means the sm argument was given
        matches = miRNA_disease[miRNA_disease["miRNA"].str.contains(miRNA_partial, case=False)]["miRNA"]
    elif disease_partial != "":
        matches = miRNA_disease[miRNA_disease["diseaseName"].str.contains(disease_partial, case=False)]["diseaseName"]
        
    matches = pd.Series(matches.unique(), name="Matches")
    if len(matches) == 0:
        raise Exception("No partial match found. Please check the spelling and try again")    
    partial_markdown = matches.to_markdown(index=False)
    print(partial_markdown)
        

##this function will ensure that only one of the four function is called and only argument is given 
#### Function calling based on input. 4 options, the miRNa, disease, part of miRNA, part of disease name 
# Only one of the four can be possible 
def functionality_calling():
    # Create a boolean array of the arguments to see which one/s is/are given
    booleans = [bool(i) for i in [miRNA, disease, miRNA_partial, disease_partial]]
    #return an array containing the True values in booleans array
    function_to_call = [index for index in range(len(booleans)) if booleans[index] == True] 
    #when more than two arguments are given, the programme cannot run. An exceptio is raise 
    if len(function_to_call) >= 2:
        raise Exception("For functionality purposes, only one argument can be given between miRNA, disease, partialmiRNA, and partial disease. Please check the provided arguments")
    elif function_to_call == []: ## this means no argument has been given 
        raise Exception("Please provide at least one argumnet between miRNA, disease, partialmiRNA, and partial disease. Otherwise, the programme cannot run")
        
          
    if function_to_call[0] == 0:
        mirna_gene_disease()
        return      
 
    elif function_to_call[0] == 1:
        mirna_gene_disease()
        return
    elif function_to_call[0] == 2:
        find_miRNA_disease_partials()
        return
    elif function_to_call[0] == 3:
        find_miRNA_disease_partials()
        
        
        
if __name__ == "__main__":
    functionality_calling()
    #No function definition inside main
else:
    print("run as module\n")

