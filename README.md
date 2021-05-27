# 特定领域知识图谱自动构建
## 一、流程
![流程图](./img/图谱流程.png)
## 二、模型：BERTOverflow & R-BERT
### 1. BERTOverflow
- 以StackOverflow数据作为语料预训练的BERT模型
- [2020-Code and Named Entity Recognition in StackOverflow](https://arxiv.org/abs/2005.01634)
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
- [2019-Enriching Pre-trained Language Model with Entity Information for Relation Classification](https://dl.acm.org/doi/abs/10.1145/3357384.3358119)
- [Github](https://github.com/monologg/R-BERT)

![R-BERT](img/R-BERT%20comprasion.jpg)

## 三、比较
1. HDSKGG
   - HDSKG中实体识别使用的是`基于词性的模式匹配`，实际中通过这些些启发式规则提取了很多噪音数据，如a powerful tool、a framework等, 而且这些噪音数据没有找到合适的办法剔除。 BERTOverflow以20种实体类型预先标注了训练语料，提取效果更好，基本不会提取出类似前面的噪音，但类别有限，也可能导致提取不到想要的实体。
   - 将预训练的BERTOverflwo模型用于实体识别，相当于识别出的实体已经有一定的领域相关性，代替了HDSKG的`Domain Relevance Estimation`部分。按道理，预训练的BERTOverflow无论是从先进性还是实用性上，都是优于原HDSKG中的方法的。
   - 
2. Stanford openIE
   - HDSKG > openIE
3. Spacy
## 四、存在的问题
- 