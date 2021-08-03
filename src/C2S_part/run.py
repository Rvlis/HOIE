import os
import sys
sys.path.append(".")
sys.path.append("../NER_part/")
sys.path.append("../Relation_predict/")
# sys.path.append("./C2S_part/")
import csv

from NER_part import corenlp_chunk_candidate_relations_triples, coref
from Relation_predict import predict, generate_predict_in

if __name__ == "__main__":

    contents = """The 2006 Pangandaran earthquake and tsunami occurred on July 17 at along a subduction zone off the coast of west and central Java, a large and densely populated island in the Indonesian archipelago. The shock had a moment magnitude of 7.7 in Jakarta, which is the capital of Indonesia. There were no direct effects of the earthquake's shaking due to its low intensity, and the large loss of life from the event was due to the resulting tsunami, which inundated a portion of the Java coast that had been unaffected by the earlier 2004 Indian Ocean earthquake and tsunami that was off the coast of Sumatra. The July 2006 earthquake was also centered in the Indian Ocean, from the coast of Java, and had a duration of more than three minutes. An abnormally slow rupture at the Sunda Trench and a tsunami that was unusually strong relative to the size of the earthquake were both factors that led to it being categorized as a tsunami earthquake. Several thousand kilometers to the southeast, surges of several meters were observed in northwestern Australia, but in Java the tsunami heights above normal sea level were typically and resulted in the deaths of more than 600 people. Other factors may have contributed to exceptionally high peak runups of on the small and mostly uninhabited island of Nusa Kambangan, just to the east of the resort town of Pangandaran, where damage was heavy and a large loss of life occurred. Since the shock was felt with only moderate intensity well inland, and even less so at the shore, the surge arrived with little or no warning. Other factors contributed to the tsunami being largely undetected until it was too late and, although a tsunami watch was posted by an American tsunami warning center and a Japanese meteorological center, no information was delivered to people at the coast."""
    input_sentences = coref.pre_process_text(contents)
    # print(input_sentences)
    with open("./C2S_part/input.txt", "w", encoding="utf-8") as wf:
        for sentence in input_sentences:
            wf.write(sentence.strip()+"\n")
        wf.write("\n")
    # os.system("cd ./C2S_part")
    os.system("mvn -q clean compile exec:java")
    simplified_sentences = list()
    with open("../data/C2S_output.txt", encoding="utf-8") as rf:
        for line in rf:
            simplified_sentence = line.split("\t")[3]
            # print(simplified_sentence)
            simplified_sentences.append(simplified_sentence)



    candidate_relation_triples = corenlp_chunk_candidate_relations_triples.chunk_candidate_relation_triples(simplified_sentences)
    print(candidate_relation_triples)
    # for triple in candidate_relation_triples:
    #     print([triple[0], triple[1], triple[3], triple[4]])
    # csv_path = "../data/csv/relation_triples.csv"
    # try:
    #     os.mkdirs(csv_path)
    # except:
    #     pass

    # with open(csv_path, "w", newline="", encoding="gb18030") as src:
    #     src_csv = csv.writer(src, doublequote=False, escapechar="\\")
    #     for triple in candidate_relation_triples:
    #         # src_csv.writerow([triple[1], triple[2], triple[3], triple[4], triple[5]])
    #         src_csv.writerow([triple[1], triple[3], triple[4]])

    # generate_predict_in.generate_predict_in(csv_path)
    # # predict.predict()