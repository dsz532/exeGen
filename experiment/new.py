import json

# j = open("txtfile/result-questionnaire.txt", "r", encoding='utf-8')
# j = json.load(j)
# j = j["list"]
# for i in j:
#     if len(i["answers"]) <= 19: continue
#     if i["role"] == "student": continue
#     answers = i["answers"][19]
#     if answers != None and answers != {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1}:
#         print(answers)

r = open("../txtfile/ques-res.txt", "r", encoding='utf-8')
r = json.load(r)
r = r["stu"]
ave = [0, 0, 0, 0, 0]
for i in range(5):
    for line in r:
        ave[i] += line[f"{i}"]
    ave[i] /= 20
print(ave)

# [4.45, 4.85, 4.65, 4.25, 4.1]
