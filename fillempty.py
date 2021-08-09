import sys
import rows
import re
import tqdm
import time
import json
import hashlib


filename = sys.argv[1]

results = rows.import_from_csv(filename, encoding='latin1')

DELETE_LINES = 8 * -1
new_results = []

old_obj = {}


def get_phase(f):
    r = [
        "_Positive_Employers_EN.csv",
        "_Positive_Employer_EN.csv",
        "_Positive_EN.csv",
        "_Positive_Employer_Stream_EN.csv",
        "_Positive_Employer_EN.csv",
        "_Positive_Employer_EN.csv",
        "_Positive_Employer_EN.csv",
        "_Positive_EN.csv",
        "_employer_positive_EN.csv",
        "_Positive_EN.csv",
        "TFWP_",
    ]
    for i in r:
        f = f.replace(i, "")
    return "{}".format(f)

def str_dec(x): 
    try:
        return x.encode("latin1").decode("utf-8")
    except UnicodeDecodeError:
        return x


for r in tqdm.tqdm(results[:DELETE_LINES]):
    obj = r._asdict()
    phase = get_phase(filename)
    for k, v in obj.items():
        if v == '':
            obj[k] = old_obj[k]
    postal_code = "N/A"
    city ="N/A"
    if 'address' in obj:
        address = str_dec(obj["address"])
        tmp_postal_code = "".join(address.split(" ")[-2:])
        if len(tmp_postal_code) <=6:
            postal_code = tmp_postal_code
        city = address.split(",")[0]
        # city = city.decode("utf-8")
        # if "montr" in city.lower():
            # assert False, (city.encode("utf-8"),)
    employer="Noname"
    if 'employer' in  obj:
        employer = str_dec(obj["employer"])
    if 'employer_name' in obj:
        employer = str_dec(obj["employer_name"])
        del obj["employer_name"]

    idhash=hashlib.md5(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()
#    tqdm.tqdm.write(postal_code)
    #if "montr" in city.lower():
    #    tqdm.tqdm.write("{}".format(city))
    obj.update({'hashid': idhash, 'phase': phase, 'zipcode': postal_code, 
                'employer': employer,
                'city': city, 'address':address})
    new_results.append(obj)
    old_obj = obj.copy()

table = rows.import_from_dicts(new_results)
rows.export_to_csv(table, f"{filename}.processed.csv")
