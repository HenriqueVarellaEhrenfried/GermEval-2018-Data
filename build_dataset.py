import pandas as pd

MODE = 'train'

if MODE == 'train':
    SOURCE = './germeval2018.training.txt'
    TARGET_BASE = './Parsed_Train/'

elif MODE == "test":
    SOURCE = './germeval2018.test.txt'
    TARGET_BASE = './Parsed_Test/'

TARGET_COARSE = TARGET_BASE + "Coarse/"
TARGET_FINE = TARGET_BASE + "Fine/"

LABELS_COARSE = ['OTHER', 'OFFENSE']
LABELS_FINE = ['OTHER', 'ABUSE', 'INSULT', 'PROFANITY']

def get_file_content(file_name):

    df = pd.read_csv(SOURCE, sep='\t', header=None, names=["Text", "Coarse", "Fine"])
    rs = []
    for i in range(0, int(df["Text"].count())):
        rs.append([df["Text"][i],df["Coarse"][i],df["Fine"][i]])
    return rs

def save_file(file_name, content):
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(content)

def get_classes(content):
    classes_coarse = []
    classes_fine = []
    counter_coarse = {}
    counter_fine = {}
    for c in content:
        classes_coarse.append(c[1])
        classes_fine.append(c[2])
        if c[1] not in counter_coarse:
            counter_coarse[c[1]] = 1
        else:
            counter_coarse[c[1]] += 1

        if c[2] not in counter_fine:
            counter_fine[c[2]] = 1
        else:
            counter_fine[c[2]] += 1

    return(list(set(classes_coarse)), counter_coarse, list(set(classes_fine)), counter_fine)


def main():

    all_lines = get_file_content(SOURCE)
    classes_coarse, counter_coarse, classes_fine, counter_fine = get_classes(all_lines)


    for i in range(0,len(all_lines)):
        text_class_coarse = LABELS_COARSE.index(all_lines[i][1])
        text_class_fine = LABELS_FINE.index(all_lines[i][2])
        content = all_lines[i][0]
        name_coarse = TARGET_COARSE + str(text_class_coarse) + "_" + str(i) + ".txt"
        name_fine = TARGET_FINE + str(text_class_fine) + "_" + str(i) + ".txt"
        print(">> Working with file: ", name_coarse)
        print(">> Working with file: ", name_fine)
        save_file(name_coarse, content)
        save_file(name_fine, content)

    print("Available classes Coarse: ", classes_coarse)
    print("Counter of classes Coarse: ", counter_coarse)

    print("Available classes: ", classes_fine)
    print("Counter of classes: ", counter_fine)

if __name__ == "__main__":
    main()

# ----- TRAIN -------
# Available classes Coarse:  ['OTHER', 'OFFENSE']
# Counter of classes Coarse:  {'OTHER': 3321, 'OFFENSE': 1688}
# Available classes:  ['OTHER', 'ABUSE', 'INSULT', 'PROFANITY']
# Counter of classes:  {'OTHER': 3321, 'INSULT': 595, 'PROFANITY': 71, 'ABUSE': 1022}

# # ----- TEST -------
# Available classes Coarse:  ['OFFENSE', 'OTHER']
# Counter of classes Coarse:  {'OTHER': 2248, 'OFFENSE': 1150}
# Available classes:  ['PROFANITY', 'INSULT', 'ABUSE', 'OTHER']
# Counter of classes:  {'OTHER': 2248, 'ABUSE': 737, 'INSULT': 368, 'PROFANITY': 45}
