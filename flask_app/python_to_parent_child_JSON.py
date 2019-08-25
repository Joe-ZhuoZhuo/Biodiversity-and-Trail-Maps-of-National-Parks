# Replace Roger.py this one for the flask app
# Cleaner code that generates the desired data

import csv
import json

class Node(object):
    def __init__(self, name, size=None):
        self.name = name
        self.children = []
        self.size = size

    def child(self, cname, size=None):
        child_found = [c for c in self.children if c.name == cname]
        if not child_found:
            _child = Node(cname, size)
            self.children.append(_child)
        else:
            _child = child_found[0]
        return _child

    def as_dict(self):
        res = {'name': self.name}
        if self.size is None:
            res['children'] = [c.as_dict() for c in self.children]
        else:
            res['size'] = self.size
        return res


root = Node('Flare')

def return_json():

    with open('reduced_species.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            grp1, grp2, grp3, grp4, size = row
            root.child(grp1).child(grp2).child(grp3).child(grp4, size)

    species_string = json.dumps(root.as_dict())
    species_dict = root.as_dict()
    return species_dict



    # with open('read.json', 'w') as outfile:
    #     json.dump(species_string, outfile, sort_keys=True, indent=4)
    #
    # return outfile


# Save a python dict object to JSON format file.
# def python_dict_to_json_file(file_path):
#     try:
#         # Get a file object with write permission.
#         file_object = open(file_path, 'w')
#
#         # Save dict data into the JSON file.
#         json.dump(species_string, file_object)
#
#         print(file_path + " created. ")
#     except FileNotFoundError:
#         print(file_path + " not found. ")
#
# if __name__ == '__main__':
#     python_dict_to_json_file("flare.json")

# file = species_string.replace('\n', '')    # do your cleanup here
#
# with open('read.json', 'w') as outfile:
#     json.dump(file, outfile, sort_keys=True, indent=4)
