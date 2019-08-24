import pandas as pd
import json


df = pd.read_csv('data/species.csv', low_memory=False)

# choose columns to keep, in the desired nested json hierarchical order
df = df[['Park Name', 'Category', 'Order', 'Family', 'Common Names']]

# order in the groupby here matters, it determines the json nesting
# the groupby call makes a pandas series by grouping "Park Name", "Category", "Order" and "Family",
#while summing the numerical column 'count'
df1 = df.groupby(['Park Name', 'Category', 'Order', 'Family'])['Common Names'].unique()
df1 = df1.reset_index()

# print(df1)

d = dict()
d = {"children": []}

# Iterating through the dataframe to get column values
for line in df1.values:
    park_name = line[0] # Park Name
    # print(category)
    category = line[1] # Category
    # print(sub_category)
    order = line[2] # Order
    # print(sub_category_type)
    family = line[3]  # Family
    # print(sub_category_sub_type)
    common_name = line[4]  # Common Name
    # print(sub_category_subtype_type)

    # make a list of keys
    category_list = []
    for item in d['children']:
        category_list.append(item['name'])
        # print("category_list")

    # if 'category' is NOT category_list, append it
    if not park_name in category_list:
        d['children'].append({"name":park_name, "children":[{"name":category, "children":[{"name": order}]}]})

    # if 'category' IS in category_list, add a new child to it
    else:
        sub_list = []
        for item in d['children'][category_list.index(park_name)]['children']:
            sub_list.append(item['name'])
        # print sub_list

        if not category in sub_list:
            d['children'][category_list.index(park_name)]['children'].append({"name":category, "children":[{"name": order}]})
        else:
            d['children'][category_list.index(park_name)]['children'][sub_list.index(category)]['children'].append({"name": order})


print(json.dumps(d, indent=4))








# import json
# import pandas as pd
#
# df = pd.read_csv('data/species.csv', low_memory=False)
#
# def get_nested_rec(key, grp):
#     rec = {}
#     rec['Park Name'] = key[0]
#     rec['Category'] = key[1]
#     rec['Order'] = key[2]
#     rec['Family'] = key[3]
#
#     for field in ['Park Name', 'Category', 'Order', 'Family', 'Scientific Name']:
#         rec[field] = list(grp[field].unique())
#
#     return rec
#
# records = []
# for key, grp in df.groupby(['Park Name', 'Category', 'Order', 'Family', 'Scientific Name']):
#     rec = get_nested_rec(key, grp)
#     records.append(rec)
#
# records = dict(data = records)
#
# print(json.dumps(records, indent=4))
#
#
# # for key, grp in df.groupby('Park Name'):
# #     records.append({
# #         "Park Name": key,
# #         "Category": grp.Category.iloc[0],
# #         "Order": {
# #             row.Family: row['Scientific Name'] for row in grp.itertuples()
# #         }})
# #
# # print(json.dumps(records, indent=4))
