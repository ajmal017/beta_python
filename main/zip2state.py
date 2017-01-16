import pdb
import pandas as pd

zip_codes = pd.read_csv('zipcode_list.csv')

def get_state(zip):
    for i in range(len(zip_codes["Zip_Code"])):
        if zip == zip_codes["Zip_Code"][i]:
            return zip_codes["State"][i]
        
    
    raise Exception('no state found for this zipcode')

if __name__ == "__main__":
    tst = get_state(1)
    pdb.set_trace()
