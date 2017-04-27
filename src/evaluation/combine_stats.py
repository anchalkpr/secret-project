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

path_to_eval_csv = "/Users/vault/Desktop/eval1.csv"
path_to_output = "/Users/vault/Desktop/eval1_summary.csv"
discussion_list = discussion_list_1
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

def get_val(row, start, val_obj):
    lda = int(row[start])
    baseline = int(row[start + 2])
    human = int(row[start + 4])

    val_obj.lda += lda
    val_obj.baseline += baseline
    val_obj.human += human
    val_obj.count += 1

    return val_obj

def get_csv_lines(map, append):
    list = []
    list.append("Discussion Title, Human, Baseline, LDA")

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
    list.append(",,,")
    list.append("Average," + str(human/count) + "," + str(baseline/count) + "," + str(lda/count))
    return list


def finalize_val(map):
    for key, val in map.items():
        val.finalize()


discussion_val_map = {}
discussion_coh_val_map = {}
with open(path_to_eval_csv) as csvfile:
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

finalize_val(discussion_val_map)
finalize_val(discussion_coh_val_map)

master_list = []

master_list.append("English Summary,,,")
english_lines = get_csv_lines(discussion_val_map, "_english")
master_list += english_lines

master_list.append(",,,")
master_list.append("Hindi Summary,,,")
hindi_lines = get_csv_lines(discussion_val_map, "_hindi")
master_list += hindi_lines

master_list.append(",,,")
master_list.append("English Coherence Summary,,,")
english_coh_lines = get_csv_lines(discussion_coh_val_map, "_english")
master_list += english_coh_lines

master_list.append(",,,")
master_list.append("Hindi Coherence Summary,,,")
hindi_coh_lines = get_csv_lines(discussion_coh_val_map, "_hindi")
master_list += hindi_coh_lines

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