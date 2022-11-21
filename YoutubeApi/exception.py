def is_request_valid(data_dict, key_values):
    if all(key in data_dict for key in key_values):
        return True
    else:
        return False
