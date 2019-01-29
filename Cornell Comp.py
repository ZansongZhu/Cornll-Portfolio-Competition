
# input，transform the customer needs into Risk averse
# 就是客户输入转换为风险偏好等评分，

import pandas as pd
import numpy as np
import io
import requests

url = 'https://raw.githubusercontent.com/xinyexu/Cornll-Portfolio-Competition/master/Sample_input.csv'
url2 = 'https://raw.githubusercontent.com/xinyexu/Cornll-Portfolio-Competition/master/Criteria%20Setting.csv'
input_f = requests.get(url).content
df = pd.read_csv(io.StringIO(input_f.decode('utf-8'))) # customer sample data
input_f = requests.get(url2).content
crit = pd.read_csv(io.StringIO(input_f.decode('utf-8'))) # rating criteria

# age_rat
df['age'] = 2019 - df['born_y']
dic_age = {crit['Age-st'][i]:i+1 for i in range(0,10)}
df['cal'] = df['age'] - df['age'] % 5
df['age_rat'] = [dic_age[x] for x in df['cal']] # range 5 for each interval???


# family_inc_rat
bins = [x for x in crit['family_inc']]
bins.append(np.inf)
names = [i for i in range(1,11)]
df['family_inc_rat'] = pd.cut(df['family_inc'], bins, labels=names)

# start_amo_rat
df['start/fam'] = df['start_amo'] / df['family_inc']
bins2 = [x for x in crit['start_amo']]
bins2.append(np.inf)
df['start_amo_rat'] = pd.cut(df['start/fam'], bins2, labels=names)

# contri_em_rat # most are below 5!!!
df['contri/fam'] = df['contri_em'] / df['family_inc']
bins4 = [x for x in crit['contri_em']]
bins4.append(np.inf)
df['contri_em_rat'] = pd.cut(df['contri/fam'], bins4, labels=names)

# Time_horiz
bins5 = [x for x in crit['Time_horiz']]
bins5.append(np.inf)
names_inv = [i for i in range(10, 0, -1)]
df['Time_horiz_rat'] = pd.cut(df['contri/fam'], bins4, labels=names_inv)  # inversely related

# risk perference rating system
df[["family_inc_rat", "start_amo_rat", 'contri_em_rat', 'Time_horiz_rat']] = df[["family_inc_rat", "start_amo_rat",
    'contri_em_rat', 'Time_horiz_rat']].apply(pd.to_numeric)
df['total_rat'] = (df['age_rat'] + df['family_inc_rat'] +
                   df['start_amo_rat'] + df['contri_em_rat'] + df['Time_horiz_rat']) / 5

# inv_selec: decided by subjective risk_tol, total_rat, inv_goal
# inv_goal haven't been included
df['inv_selec'] = round((df['risk_tol'] + df['total_rat']) / 2)



# Variables and meanings
# born_y: Born year:
# acc_user: and this account is for? (1: just me ; 2: me and partner)
# inv_for: I am investing for?  (retirement / something else)
# acc_type: and my preferred account type is? (tax advantaged (IRA)/ taxable (Brokerage)
# start_amo, contri_em: I have $ to start and want to contribute $ each month?
# family_inc: My household's total c before taxes is about $ ?
# risk_tol: Where would you be most comfortable placing yourself on the risk tolerance scale from 1 to 10? (More risk :10)

# output: index of different asset allocation strategy


# may use vNM expected utility theory expected utility theory
# https://www.princeton.edu/~markus/teaching/Fin501/04Lecture.pdf
# df['family_inc_rat'] = [min(crit['family_inc'], key=lambda x:abs(x-each)) for each in df['family_inc']] # min to cal the cloest number
