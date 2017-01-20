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
    'IntroChunk': ['SHOWN ON RETURN:\n\n', '\n\nADDRESS:\n\n'],
    "SPOUSE SSN": ["SPOUSE SSN:", "NAME(S)"],
    "FILING STATUS": ["\n\nADDRESS:\n\n", "\n\nFORM NUMBER:\n\n"],
    "TOTAL INCOME": ["TOTAL INCOME:", "TOTAL INCOME PER COMPUTER:"]
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
                "TOTAL INCOME": "",

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
                res = parse_item(k, string)
                if k == 'IntroChunk':
                    # 222-22-2222\nFIRST M & SPOUSE M LAST\n\nAC\n\n999 AVENUE RD\nCITY, ST 10.000-90.00-800
                    chunks = res.split('\n')
                    logger.error(chunks)
                    output["sections"][i]["fields"]['SSN'] = chunks[0]
                    if '&' in chunks[1]:
                        csplit = chunks[1].split('&')
                        output["sections"][i]["fields"]['NAME'] = csplit[0] + csplit[1].split(' ')[-1]
                        output["sections"][i]["fields"]['SPOUSE NAME'] = csplit[1].strip(' ')
                    else:
                        output["sections"][i]["fields"]['NAME'] = chunks[1]
                    output["sections"][i]["fields"]['ADDRESS'] = chunks[5] + ', ' + chunks[6]
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
    # '999 AVENUE RD, CITY, ST 10.000-90.00-800'
    address = {
        "address1": '',
        "address2": '',
        "city": '',
        "state": '',
        "post_code": ''
    }
    addr_list1 = addr_str.split(',')
    address['address1'] = addr_list1[0].strip(' ,')
    if '\n' in address['address1']:
        address['address1'] = addr_list1[0].strip(' ,').split('\n')[0]
        address['address2'] = addr_list1[0].strip(' ,').split('\n')[1]
    if len(addr_list1) >= 2:
        address['city'] = addr_list1[1].strip(' ,')
        address['state'] = addr_list1[2].strip(' ,').split(' ')[0]
        address['post_code'] = addr_list1[2].strip(' ,').split(' ')[1]
    return address


def clean_results(results):
    clean_output = {}
    clean_output['SSN'] = results['sections'][0]['fields']['SSN']
    clean_output['SPOUSE SSN'] = results['sections'][0]['fields']['SPOUSE SSN']
    clean_output['NAME'] = results['sections'][0]['fields']['NAME']
    clean_output['SPOUSE NAME'] = results['sections'][0]['fields']['SPOUSE NAME']
    # logger.error(results['sections'][0])
    # logger.error(results['sections'][0]['fields']['ADDRESS'])
    clean_output['ADDRESS'] = parse_address(results['sections'][0]['fields']['ADDRESS'])
    clean_output['FILING STATUS'] = results['sections'][0]['fields']['FILING STATUS']
    clean_output['TOTAL INCOME'] = results['sections'][1]['fields']['TOTAL INCOME']

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
