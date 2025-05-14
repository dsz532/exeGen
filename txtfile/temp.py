import json

userc=0
f = open("../txtfile/result_complete.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)

f = open("../txtfile/result_complete_4o_mul.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)

f = open("../txtfile/result_complete_4o_sin.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)

f = open("../txtfile/result_complete_4o_ToF.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Llama_mul.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Llama_sin.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Llama_ToF.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_no_discriminator_4o.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_no_generator_4o.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_no_knowledgechain_4o.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_no_kt_4o.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_no_regeneration_4o.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_max_mul.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_max_sin.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_max_ToF.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_plus_mul.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_plus_sin.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_plus_ToF.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_turbo_mul.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_turbo_sin.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
f = open("../txtfile/result_Qwen_turbo_ToF.txt", "r", encoding='utf-8')
j = json.loads(f.read())
userc+=len(j)
print(userc)
# cost = 0
# cost4o = 0
# costturbo = 0
# tim4o = 0
# timturbo = 0
# for i in j:
#     try:
#         cost += i['cost']['usage_excluding_cached_inference']['gpt-4o']['prompt_tokens'] * 0.005 * 0.001 + \
#                 i['cost']['usage_excluding_cached_inference']['gpt-4o']['completion_tokens'] * 0.015 * 0.001
#         cost4o += i['cost']['usage_excluding_cached_inference']['gpt-4o']['prompt_tokens'] * 0.005 * 0.001 + \
#                   i['cost']['usage_excluding_cached_inference']['gpt-4o']['completion_tokens'] * 0.015 * 0.001
#         tim4o += 1
#     except:
#         cost += i['cost']['usage_excluding_cached_inference']['gpt-4-turbo']['prompt_tokens'] * 0.01 * 0.001 + \
#                 i['cost']['usage_excluding_cached_inference']['gpt-4-turbo']['completion_tokens'] * 0.03 * 0.001
#         costturbo += i['cost']['usage_excluding_cached_inference']['gpt-4-turbo']['prompt_tokens'] * 0.01 * 0.001 + \
#                      i['cost']['usage_excluding_cached_inference']['gpt-4-turbo']['completion_tokens'] * 0.03 * 0.001
#         timturbo += 1
# print(f'平均每用户消耗：{cost / 20}')
# print(f'总消耗：{cost}')
# print(f"使用4o用户数：{tim4o}")
# print(f"使用turbo用户数：{timturbo}")
# print(f"4o平均消耗：{cost4o / tim4o}")
# print(f"turbo平均消耗：{costturbo / timturbo}")
