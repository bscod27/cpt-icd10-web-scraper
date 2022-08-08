import pandas as pd
import requests
from bs4 import BeautifulSoup
import regex as re


def code_scraper(df: pd.DataFrame, code_type: str, col_name: str) -> pd.DataFrame:
    """
    Takes a pandas data frame with CPT or ICD-10 codes as input and 
    outputs a pandas data frame containing the codes and their respective descriptions/summaries.
    
    @param df: 
    @param code_type: 
    @param col_name: 
    """
    
    code = []
    summary = []
    
    if code_type == 'cpt':
        for i in df[col_name]:
            url = 'https://www.aapc.com/codes/cpt-codes/' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            string = ' '.join(re.findall('\w+', str(soup.find('p'))))
            try:
                summary.append(re.findall('p (.*) p', string)[0])
            except: 
                summary.append('Code does not exist')
            finally: 
                code.append(str(i))
            
    elif code_type == 'icd10':
        for i in df[col_name]:
            a, b, c, d = str(i)[0:4]
            url = 'https://www.icd10data.com/ICD10PCS/Codes/'+ a +'/' + b +'/' + c + '/' + d +'/' + i
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            try:
                summary.append(re.findall(': (.*)<',str(soup.find('title')))[0])
            except: 
                summary.append('Code does not exist')
            finally: 
                code.append(str(i))
    
    else: 
        raise SyntaxError("Invalid code_type provided. Must be either 'cpt' or 'icd10'.")
                
    return pd.DataFrame({'code':code, 'summary': summary})