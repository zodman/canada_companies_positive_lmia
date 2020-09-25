import sys
import rows
import re
import tqdm
import time


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


for r in tqdm.tqdm(results[:DELETE_LINES]):
    obj = r._asdict()
    phase = get_phase(filename)
    for k, v in obj.items():
        if v == '':
            obj[k] = old_obj[k]
    obj.update({'phase': phase})
    new_results.append(obj)
    old_obj = obj.copy()

table = rows.import_from_dicts(new_results)
rows.export_to_csv(table, f"{filename}.processed.csv")
