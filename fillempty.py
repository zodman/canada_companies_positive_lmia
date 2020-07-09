import sys
import tqdm
import rows

filename = sys.argv[1]

results = rows.import_from_csv(filename, encoding='latin1')


new_results = []

old_obj = {}
for r in tqdm.tqdm(results):
    obj = r._asdict()
    for k,v in obj.items():
        if v == '':
            obj[k] = old_obj[k]
    new_results.append(obj)
    old_obj =obj.copy()

table = rows.import_from_dicts(new_results)
rows.export_to_csv(table, f"{filename}.processed.csv")
