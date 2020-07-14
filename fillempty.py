import sys
import tqdm
import rows

filename = sys.argv[1]

results = rows.import_from_csv(filename, encoding='latin1')

DELETE_LINES = 8 * -1
new_results = []

old_obj = {}
for r in results[:DELETE_LINES]:
    obj = r._asdict()
    phase = filename.lower()
    phase = phase.replace("_positive_en.csv", "")
    phase = phase.replace("_positive_employer_en.csv", "")
    phase = phase.replace("_positive_employer_stream_en.csv", "")
    phase = phase.replace("_employer", "")
    phase = phase.replace("_positives_en", "")
    print(phase)
    for k, v in obj.items():
        if v == '':
            obj[k] = old_obj[k]
    obj.update({'phase': phase})
    new_results.append(obj)
    old_obj = obj.copy()
table = rows.import_from_dicts(new_results)
rows.export_to_csv(table, f"{filename}.processed.csv")
