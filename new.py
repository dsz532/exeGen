import json

j = open("output/user1.txt", "r", encoding='utf-8')
j = json.load(j)


def iscorrect(i):
    if i == 1:
        return "正确"
    else:
        return "错误"


outtxt = ""
for user in j:
    outtxt = outtxt + user["round"] + "\n"
    outtxt = outtxt + "\n"
    for task, i in zip(user["tasks"], range(len((user["tasks"])))):
        outtxt = outtxt + str(i + 1) + ". " + task["content"] + "\n"
        outtxt = outtxt + "选项：" + task["option"] + "\n"
        outtxt = outtxt + "正确答案：" + task["right_answer"] + "\n"
        outtxt = outtxt + "学生是否正确作答：" + iscorrect(task["is_correct"]) + "\n"
        outtxt = outtxt + "\n"
    outtxt = outtxt + "\n"
    for result, i in zip(user["result"], range(len((user["result"])))):
        outtxt = outtxt + str(i + 1) + ". " + result["content"] + "\n"
        outtxt = outtxt + "选项：" + result["option"] + "\n"
        outtxt = outtxt + "正确答案：" + result["answer"] + "\n"
        outtxt = outtxt + "\n"
    outtxt = outtxt + "\n"

print(outtxt)
o = open("output/questionnaire.txt", "w", encoding='utf-8')
o.write(outtxt)
o.close()
