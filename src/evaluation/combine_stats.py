import csv

#form 1 of 2
discussion_list = ["give-inputs-hindi-and-tamil-online-handwriting-recognition-system",
                   "give-suggestions-creation-content-digital-marketing-course-using-e-commerce-site",
                   "give-suggestions-new-activities-under-forthcoming-oil-gas-conservation-fortnight-ogcf-%E2%80%93",
                   "give-your-inputssuggestions-draft-iim-bill-2015",
                   "ideas-envisioned-role-dgsd",
                   "inviting-suggestions-manual-procurement-goods"]

#form 2 of 2

discussion_list = ["let-world-see-incredibleindia-through-your-own-eyes",
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

    def __str__(self):
        return "Count: " + str(self.count)

discussion_val_map = {}

path_to_eval_csv = "/Users/vault/Desktop/eval2.csv"
with open(path_to_eval_csv) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(readCSV):
        if i == 0:
            continue

        for section in range(0, 12):
            start = (section * 3) + 2
            discussion_title = discussion_list[int(section/2)]
            if(section%2 == 0):
                discussion_title = discussion_title + "_english"
            else:
                discussion_title = discussion_title + "_hindi"

            lda = int(row[start])
            baseline = int(row[start+1])
            human = int(row[start+2])

            val_obj = discussion_val_map.get(discussion_title, Val())
            val_obj.lda += lda
            val_obj.baseline += baseline
            val_obj.human += human
            val_obj.count += 1

            discussion_val_map[discussion_title] = val_obj

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