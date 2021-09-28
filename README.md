# MIE-information extraction
## 一、流程
![流程图](./img/图谱流程.png)
## 二、Pipeline：BERTOverflow & R-BERT
### 1. BERTOverflow
- 以StackOverflow数据作为语料预训练的BERT模型
- [2020-ACL-Code and Named Entity Recognition in StackOverflow](https://arxiv.org/abs/2005.01634)
- [Github](https://github.com/jeniyat/StackOverflowNER)
- "We trained in-domain BERT representations (BERTOverflow) on __152 million sentences__ from StackOverflow, which lead to an absolute increase of __+10 F-1 score__ over off-the-shelf BERT."
- "We also present the SoftNER model which achieves an overall __79.10 F1 score__ for code and named entity recognition on StackOverflow data."

| 实体类型 | precision | recall | F1-score |
| :--- | :---: | :---: | :---: |
| Algorithm | 57.89% | 68.75% | 62.86 |
| Application | 80.59% | 80.59% | 80.59 |
| Class | 72.66% | 72.94% | 72.80 |
| Data_Structure | 89.76% | 74.49% | 81.42 |
| Data_Type | 85.34% | 89.19%| 87.22|
| File_Name | 89.12% | 80.37%| 84.52|
| File_Type | 91.92% | 70.54% | 79.82|
| Function | 66.78% | 75.56% | 70.90|
| HTML_XML_Tag | 62.79% |51.92% |  56.84|
| Language | 77.94% | 89.33% | 83.25|
| Library | 67.77% | 79.38% | 73.12|
| Operating_System | 88.57% | 93.94% | 91.18|
| User_Interface_Element | 74.88% | 84.79% | 79.52|
| Variable | 67.77% | 79.38% | 73.12|
| Website | 82.76% | 61.54% | 70.59|

### 2. R-BERT
- 使用BERT实现的文本分类模型
- [2019-CIKM-Enriching Pre-trained Language Model with Entity Information for Relation Classification](https://dl.acm.org/doi/abs/10.1145/3357384.3358119)
- [Github](https://github.com/monologg/R-BERT)

![R-BERT](img/R-BERT%20comprasion.jpg)

## 三、比较工具
1. HDSKG
   - HDSKG中实体识别使用的是`基于词性的模式匹配`，实际中通过这些些启发式规则提取了很多噪音数据，如a powerful tool、a framework等, 而且这些噪音数据没有找到合适的办法剔除。 BERTOverflow以20种实体类型预先标注了训练语料，提取效果更好，基本不会提取出类似前面的噪音，但类别有限，也可能导致提取不到想要的实体。
   - 将预训练的BERTOverflwo模型用于实体识别，相当于识别出的实体已经有一定的领域相关性，代替了HDSKG的`Domain Relevance Estimation`部分。按道理，预训练的BERTOverflow无论是从先进性还是使用效果上，都是优于原HDSKG中的方法的。
2. Stanford openIE
   - HDSKG > openIE 
3. Spacy
4. [ThuNLP-OpenNRE](https://github.com/thunlp/OpenNRE)

## 三、Dataset & Benchmark
1. CaRB：CaRB is a dataset cum evaluation framework for benchmarking Open Information Extraction systems
2. CaRB45：CaRB45 is a dataset seleceted from CaRB, which has a size of 45 sentences. Each sentence has following features:
   - It is a compound sentence.
   - It includes at least two fact triples.
   -   

## 四、Evaluation

1. Performance of various Open IE systems on CaRB
   
   | System | precision | recall | F1-score |
   | :--- | :---: | :---: | :---: |
   | Ollie | 0.505 | 0.346 | 0.411 |
   | Props | 0.340 | 0.300 | 0.319 |
   | OpenIE4 | 0.553 | __0.437__ | __0.488__ |
   | OpenIE5 | 0.521 | 0.424 | 0.467 |
   | ClauseIE | 0.521 | 0.424| 0.450|
   | MIE | __0.574__ | 0.419| 0.484|

2. Comparison of various component-ablated versions of MIE on __CaRB__
   <!-- ![ablation on CaRB](./img/ablation%20on%20CaRB.png) -->
   <div align="left">
      <img src="./img/ablation%20on%20CaRB.png" width = "80%" alt="" align=left />
   </div>

3. Comparison of various component-ablated versions of MIE on __CaRB45__
   <!-- ![ablation on CaRB45](./img/ablation%20on%20CaRB45.png) -->
   <div align="left">
      <img src="./img/ablation%20on%20CaRB45.png" width = "80%" alt="" align=left />
   </div>
   
## 四、需要解决的问题
- BERTOverflow实体识别的过程繁琐、效率不高，作者推荐训练100轮，本地训练10轮耗费7、8小时，最终效果和作者论文种提到的还有差距
- 使用BERTOverflow对大约3000条语句进行了实体识别，很多都不满足`简单句（实体数量=2）`和`复杂句（实体数量>2）`的条件，也就是句子中仅有一个或没有实体，打算准备更多的句子进行识别
- R-BERT进行分类时，准备的训练集和测试集是原公开的数据集，没有领域相关性，在实体识别阶段后，准备手工标注数据集
- 关系分类阶段对关系的划分还不够明确，复旦论文关系定义
- 未考虑实体可能包含的属性
- 用到的模型和HDSKG实验部分还没有整合到一块
- `实体数量 <1`筛选规则