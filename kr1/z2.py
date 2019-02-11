def xlsx_to_json(xlsx_workbook, json_file):
    ws = xlsx_workbook['List']
    data = {}
    last_key = None
    for args in ws:
        outer_key, inner_key, inner_value = map(lambda x: x.value, args)
        if outer_key:
            data.setdefault(outer_key, {})[inner_key] = inner_value
            last_key = outer_key
        else:
            data[last_key][inner_key] = inner_value
    json.dump(data, json_file)
