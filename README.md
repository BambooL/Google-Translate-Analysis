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
Beijing University is better than Tsinghua University
```
Overall, Google fails in 964 over a total number of 12544 translation jobs. 

### Universities that have the most/least Google's support

We analyzed these false cases and get the list of schools that being most favored/unfavored by Google using the ``get_stats.py`` script. Favored schools are those thought better by Google in the false cases. For example, in the case of 
```
北京大学不如清华大学
Beijing University is better than Tsinghua University
```
Beijing University is being favored and Tsinghua University is being unfavored. We counted the total times of being favored and unfavored for each school and logged the results in stats. We list the most favored/unfavored 10 of them:

```
____________________________________________________
Unfavor List:
Ningxia University: 102
Fudan University: 91
Jiangnan University: 72
Nankai University: 62
Nanchang University: 56
Shandong University: 51
Zhengzhou University: 48
Chang’an University: 35
Jinan University: 33
Liaoning University: 31
Tsinghua University: 29
Huazhong Normal University: 25
Fuzhou University: 24
Yanbian University: 23
Lanzhou University: 23
Jilin University: 23
Donghua University: 23
Chongqing University: 20
Tibet University: 17
Anhui University: 17
____________________________________________________
Favor List:
Zhengzhou University: 34
Nanchang University: 33
Donghua University: 33
Nankai University: 32
Hainan University: 29
Tsinghua University: 28
Renmin University of China: 28
Jiangnan University: 28
Yanbian University: 27
Nanjing University: 27
Shanghai Jiaotong University: 26
Beijing Jiaotong University: 21
Shandong University: 19
Fudan University: 19
Chongqing University: 19
Shanghai University: 18
Jinan University: 18
Guizhou University: 17
Xiamen University: 16
Tibet University: 16
____________________________________________________
Total false number: 964

```

### Universities not affected

We also noticed that Google always translates with no bias for schools as listed:
```
['Foreign Economic and Trade University', 'Chinese Pharmaceutical University', 'University of Defense Science and Technology', 'East China University of Technology', 'National University of Defense Science and Technology', 'Southwestern University of Finance', 'Beijing University of Chinese Medicine', 'Central Conservatory of Music', 'Northeast Normal University', 'Northwestern Polytechnical University', 'The Central Conservatory of Music', 'The Fourth Military Medical University', 'China University of Political Science and Technology', 'Shaanxi Normal University', 'Beijing University of Science and Technology', 'The University of International Business and Economics']
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
[中国地质大学]]，
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

