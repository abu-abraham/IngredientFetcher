import re
import operator

def train_doc():
    with open('train.txt') as f:
        contents = f.readlines();
    d = {}
    for line in contents:
        line = re.sub("[-?.,(!/;_:*=)\"\'@]", '', line)
        for word in line.split():
            word = re.sub(r'\d+', '', word)
            if len(word) < 3:
                continue
            word = word.lower()
            if word in d:
                d[word] = d[word]+1
            else:
                d[word] = 0
    sorted_dictionary = sorted(d.items(), key=operator.itemgetter(1),reverse=True)
    f = open("final_word_list.txt","a") 
    for item in sorted_dictionary:
        f.write(item[0])
        f.write("\n")
    f.close()
    


def get_full_list_of_words():
    with open('final_word_list.txt') as f:
        contents = f.readlines()
    r_list = set()
    for line in contents:
        r_list.add(line.strip())
    return r_list

def read_line_by_line():
    contents = []
    count = 0
    with open('train.txt') as f:
        for line in iter(lambda: f.readline().rstrip(), '.'):
            contents.append(line)
            if len(line)<=0:
                count+=1;
                if count>=10:
                    return contents
            else:
                count = 0
        else:
            return contents

def generate_predictions_previous_word():
    d = {}
    contents = read_line_by_line()
    for line in contents:
        line = re.sub("[-?.,(!/;_:*=)\"\'@]", '', line)
        line = line.split()
        for index,word in enumerate(line):
            word = re.sub(r'\d+', '', word)
            word = word.lower()
            if len(word)<3:
                break
            if index == 0:
                d.setdefault(word,[]).append(' ')
            else:
                d.setdefault(word,[]).append(line[index-1])
    return d;  
