#!/usr/bin/env python
'''
usage: mapping.py [-h] -f FROM -t TO -m MAP -o OUTPUT [--i I]
'''
import argparse
import requests
import re
import itertools
import pandas as pd
import wikipedia
wikipedia.set_lang("en")
concepts_external_links={'ICD9_code' : 'http://www.icd9data.com/getICD9Code.ashx?icd9=',
    'ICD10_code' : 'https://icd.who.int/browse10/2019/en#/'}

DATA_DIR = "../data"

def parse_args():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')

    required.add_argument("-f", "--fromterm", help="terms to convert FROM (options: phecodeX, phecodeXupdated, phecode1.2, ICD9, ICD10, hpo)",type=str,required=True) 
    required.add_argument("-m", "--map", help="type of mappings to use (options: string, substring, wikimed)",type=str,required=True)
    required.add_argument("-o", "--outputDir", help="Output directory",type=str, required=True) 

    parser.add_argument("-t", "--toterm", help="Only required if -m is string or substring: terms to convert TO (options: phecodeX, phecodeXupdated, phecode1.2, ICD9, ICD10, hpo)",type=str) 
    parser.add_argument("-i", "--indexrange", help="index ranges for a subset of the file (for parallelization, 0 indexed), example --i 0-100 will retrieve first 100 in file")

    return parser.parse_args()

def main():
    args = parse_args()
    fromTermDF = extractTermsToConvertFROM(args.fromterm, args.indexrange)

    if args.indexrange is None:
        file_suffix = ""
    else:
        file_suffix = f"_{args.indexrange.strip().split('-')[0]}"

    if args.map == 'string':
        out = stringMatch(fromTermDF, args.fromterm, args.toterm)
        out.to_csv(f"{args.outputDir}stringMatch_{args.fromterm}-{args.toterm}{file_suffix}.tsv",sep="\t",index=False)
        
    elif args.map == 'substring':
        out = subStringMatch(fromTermDF, args.fromterm, args.toterm)
        out.to_csv(f"{args.outputDir}subStringMatch_{args.fromterm}-to-{args.toterm}{file_suffix}.tsv",sep="\t",index=False)

    elif args.map == 'wikimed':
        out = wikimedMatch(fromTermDF, args.fromterm)
        if 'ICD9_code' in out.columns:
            icd9 = out[out['ICD9_code'].notnull()].drop('ICD10_code',axis=1).merge(pd.read_csv(f"{DATA_DIR}/ICD9.tsv",sep="\t",dtype=str))
        else:
            icd9 = pd.DataFrame([])

        if 'ICD10_code' in out.columns:
            icd10 = out[out['ICD10_code'].notnull()].drop('ICD9_code',axis=1).merge(pd.read_csv(f"{DATA_DIR}/ICD10.tsv",sep="\t",dtype=str))
        else: 
            icd10 = pd.DataFrame([])

        icd9.to_csv(f"{args.outputDir}wikiMedMap_{args.fromterm}-to-ICD9{file_suffix}.tsv",sep="\t",index=False)
        icd10.to_csv(f"{args.outputDir}wikiMedMap_{args.fromterm}-to-ICD10{file_suffix}.tsv",sep="\t",index=False)


def extractTermsToConvertFROM(fromTerm, indexrange):
    fromTermDF = pd.read_csv(f"{DATA_DIR}/{fromTerm}.tsv",sep="\t",dtype=str)
    if indexrange is not None:
        start_i, end_i = indexrange.strip().split("-")
        fromTermDF = fromTermDF.iloc[int(start_i):int(end_i)]
    return fromTermDF

def extractTermsToConvertTO(toTerm):
    toTermDF = pd.read_csv(f"{DATA_DIR}/{toTerm}.tsv",sep="\t",dtype=str)
    return toTermDF

def stringMatch(fromTermDF, fromTerm, toTerm):
    toTermDF = extractTermsToConvertTO(toTerm)
    out = []
    for _,r in fromTermDF.iterrows():
        match = toTermDF[toTermDF[f'{toTerm}_simpleLabel'] == r[f'{fromTerm}_simpleLabel']]
        for match_i in range(len(match)):
            out.append({**dict(r), **dict(match.iloc[match_i])})

    return pd.DataFrame(out)

def subStringMatch(fromTermDF, fromTerm, toTerm):
    toTermDF = extractTermsToConvertTO(toTerm)
    out = []
    for _,r in fromTermDF.iterrows():
        match = toTermDF.loc[[substrMatchChecker(r[f'{fromTerm}_simpleLabel'], x) for x in toTermDF[f'{toTerm}_simpleLabel']]]
        for match_i in range(len(match)):
            out.append({**dict(r), **dict(match.iloc[match_i])})

    return pd.DataFrame(out)

# Helper function
def substrMatchChecker(substr, string):
    if substr == string: # if perfect match regardless of length
        return True
    if len(substr) <= 5: # if substring is short
        return False
    if len(substr)/len(string) > 2/3:
        if f" {substr} " in f" {string} ":
            return True
        #if len(substr.split(" ")) > 1:
            #if all(f" {w} " in f" {string} " for w in substr.split(" ")): #regardless of the ordering of the words
         #       return True 
    return False

def wikimedMatch(fromTermDF, fromTerm):
    out = []
    for _,r in fromTermDF.iterrows():
        match = searchWikipedia(r[f'{fromTerm}_simpleLabel'])
        if match is not None:
            for m in match:
                out.append({**dict(r), **m})

    return pd.DataFrame(out)

# Helper function
def searchWikipedia(string):
    try: 
        diseasePage=wikipedia.page(string, auto_suggest=False)
        page_external_links=diseasePage.references
        return [{key:x.replace(concepts_external_links[key] ,"")} for x in page_external_links for key in concepts_external_links if concepts_external_links[key] in x]
    except: # Either the page is not available or there are no urls for the JSON decoder. Should probably except specific errors: KeyError, json.decoder.JSONDecodeError #except (wikipedia.exceptions.DisambiguationError,wikipedia.exceptions.PageError) as e:
        print(string)
        return None
        
if __name__ == '__main__':
    main()


