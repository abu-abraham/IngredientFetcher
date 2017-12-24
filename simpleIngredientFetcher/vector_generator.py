def return_vectors_of_all_dishes():
    temp_set = set()
    with open('dishes.txt') as f:
        content = f.readlines()
    for item in content:
        for vec in item.split():
            temp_set.add(str(vec).lower())
    print len(temp_set)
    return generate_vectors(content,list(temp_set))

def generate_vectors(content, temp_list):
    vector_rep = dict()
    tmp = []
    for item in content:
        item = item.lower()
        for vec in item.split():
            tmp.append(temp_list.index(vec))
        vector_rep[item.strip()] = tmp
        tmp = []
    print temp_list
    return vector_rep,temp_list


