import json
import csv


dict_data = []

with open("./transformer_lookup.json", "r") as file:
    jsonobj = json.load(file)

    for obj in jsonobj:
        listobj = jsonobj[obj]
        listobj[0] = obj

        dict_data.append(listobj)

print(dict_data)

with open("./asdas.csv", 'w', newline='') as csvfile:
    write = csv.writer(csvfile)
    write.writerows(dict_data)
