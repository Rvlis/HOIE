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


## 三、Dataset
1. CaRB：CaRB is a dataset cum evaluation framework for benchmarking Open Information Extraction systems, which has a size of 641 sentence.


2. CaRB-complex-45：CaRB45 is a dataset seleceted from CaRB, which has a size of 45 sentences. Each sentence has following features:
   - It is a compound sentence.
   - It includes at least two fact triples.
   - It doesn't involve reporting verbs like __said__, __told__, __asked__, etc.

## 四、Evaluation

1. Performance of MIE and various Open IE systems on CaRB
   
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
      <img src="./img/ablation%20on%20CaRB.png" width = "80%" alt="" align=center />
   </div>


3. Comparison of various component-ablated versions of MIE on __CaRB45__
   <!-- ![ablation on CaRB45](./img/ablation%20on%20CaRB45.png) -->
   <div align="left">
      <img src="./img/ablation%20on%20CaRB45.png" width = "80%" alt="" align=center />
   </div>
   