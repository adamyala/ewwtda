def flatten(nested_list):
    for item in nested_list:
        try:
            yield from flatten(item)
        except TypeError:
            yield item
