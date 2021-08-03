# import spacy
# from spacy import displacy

# nlp = spacy.load("en_core_web_md")

# doc = nlp("Yao Ming was born in Shanghai, which is in the east of China.")

# displacy.render(doc, style='dep', jupyter=True, options = {'distance': 90})
# # print([(X.text, X.label_, X.start, X.end) for X in doc.ents]) 

test_list = [["hehe",4,7], ["haha", 5, 6]]
sen = "hoho"
begin = 0
end = 6
flag = True
for item in test_list:
    if begin >= item[1] and end <= item[2]:
        flag = False
        # break
    if begin <= item[1] and end >= item[2]:
        while item in test_list:
            test_list.remove(item)


print(test_list)