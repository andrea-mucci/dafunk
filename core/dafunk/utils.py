def dict_keys_lower(test_dict):
    # create new dictionary with uppercase keys
    new_dict = dict(map(lambda x: (x[0].lower(), x[1]), test_dict.items()))

    # check if values are nested dictionaries and call function recursively
    for key, value in new_dict.items():
        if isinstance(value, dict):
            new_dict[key] = dict_keys_lower(value)

    return new_dict
