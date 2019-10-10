def sqlalch_list_to_json(objects: list, cols=None):
    collection = {}
    for o in objects:
        obj = o.as_dict(cols)
        collection[obj.get("id")] = obj
    return collection
