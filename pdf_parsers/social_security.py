#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
required packages to install
linux: apt-get install tesseract
python3: pip-install pyPdf2
"""
import argparse
from PyPDF2 import PdfFileReader
import os
import shutil
import sys
import json
import subprocess
import logging

logger = logging.getLogger('pdf_parsers.social_security')


def get_pdf_content_lines(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        pdf_reader = PdfFileReader(f)
        for page in pdf_reader.pages:
            for line in page.extractText().splitlines():
                yield line


# for each item to extract its string, the value is found between
# the pairs in the list e.g. SSN is found between "SSN:", "SPOUSE SSN:"
keywords = {
    'Retirement': ['*Retirement', '*Disability'],
    'Disability': ['*Disability', '*Family'],
    'Family': ['*Family', '*Survivors'],
    'Survivors': ['*Survivors', 'Medicare'],
    'Medicare': ['Medicare', '*'],
    'LastYear': ['You paid:', ''],
    'PaidThisYear': ['', ''],
    'EmployerPaidThisYear': ['', ''],
    'PaidLastYear': ['', ''],
    'EmployerPaidLastYear': ['', ''],
}

output = {
    "sections": [
        {
            "name": "Estimated Benefits",
            "fields": {
                "Retirement": "",
                'Disability': '',
                'Family': '',
                'Survivors': '',
                'Medicare': '',
            }
        },
        {
            'name': 'Estimated Earnings',
            'fields': {
                'LastYear': '',
            }
        },
        {
            'name': 'Estimated Paid',
            'fields': {
                'PaidThisYear': '',
                'EmployerPaidThisYear': '',
                'PaidLastYear': '',
                'EmployerPaidLastYear': '',
            }
        },
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
        for k, v in section["fields"].items():
            res = parse_item(k, string)
            if output["sections"][i]["fields"][k] == "":
                output["sections"][i]["fields"][k] = res
        i += 1
    return output


def parse_vector_pdf(fl):
    res = get_pdf_content_lines(fl)
    return parse_text('\n'.join(res))


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


def clean_results(results):
    clean_output = {}
    clean_output['Retirement'] = results['sections'][0]['fields']['Retirement']
    clean_output['Disability'] = results['sections'][0]['fields']['Disability']
    clean_output['Family'] = results['sections'][0]['fields']['Family']
    clean_output['Survivors'] = results['sections'][0]['fields']['Survivors']
    clean_output['Medicare'] = results['sections'][0]['fields']['Medicare']

    return clean_output


def parse_pdf(filename):
    try:
        # check if pdf is searchable, pdffonts lists fonts used in pdf, if scanned (image), list is empty
        cmd_out = subprocess.getstatusoutput("pdffonts {} | wc -l".format(filename))
        if int(cmd_out[1]) > 2:
            result = parse_vector_pdf(filename)
        else:
            result = parse_scanned_pdf(filename)

        logger.info('Social Security PDF parsed OK')
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
