def merge_students_data(csv_file, xlsx_workbook, json_file):
    reader = csv.reader(csv_file)
    next(reader, None)
    data = {' '.join(item[:2]): {'age': int(item[2])} for item in reader}
    ws = xlsx_workbook['List1']
    for name, *marks in ws.iter_rows():
        data[name.value]['marks'] = list(filter(lambda x: x is not None, map(lambda x: x.value, marks)))
    json.dump(data, json_file)
