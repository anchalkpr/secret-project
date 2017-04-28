import csv

#form 1 of 2
discussion_list_1 = ["give-inputs-hindi-and-tamil-online-handwriting-recognition-system",
                   "give-suggestions-creation-content-digital-marketing-course-using-e-commerce-site",
                   "give-suggestions-new-activities-under-forthcoming-oil-gas-conservation-fortnight-ogcf-%E2%80%93",
                   "give-your-inputssuggestions-draft-iim-bill-2015",
                   "ideas-envisioned-role-dgsd",
                   "inviting-suggestions-manual-procurement-goods"]

#form 2 of 2
discussion_list_2 = ["let-world-see-incredibleindia-through-your-own-eyes",
                   "open-forum-discussion-surajya",
                   "republic-day-walking-down-memory-lane",
                   "share-your-views-public-procurement-bill",
                   "statuecleaning-my-contribution-towards-nation-building",
                   "suggestions-role-voluntary-consumer-organisations-tackling-menace-misleading"]


class Val:
    def __init__(self):
        self.lda = float(0.0)
        self.baseline = float(0.0)
        self.human = float(0.0)
        self.count = 0

    def finalize(self):
        self.lda = self.lda / self.count
        self.baseline = self.baseline / self.count
        self.human = self.human / self.count

    def __str__(self):
        return "Count: " + str(self.count)

def add_val(val1, val2):
    val = Val()
    val.lda = val1.lda + val2.lda
    val.human = val1.human + val2.human
    val.baseline = val1.baseline + val2.baseline
    val.count = val1.count + val2.count

    return val

def get_val(row, start, val_obj):
    lda = int(row[start])
    baseline = int(row[start + 2])
    human = int(row[start + 4])

    val_obj.lda += lda
    val_obj.baseline += baseline
    val_obj.human += human
    val_obj.count += 1

    return val_obj

def get_csv_lines(map, append, discussion_list):
    list = []

    lda = human = baseline = float(0.0)
    count = 0
    for discussion in discussion_list:
        discussion_title = discussion + append
        val = map.get(discussion_title)
        s = discussion_title + "," + str(val.human) + "," + str(val.baseline) + "," + str(val.lda)
        list.append(s)

        lda += val.lda
        human += val.human
        baseline += val.baseline
        count += 1

    val = Val()
    val.lda = lda
    val.human = human
    val.baseline = baseline
    val.count = count
    return list, val


def finalize_val(map):
    for key, val in map.items():
        val.finalize()


discussion_val_map = {}
discussion_coh_val_map = {}

def pop_map(path_to_file, discussion_list):
    with open(path_to_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(readCSV):
            if i == 0:
                continue

            for disc in range(0, 12):
                start = (disc * 3) + 2
                start_coh = ((disc) * 3) + 3
                discussion_title = discussion_list[int(disc/2)]
                if(disc%2 == 0):
                    discussion_title = discussion_title + "_english"
                else:
                    discussion_title = discussion_title + "_hindi"

                val_obj = discussion_val_map.get(discussion_title, Val())
                val_coh_obj = discussion_coh_val_map.get(discussion_title, Val())

                discussion_val_map[discussion_title] = get_val(row, start, val_obj)
                discussion_coh_val_map[discussion_title] = get_val(row, start_coh, val_coh_obj)


path_to_output = "/Users/vault/Desktop/eval_summary.csv"
pop_map("/Users/vault/Desktop/eval1.csv", discussion_list_1)
pop_map("/Users/vault/Desktop/eval2.csv", discussion_list_2)


finalize_val(discussion_val_map)
finalize_val(discussion_coh_val_map)

master_list = []

master_list.append("English Summary,,,")
master_list.append("Discussion Title, Human, Baseline, LDA")
english_lines, eng_val_1 = get_csv_lines(discussion_val_map, "_english", discussion_list_1)
master_list += english_lines
english_lines, eng_val_2 = get_csv_lines(discussion_val_map, "_english", discussion_list_2)
master_list += english_lines
eng_val = add_val(eng_val_1, eng_val_2)
eng_val.finalize()
master_list.append("Average," + str(eng_val.human) + "," + str(eng_val.baseline) + "," + str(eng_val.lda))

master_list.append(",,,")
master_list.append("Hindi Summary,,,")
master_list.append("Discussion Title, Human, Baseline, LDA")
hindi_lines, hin_val_1 = get_csv_lines(discussion_val_map, "_hindi", discussion_list_1)
master_list += hindi_lines
hindi_lines, hin_val_2 = get_csv_lines(discussion_val_map, "_hindi", discussion_list_2)
master_list += hindi_lines
hin_val = add_val(hin_val_1, hin_val_2)
hin_val.finalize()
master_list.append("Average," + str(hin_val.human) + "," + str(hin_val.baseline) + "," + str(hin_val.lda))

master_list.append(",,,")
master_list.append("English Coherence Summary,,,")
master_list.append("Discussion Title, Human, Baseline, LDA")
english_coh_lines, engc_val_1 = get_csv_lines(discussion_coh_val_map, "_english", discussion_list_1)
master_list += english_coh_lines
english_coh_lines, engc_val_2 = get_csv_lines(discussion_coh_val_map, "_english", discussion_list_2)
master_list += english_coh_lines
engc_val = add_val(engc_val_1, engc_val_2)
engc_val.finalize()
master_list.append("Average," + str(engc_val.human) + "," + str(engc_val.baseline) + "," + str(engc_val.lda))

master_list.append(",,,")
master_list.append("Hindi Coherence Summary,,,")
master_list.append("Discussion Title, Human, Baseline, LDA")
hindi_coh_lines, hinc_val_1 = get_csv_lines(discussion_coh_val_map, "_hindi", discussion_list_1)
master_list += hindi_coh_lines
hindi_coh_lines, hinc_val_2 = get_csv_lines(discussion_coh_val_map, "_hindi", discussion_list_2)
master_list += hindi_coh_lines
hinc_val = add_val(hinc_val_1, hinc_val_2)
hinc_val.finalize()
master_list.append("Average," + str(hinc_val.human) + "," + str(hinc_val.baseline) + "," + str(hinc_val.lda))


with open(path_to_output, "w") as output:
    for line in master_list:
        output.write(line)
        output.write("\n")

'''
lda_english = float(0)
lda_hindi = float(0)
baseline_english = float(0)
baseline_hindi = float(0)
human_english = float(0)
human_hindi = float(0)
count = 0


for discussion_title in discussion_list:
    print ("Discussion title: " + discussion_title)
    val_obj = discussion_val_map.get(discussion_title+"_english")
    print ("English results: ")
    lda_e = val_obj.lda/val_obj.count
    lda_english+=lda_e
    baseline_e = val_obj.baseline / val_obj.count
    baseline_english+=baseline_e
    human_e = val_obj.human / val_obj.count
    human_english += human_e

    print ("LDA:\t\t"+ str(lda_e))
    print ("Baseline:\t" + str(baseline_e))
    print ("Human:\t\t" + str(human_e))

    val_obj = discussion_val_map.get(discussion_title + "_hindi")
    print("Hindi results: ")
    lda_h = val_obj.lda / val_obj.count
    lda_hindi += lda_h
    baseline_h = val_obj.baseline / val_obj.count
    baseline_hindi += baseline_h
    human_h = val_obj.human / val_obj.count
    human_hindi += human_h

    print("LDA:\t\t" + str(lda_h))
    print("Baseline:\t" + str(baseline_h))
    print("Human:\t\t" + str(human_h))
    print ("\n")

    count+=1

print ("Average results for English: ")
print ("LDA:\t\t"+str(lda_english/count))
print ("Baseline:\t"+str(baseline_english/count))
print ("Human:\t\t"+str(human_english/count))
print ("\n")
print ("Average results for Hindi: ")
print ("LDA:\t\t"+str(lda_hindi/count))
print ("Baseline:\t"+str(baseline_hindi/count))
print ("Human:\t\t"+str(human_hindi/count))
'''