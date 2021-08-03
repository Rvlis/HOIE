import jsonlines
import os

s_cnt = 0
with open("./train.jsonl", encoding="utf-8") as rf:
    with open("./raw_text.txt", "w", encoding="utf-8") as wf:
        for item in jsonlines.Reader(rf):
            content = item["content"]
            for sentence in content:
                # print(sentence["sentence"])
                wf.write(sentence["sentence"]+" ")
                s_cnt += 1
            wf.write("\n")

print(s_cnt)