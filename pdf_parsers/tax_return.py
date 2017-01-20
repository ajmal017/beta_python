#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
required packages to install
linux: apt-get install tesseract
python3: pip-install pyPdf2
"""

import argparse
import os
import shutil
import sys
import json
import subprocess
import logging
import re
import random
import string

logger = logging.getLogger('pdf_parsers.tax_return')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_pdf_content_lines(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        tmp_file_id = id_generator()
        subprocess.run(['pdftotext', pdf_file_path, '/tmp/' + tmp_file_id], stdout=subprocess.PIPE)
        with open('/tmp/' + tmp_file_id, 'rb') as f:
            return f.read()


# for each item to extract its string, the value is found between
# the pairs in the list e.g. SSN is found between "SSN:", "SPOUSE SSN:"
keywords = {
    'IntroChunk': ['SHOWN ON RETURN:\n', '\n\nADDRESS:\n'],
    "FILING STATUS": ["\n\nFILING STATUS:\n", "\nFORM NUMBER:\n"],
    'NAME': ['\nNAME(S) SHOWN ON RETURN:', '\nADDRESS:\n'],
    'SSN': ['\nSSN:', '\nSPOUSE SSN:'],
    'SPOUSE SSN': ['\nSPOUSE SSN:', '\nNAME(S) SHOWN ON RETURN:'],
    'ADDRESS': ['\nADDRESS:\n\n', '\n\nFILING STATUS:'],
    # "TOTAL INCOME": ["TOTAL INCOME PER COMPUTER:\n\n", "\n\nAdjustments to Income"],
    'TotalIncomeColumn': ['TOTAL INCOME PER COMPUTER:\n\nPage 3 of 8\n\n', '\n\nAdjustments to Income'],
    'IncomeColumn': ['EARNED INCOME CREDIT NONTAXABLE COMBAT PAY:\n\n', '\n\nFORM 4136 CREDIT FOR FEDERAL TAX ON FUELS PER'],
}

output = {
    "sections": [
        {
            "name": "Introduction",
            "fields": {
                'IntroChunk': '',
                "SSN": "",
                "SPOUSE SSN": "",
                "NAME": "",
                "SPOUSE NAME": "",
                "ADDRESS": "",
                "FILING STATUS": ""
            }
        },
        {
            "name": "Income",
            "fields": {
                'TotalIncomeColumn': '',
                "TotalIncome": "",
                'IncomeColumn': '',
                'EarnedIncomeCredit': '',
                'CombatCredit': '',
                'ExcessSSCredit': '',
                'AddChildTaxCredit': '',

                'RefundableCredit': '',
                'PremiumTaxCredit': '',
                'TotalPayments': '',
            }
        }
    ]
}


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def parse_item(key, s):
    sub_str = keywords[key]
    start = sub_str[0]
    end = sub_str[1]
    result = find_between(s, start, end)

    return result.lstrip().rstrip().lstrip('.').rstrip('.').rstrip('\n')


def parse_text(string):
    i = 0
    for section in output["sections"]:
        for k, v in list(section["fields"].items()):
            if k in list(keywords.keys()):
                logger.error(k)
                res = parse_item(k, string)
                if k == 'NAME':
                    if '&' in res:
                        csplit = res.split('&')
                        output["sections"][i]["fields"]['NAME'] = csplit[0] + csplit[1].split(' ')[-1]
                        output["sections"][i]["fields"]['SPOUSE NAME'] = csplit[1].strip(' ')
                elif k == "TotalIncomeColumn":
                    chunks = res.split('\n')
                    output["sections"][i]["fields"]['TotalIncome'] = chunks[-2]
                elif k == 'IncomeColumn':
                    chunks = res.split('\n')
                    logger.error(chunks)
                    logger.error(len(chunks))
                    """
                    chunks 0 - health care full year coverage indicator
                           1 - cobra premium subsidy
                           2 - estimated tax payments
                           3 - other payment credit
                           4 - refundable education credit
                           5 - refundable education credit per computer
                           6 - refundable education credit verified
                           7 - earned income credit
                           8 - earned income credit per computer
                           9 - earned income credit nontaxable combat pay
                           10 - schedule 8812 combat pay
                           11 - excess social security
                           12 - tot ss/medicare withheld
                           13 - additional child tax credit
                    """
                    if len(chunks) > 1:
                        output["sections"][i]["fields"]['EarnedIncomeCredit'] = chunks[7]
                        output["sections"][i]["fields"]['CombatCredit'] = chunks[8]
                        output["sections"][i]["fields"]['ExcessSSCredit'] = chunks[11]
                        output["sections"][i]["fields"]['AddChildTaxCredit'] = chunks[13]

                if output["sections"][i]["fields"][k] == "":
                    output["sections"][i]["fields"][k] = res
        i += 1
    return output


def parse_vector_pdf(fl):
    logger.error(get_pdf_content_lines(fl))
    res = get_pdf_content_lines(fl).decode("utf-8")
    return parse_text(res)


def parse_scanned_pdf(fl):
    tmp_pdfs = "tmp"
    if not os.path.exists(tmp_pdfs):
        os.makedirs(tmp_pdfs)

    os.system("convert -density 300 -alpha Off {0} {1}/img.tiff".format(fl, tmp_pdfs))
    os.system("tesseract {0}/img.tiff {0}/out".format(tmp_pdfs))
    cmd = "touch {0}/out.txt && sed -i -e 's/—/-/g' {0}/out.txt".format(tmp_pdfs)
    os.system(cmd)
    with open("{0}/out.txt".format(tmp_pdfs), 'r') as f:
        txt = f.read()

    shutil.rmtree(tmp_pdfs)
    txt = ''.join(txt)
    return parse_text(txt)


def parse_address(addr_str):
    # addr_str format:
    # 200 SAMPLE RD\nHOT SPRINGS, AR 33XXX
    address = {
        "address1": '',
        "address2": '',
        "city": '',
        "state": '',
        "post_code": ''
    }
    logger.error(addr_str)
    addr_list1 = addr_str.split('\n')
    address['address1'] = addr_list1[0].strip(' ,')
    if len(addr_list1) > 2:
        address['address2'] = addr_list1[1].strip(' ,')
    if len(addr_list1) == 2:
        address['city'] = addr_list1[1].split(',')[0]
        address['state'] = addr_list1[1].strip(' ').split(',')[1].split(' ')[1]
        address['post_code'] = addr_list1[1].split(' ')[-1]
    return address


def clean_results(results):
    clean_output = {}
    clean_output['SSN'] = results['sections'][0]['fields']['SSN']
    clean_output['SPOUSE SSN'] = results['sections'][0]['fields']['SPOUSE SSN']
    clean_output['NAME'] = results['sections'][0]['fields']['NAME']
    clean_output['SPOUSE NAME'] = results['sections'][0]['fields']['SPOUSE NAME']
    clean_output['ADDRESS'] = parse_address(results['sections'][0]['fields']['ADDRESS'])
    clean_output['FILING STATUS'] = results['sections'][0]['fields']['FILING STATUS']
    clean_output['TotalIncome'] = results['sections'][1]['fields']['TotalIncome']

    clean_output['EarnedIncomeCredit'] = results['sections'][1]['fields']['EarnedIncomeCredit']
    clean_output['CombatCredit'] = results['sections'][1]['fields']['CombatCredit']
    clean_output['ExcessSSCredit'] = results['sections'][1]['fields']['ExcessSSCredit']
    clean_output['AddChildTaxCredit'] = results['sections'][1]['fields']['AddChildTaxCredit']

    return clean_output


def parse_pdf(filename):
    try:
        # check if pdf is searchable, pdffonts lists fonts used in pdf, if scanned (image), list is empty
        cmd_out = subprocess.getstatusoutput("pdffonts {} | wc -l".format(filename))
        if int(cmd_out[1]) > 2:
            result = parse_vector_pdf(filename)
        else:
            result = parse_scanned_pdf(filename)

        logger.info('Tax Return PDF parsed OK')
        return clean_results(result)
    except Exception as e:
        logger.error(e)
        return


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', type=str, help='Input pdf file', required=True)

        args = parser.parse_args()

        # check if pdf is searchable, pdffonts lists fonts used in pdf, if scanned (image), list is empty
        cmd_out = subprocess.getstatusoutput("pdffonts {} | wc -l".format(args.file))
        if int(cmd_out[1]) > 2:
            result = parse_vector_pdf(args.file)
        else:
            result = parse_scanned_pdf(args.file)

        print(json.dumps(clean_results(result), sort_keys=True, indent=4, separators=(',', ': ')))
        return result
    except KeyboardInterrupt:
        print('Keyboard interrupt!')
        return 0
    except Exception as e:
        print(e)
        raise e


if __name__ == "__main__":
    sys.exit(main())
