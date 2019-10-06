def sqlalch_list_to_json(objects: list):
    collection = {}
    for o in objects:
        obj = o.as_dict()
        collection[obj.get("id")] = obj
    return collection
