def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses


def generate_size(count, total):
    percentage = count / total * 100
    return round(percentage, 2)
