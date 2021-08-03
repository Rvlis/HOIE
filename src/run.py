import os
import sys
sys.path.append(".")
sys.path.append("./NER_part/")
sys.path.append("./Relation_predict/")
sys.path.append("./C2S_part/")
import csv
from tqdm import tqdm

from NER_part import corenlp_chunk_candidate_relations_triples, coref
# from Relation_predict import get_entity_and_relation_csv

if __name__ == "__main__":

    # contents = """The 2006 Pangandaran earthquake and tsunami occurred on July 17 at along a subduction zone off the coast of Java, a large and densely populated island in the Indonesian archipelago. The shock had a moment magnitude of 7.7 in Jakarta, which is the capital of Indonesia. There were no direct effects of the earthquake's shaking due to its low intensity, and the large loss of life from the event was due to the resulting tsunami, which inundated a portion of the Java coast that had been unaffected by the earlier 2004 Indian Ocean earthquake and tsunami that was off the coast of Sumatra. The July 2006 earthquake was also centered in the Indian Ocean, from the coast of Java, and had a duration of more than three minutes. An abnormally slow rupture at the Sunda Trench and a tsunami that was unusually strong relative to the size of the earthquake were both factors that led to it being categorized as a tsunami earthquake. Several thousand kilometers to the southeast, surges of several meters were observed in northwestern Australia, but in Java the tsunami heights above normal sea level were typically and resulted in the deaths of more than 600 people. Other factors may have contributed to exceptionally high peak runups of on the small and mostly uninhabited island of Nusa Kambangan, just to the east of the resort town of Pangandaran, where damage was heavy and a large loss of life occurred. Since the shock was felt with only moderate intensity well inland, and even less so at the shore, the surge arrived with little or no warning. Other factors contributed to the tsunami being largely undetected until it was too late and, although a tsunami watch was posted by an American tsunami warning center and a Japanese meteorological center, no information was delivered to people at the coast."""
    
    with open("./Preprocess_part/data/raw_text_sm.txt", encoding="utf-8") as contents:
        input_sentences = list()
        # read contents
        # for content in contents:
        #     # coref resolve
        #     input_sentences.extend(coref.pre_process_text(content))
        #     # print(input_sentences)

        content = """The 2006 Pangandaran earthquake and tsunami occurred on July 17 at along a subduction zone off the coast of Java, a large and densely populated island in the Indonesian archipelago. The shock had a moment magnitude of 7.7 in Jakarta, which is the capital of Indonesia. There were no direct effects of the earthquake's shaking due to its low intensity, and the large loss of life from the event was due to the resulting tsunami, which inundated a portion of the Java coast that had been unaffected by the earlier 2004 Indian Ocean earthquake and tsunami that was off the coast of Sumatra. The July 2006 earthquake was also centered in the Indian Ocean, from the coast of Java, and had a duration of more than three minutes. An abnormally slow rupture at the Sunda Trench and a tsunami that was unusually strong relative to the size of the earthquake were both factors that led to it being categorized as a tsunami earthquake. Several thousand kilometers to the southeast, surges of several meters were observed in northwestern Australia, but in Java the tsunami heights above normal sea level were typically and resulted in the deaths of more than 600 people. Other factors may have contributed to exceptionally high peak runups of on the small and mostly uninhabited island of Nusa Kambangan, just to the east of the resort town of Pangandaran, where damage was heavy and a large loss of life occurred. Since the shock was felt with only moderate intensity well inland, and even less so at the shore, the surge arrived with little or no warning. Other factors contributed to the tsunami being largely undetected until it was too late and, although a tsunami watch was posted by an American tsunami warning center and a Japanese meteorological center, no information was delivered to people at the coast."""
        input_sentences.extend(coref.pre_process_text(content))

        with open("../data/C2S_input.txt", "w", encoding="utf-8") as wf:
            for sentence in input_sentences:
                wf.write(sentence.strip()+"\n")
            wf.write("\n")
        os.system("mvn -q clean compile exec:java")

        simplified_sentences = list()
        with open("../data/C2S_output.txt", encoding="unicode_escape") as rf:
            for line in rf:
                simplified_sentence = line.split("\t")[3]
                # print(simplified_sentence)
                simplified_sentences.append(simplified_sentence)



            candidate_relation_triples = corenlp_chunk_candidate_relations_triples.chunk_candidate_relation_triples(simplified_sentences)
            # print(candidate_relation_triples)
            # atomic proposition with the position of head and tail: [sentence, [start, end], [start, end]]
            atomic_propositions = list()
            with open("../data/atomic_propositions.txt", "w", encoding="utf-8") as wf:    
                for relation_triple in candidate_relation_triples:
                    # print(relation_triple)
                    h_start = 0
                    h_end = len(relation_triple[0])
                    t_start = len(relation_triple[0])+1 + len(relation_triple[1])+1
                    t_end = len(relation_triple[0])+1 + len(relation_triple[1])+1 + len(relation_triple[2])
                    atomic_proposition = [str(relation_triple[0] + " " + relation_triple[1] + " " + relation_triple[2]), [h_start, h_end], [t_start, t_end]]
                    # print(atomic_proposition)
                    wf.write(str(relation_triple[0] + " " + relation_triple[1] + " " + relation_triple[2]) + "\t" + str(h_start) + "\t" + str(h_end) + "\t" + str(t_start) + "\t" + str(t_end) + "\n")


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