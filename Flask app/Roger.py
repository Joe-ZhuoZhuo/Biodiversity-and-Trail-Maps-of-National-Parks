def rogers_func():
    import pandas as pd
    import json
    
    df = pd.read_csv('data/species.csv', low_memory=False)

    # choose columns to keep, in the desired nested json hierarchical order
    df = df[['Park Name', 'Category', 'Order', 'Family', 'Common Names']]

    # order in the groupby here matters, it determines the json nesting
    # the groupby call makes a pandas series by grouping "Park Name", "Category", "Order" and "Family",
    #while getting the unique values for "common names"
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

        # if 'park_name' is NOT category_list, append it
        if not park_name in category_list:
            d['children'].append({"name":park_name, "children":[{"name":category, "children":[{"name": order}]}]})

        # if 'park_name' IS in category_list, add a new child to it
        else:
            sub_list = []
            for item in d['children'][category_list.index(park_name)]['children']:
                sub_list.append(item['name'])
            # print sub_list

            if not category in sub_list:
                d['children'][category_list.index(park_name)]['children'].append({"name":category, "children":[{"name": order}]})
            else:
                d['children'][category_list.index(park_name)]['children'][sub_list.index(category)]['children'].append({"name": order})
    return d
