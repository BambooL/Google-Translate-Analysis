# Google Translate False Cases (Chinese Universities)

## Description
We use the google translate to translate sentences in Chinese to English. All the sentences have a same structure that,

'''
甲学校 不如 乙学校
'''
which are supposed to be translated as,
'''
A University is not as good as B University
'''

We iterate the translation for universities in Chinese 211 project and all the translations are logged in the file ''res''. There are 112 schools in this list, therefore 112 * 112 translation jobs are initiated.

## Result

(Un)Intentionally biased false cases are caught during this analysis. For example, 
'''
北京大学不如清华大学
'''
is translated as
'''
Beijing University is better than Tsinghua University
'''

Overall, Google fails in 964 over a total number of 12544 translation jobs. 

### Universities that have the most/least Google's support

We analyzed these false cases and get the list of schools that being most favored/unfavored by Google using the ''get_stats.py'' script. Favored schools are those thought better by Google in the false cases. For example, in the case of 
'''
北京大学不如清华大学
Beijing University is better than Tsinghua University
'''
Beijing University is being favored and Tsinghua University is being unfavored. We counted the total times of being favored and unfavored for each school and logged the results in stats. We list the most favored/unfavored 10 of them:

'''
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

'''

### Universities not affected

We also noticed that Google always translates with no bias for schools as listed:
'''
['Foreign Economic and Trade University', 'Chinese Pharmaceutical University', 'University of Defense Science and Technology', 'East China University of Technology', 'National University of Defense Science and Technology', 'Southwestern University of Finance', 'Beijing University of Chinese Medicine', 'Central Conservatory of Music', 'Northeast Normal University', 'Northwestern Polytechnical University', 'The Central Conservatory of Music', 'The Fourth Military Medical University', 'China University of Political Science and Technology', 'Shaanxi Normal University', 'Beijing University of Science and Technology', 'The University of International Business and Economics']
'''


(We did alias analysis mannually and quickly, this report is not 100% accurate. Please correct me if there are any mistakes.)


