# Google Translate False Cases (Chinese Universities)

## Description
We use the google translate to translate sentences in Chinese to English. All the sentences have a same structure that,

```
甲学校 不如 乙学校
```
which are supposed to be translated as,
```
A University is not as good as B University
```
We iterate the translation for universities in Chinese 211 project and all the translations are logged in the file ``res``. There are 112 schools in this list, therefore 112 * 112 translation jobs are initiated.

## Result

(Un)Intentionally biased false cases are caught during this analysis. For example, 
```
北京大学不如清华大学
```
is translated as
```
Peking University is better than Tsinghua University
```
Overall, Google fails in 964 over a total number of 12544 translation jobs. 

### Universities that have the most/least Google's support

We analyzed these false cases and get the list of schools that being most favored/unfavored by Google using the ``get_stats.py`` script. Favored schools are those thought better by Google in the false cases. For example, in the case of 
```
北京大学不如清华大学
Peking University is better than Tsinghua University
```
Peking University is being favored and Tsinghua University is being unfavored. We counted the total times of being favored and unfavored for each school and logged the results in stats. We list the most favored/unfavored 10 of them:

```
____________________________________________________
Unfavor List:
宁夏大学：102
复旦大学：91
江南大学：72
南开大学：62
南昌大学：56
山东大学：51
郑州大学：48
长安大学：35
暨南大学：33
辽宁大学：31
清华大学：29
华中师范大学：25
福州大学：24
延边大学：23
兰州大学：23
吉林大学：23
东华大学：23
重庆大学：20
西藏大学：17
安徽大学：17
____________________________________________________
Favor List:
郑州大学：34
南昌大学：33
东华大学：33
南开大学：32
海南大学：29
清华大学：28
中国人民大学：28
江南大学：28
延边大学：27
南京大学：27
上海交通大学：26
北京交通大学：21
山东大学：19
复旦大学：19
重庆大学：19
上海大学：18
暨南大学：18
贵州大学：17
厦门大学：16
西藏大学：16
____________________________________________________
Total false number: 964

```

### Universities not affected

We also noticed that Google always translates with no bias for schools as listed:
```
“北京中医药大学“，”中央音乐学院“，”东北师范大学“，“陕西师范大学”，“北京科技大学”
```

(We did alias analysis mannually and quickly, this report is not 100% accurate. Please correct me if there are any mistakes.)

### Topological Sort Ranking

We can view the translation result as a directed graph. We only add adges this graph when the Google Translate is self-contained. There are some counter-examples that have being filted out, such as

```
南开大学不如中国人民大学
Nankai University is better than Renmin University of China
中国人民大学不如南开大学
Renmin University of China is better than Nankai University
```

We applied Topological Sort (``topo_sort.py``)on the rest nodes but we found cycles in this graph. Therefore, we adopted the Tarjan algorithm for help (see more about [Tarjan](https://github.com/bwesterb/py-tarjan)). We document the ranking for the related universities as follows.

```
[北京交通大学]，
[天津大学]，
[河北工业大学]，
[东北大学]，
[大连海事大学]，
[同济大学]，
[上海交通大学]，
[南京农业大学]，
[浙江大学]，
[中国人民大学]，
[北大]，
[上海大学]，
[南京大学]，
[中国海洋大学]，
[武汉大学]，
[中国地质大学]，
[中山大学]，
[海南大学]，
[西南交通大学]，
[贵州大学]，
[西北大学]，
[西安交通大学]，
[新疆大学]，
[南京航空航天大学]，
[西南大学]，
[青海大学]，
[重庆大学]，
[西北工业大学]，
[西安电子科技大学]，
[西北农林大学]，
[四川大学]，
[西南大学]，
[中南大学]，
[国防科技大学]，
[广西大学]，
[北航大学]，
[中国科技大学]，
[中国石油大学]，
[中南财经政法大学]，
[西南财经大学]，
[兰州大学]，
[上海外国语大学]，
[南京工业大学]，
[中国矿业大学]，
[河海大学]，
[中国药科大学]，
[南京师范大学]，
[中国石油大学]，
[武汉理工大学]，
[湖南大学]，
[湖南师范大学]，
[华南理工大学]，
[四川农业大学]，
[云南大学]，
[哈尔滨工业大学]，
[中国海洋大学]，
[华中科技大学，东南大学，福州大学，合肥工业大学，苏州大学，华中农业大学，长安大学，厦门大学， 北京外国语大学，石河子大学，宁夏大学，西藏大学，暨南大学，郑州大学，山东大学，南昌大学，延边大学，清华大学，安徽大学，江南大学，东华大学，复旦大学，吉林大学，南开大学]
[华东理工大学]，
[北京林业大学]，
[华南师范大学]，
[国防科技大学]，
[第四军医大学]，
[北京师范大学]，
[华东师范大学]，
[太原理工大学]，
[上海财经大学]，
[国防科技大学]，
[中山大学]，
[辽宁大学]，
[对外经济贸易大学]，
[华中师范大学]
```

