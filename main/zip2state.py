import pandas as pd
zip_codes = pd.read_csv('main/zipcode_list.csv')

def get_state(zip):

    if type(zip) == int:
        for i in range(len(zip_codes["Zip_Code"])):
            if zip == zip_codes["Zip_Code"][i]:
                return zip_codes["State"][i]
            
        raise Exception('no state found for this zipcode')

    else:
        raise TypeError("zip must be integer")
