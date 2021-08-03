"""
implementation of paper "HDSKG" : (Ⅲ.) APPROACH  part D. "Chunk Candidate Relations Triples"
"""
import sys
sys.path.append(".")

from stanza.server import CoreNLPClient
import os
from tqdm import tqdm
import scenarios        # implementation of 6 scenarios
# import pre_process_text # implementation of preprocess text
# from scripts import myutils
import coref
import spacy
nlp = spacy.load("en_core_web_md")
import csv

# Table Ⅰ. REGULAR EXPRESSION OF DIFFERENT CHUNKS
VVP_pattern = [
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(TO*)+(VB)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:TO]{1,})([pos:VB]{1,})",
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:IN]{1,})([pos:VBG]{1,})",
    # new: was a large and densely populated island in
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:JJ]*)([pos:CC]?)([pos:RB]*)([pos:/VB.*/]*)([pos:/NN.*/]*)([pos:/IN|TO/]{1,})"
]

VP_pattern = [
    # (MD)*(VB.*)+(CD)*(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:CD]*)([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:/IN|TO/]{1,})",
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
    # "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:/IN|TO/]{1,})",
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]{1,})",
    # (MD)*(VB.*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})",

    # new: is in the east of
    "([pos:/VB.*/]{1,})([pos:/IN|TO/]{1,})([pos:DT]?)([pos:/NN.*/]*)([pos:/IN|TO/]{1,})",
    "([pos:/VB.*/]{1,})([pos:DT]?)([pos:/NN.*/]*)([pos:/IN|TO/]{1,})"
]

NP_pattern = [
    # (CD)*(DT)?(CD)*(JJ)*(CD)*(VBD|VBG)*(NN.*)*-
    # (POS)*(CD)*(VBD|VBG)*(NN.*)*-
    # (VBD|VBG)*(NN.*)*(POS)*(CD)*(NN.*)+
    "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})",
    "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})([pos:CC]?)([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})"
]



def chunk_candidate_relation_triples(input_sentences):
    """
    :param input_sentences: list[input_sentence1, input_sentence2, ...]

    """
    candidate_relation_triples = list()
    # set up the client
    with CoreNLPClient(annotators=['tokenize','ssplit','pos','depparse'], timeout=60000, memory='4G', be_quiet=True) as client:
        print("----------Chunk Candidate relations triples----------")
        for input_sentence in tqdm(input_sentences):
            # print(input_sentence)
            # os.system("pause")
            ann = client.annotate(input_sentence)
            sentence = ann.sentence[0]

            # HDSKG's method
            # denpendency_rel: source, target, dep
            dependency_rel = list()
            enhanced_plus_plus_dependency_parse = sentence.enhancedPlusPlusDependencies
            edges = list(enhanced_plus_plus_dependency_parse.edge)
            for edge in edges:
                # print(type(edge.source),type(edge.target),type(edge.dep))
                dependency_rel.append([edge.source-1, edge.target-1, edge.dep])
            # print(list(enhanced_plus_plus_dependency_parse.edge))
            # for item in dependency_rel:
            #     print(item)
            # os.system("pause")
            VPs = list()
            NPs = list()
            

            # VVP_pattern
            for pattern in VVP_pattern:
                matches = client.tokensregex(input_sentence, pattern)
                # length means the number of matched phrase
                length = matches["sentences"][0]["length"]
                if length != 0:
                    for i in range(length):
                        text = matches["sentences"][0][str(i)]["text"]
                        begin = matches["sentences"][0][str(i)]["begin"]
                        end = matches["sentences"][0][str(i)]["end"]
                        # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                        flag = True
                        for item in VPs:
                            if begin >= item[1] and end <= item[2]:
                                flag = False
                                break
                            if begin <= item[1] and end >= item[2]:
                                VPs.remove(item)
                        if flag:
                            VPs.append([text,begin,end])
                        # VPs.append([text,begin,end])

            # VP_pattern
            for pattern in VP_pattern: 
                matches = client.tokensregex(input_sentence, pattern)
                # print(matches)
                # length means the number of matched phrase
                length = matches["sentences"][0]["length"]
                if length != 0:
                    for i in range(length):
                        text = matches["sentences"][0][str(i)]["text"]
                        begin = matches["sentences"][0][str(i)]["begin"]
                        end = matches["sentences"][0][str(i)]["end"]
                        # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                        # VP存在重复匹配问题，需要多加一步判断
                        flag = True
                        for item in VPs:
                            if begin >= item[1] and end <= item[2]:
                                flag = False
                                break
                            if begin <= item[1] and end >= item[2]:
                                VPs.remove(item)
                        if flag:
                            VPs.append([text,begin,end])

            # NP_pattern
            # Spacy NER
            NP_set = set()
            doc = nlp(input_sentence)
            for ent in doc.ents:
                if ent.text not in NP_set:
                    NP_set.add(ent.text)
                    NPs.append([ent.text, ent.start, ent.end])
            # rule-based NER
            for pattern in NP_pattern:
                matches = client.tokensregex(input_sentence, pattern)
                # print(matches)
                # length means the number of matched phrase
                length = matches["sentences"][0]["length"]
                if length != 0:
                    for i in range(length):
                        text = matches["sentences"][0][str(i)]["text"]
                        begin = matches["sentences"][0][str(i)]["begin"]
                        end = matches["sentences"][0][str(i)]["end"]
                        # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                        # NPs遵循贪婪匹配
                        flag = True
                        for item in sorted(NPs):
                            if begin >= item[1] and end <= item[2]:
                                flag = False
                                break
                            if begin <= item[1] and end >= item[2]:
                                NPs.remove(item)
                        # print(text, begin, end, flag)
                        if flag:
                            # print([text,begin,end])
                            if text not in NP_set:
                                NP_set.add(text)
                                NPs.append([text,begin,end])
            # print(sentence)
            # print(NPs)
            # os.system("pause")
            # print(NPs)
            # for item in VPs:
            #     print(item[0],item[1],item[2])
            # for item in NPs:
            #     print(item[0],item[1],item[2])

            candidate_relation_triples.extend(scenarios.Scenario(dependency_rel, VPs, NPs))
            
    # for item in candidate_relation_triples:
    #     print(item)

    # myutils.remove_file("./csvs/candidate_relation_triples.csv")
    # crt_csv = myutils.open_csv("candidate_relation_triples", "w")
    # for item in candidate_relation_triples:
    #     print(item)
    #     crt_csv.writerow(
    #         [item[1], item[2], item[3]]
    #     )

    print("candidate_relation_triples:")
    for triple in candidate_relation_triples:
        print(triple)
    return candidate_relation_triples
    
            

contents = """
The 2006 Pangandaran earthquake and tsunami occurred on July 17 at along a subduction zone off the coast of west and central Java, a large and densely populated island in the Indonesian archipelago. The shock had a moment magnitude of 7.7 and a maximum perceived intensity of IV ("Light") in Jakarta, the capital and largest city of Indonesia. There were no direct effects of the earthquake's shaking due to its low intensity, and the large loss of life from the event was due to the resulting tsunami, which inundated a portion of the Java coast that had been unaffected by the earlier 2004 Indian Ocean earthquake and tsunami that was off the coast of Sumatra. The July 2006 earthquake was also centered in the Indian Ocean, from the coast of Java, and had a duration of more than three minutes. An abnormally slow rupture at the Sunda Trench and a tsunami that was unusually strong relative to the size of the earthquake were both factors that led to it being categorized as a tsunami earthquake. Several thousand kilometers to the southeast, surges of several meters were observed in northwestern Australia, but in Java the tsunami runups (height above normal sea level) were typically and resulted in the deaths of more than 600 people. Other factors may have contributed to exceptionally high peak runups of on the small and mostly uninhabited island of Nusa Kambangan, just to the east of the resort town of Pangandaran, where damage was heavy and a large loss of life occurred. Since the shock was felt with only moderate intensity well inland, and even less so at the shore, the surge arrived with little or no warning. Other factors contributed to the tsunami being largely undetected until it was too late and, although a tsunami watch was posted by an American tsunami warning center and a Japanese meteorological center, no information was delivered to people at the coast. 
"""

if __name__ == "__main__":

    input_sentences = coref.pre_process_text(contents)
    with open("../C2S_part/input.txt", "w", encoding="utf-8") as wf:
        for sentence in input_sentences:
            wf.write(sentence.strip()+"\n")
        wf.write("\n")

    
    # candidate_relation_triples = chunk_candidate_relation_triples(input_sentences)
    # print(candidate_relation_triples)
    # csv_path = "../../data/csv/relation_triples.csv"
    # try:
    #     os.mkdirs(csv_path)
    # except:
    #     pass

    # with open(csv_path, "w", newline="", encoding="gb18030") as src:
    #     src_csv = csv.writer(src, doublequote=False, escapechar="\\")
    #     for triple in candidate_relation_triples:
    #         src_csv.writerow([triple[1], triple[2], triple[3], triple[4], triple[5]])