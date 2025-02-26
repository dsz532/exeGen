import json
import re

def extract_last_json(s):
    pattern = r'```json(.*?)```'
    matches = re.findall(pattern, s, re.DOTALL)
    if matches:
        json_str = matches[-1]
        try:
            json_obj = json.loads(json_str, strict=False)
            return json_obj
        except json.JSONDecodeError as e:
            print(f"解析错误：{e}")
    return None

with open("C:/code/exeGen/txtfile/test.txt", "r") as f:
    s = f.read()
    print(extract_last_json(s))
