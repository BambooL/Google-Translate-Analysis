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


