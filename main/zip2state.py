import pandas as pd
import os
dir = os.path.dirname(__file__)
file_name = os.path.join(dir, 'zipcode_list.csv')
zip_codes = pd.read_csv(file_name)
  
def get_state(zip):

    # check input is valid
    validate_input(zip)

    # look for the state
    for i in range(len(zip_codes["Zip_Code"])):
        if zip == zip_codes["Zip_Code"][i]:
            return zip_codes["State"][i]

    return 'FL'
    #raise Exception('no state found for this zipcode')
    # a fudge so that can demo without tripping up


def validate_input(zip):
    if not zip:
        raise Exception("zip not provided")

    else:
        if type(zip) != int:
            raise Exception("zip must be integer")
    
