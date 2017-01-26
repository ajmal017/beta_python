def get_age_group(age):
    return int(abs(age - 15) / 10)

def get_pc_column_name(income):
    income_group = int(income / 10000)
    if income_group == 6: income_group = 5
    if income_group < 1: income_group = 1
    if income_group > 7: income_group = 7
    return 'pc_{}'.format(income_group)

def get_region_column_name(region_no):
    region = ['northeast', 'south', 'midwest', 'west']
    if region_no >= 1 and region_no <= 4:
        return region[region_no - 1]
    else:
        return None

def get_location_column_name(rucc):
    if rucc in [1, 2, 3]:
        return 'quot_city'
    if rucc in [4, 5, 6, 7]:
        return 'quot_suburb'
    if rucc in [8, 9]:
        return 'quot_rural'
    return None
