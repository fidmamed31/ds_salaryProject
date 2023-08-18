# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:25:17 2023

@author: mafidma
"""

import pandas as pd

df=pd.read_csv('glassdoor_jobs.csv')



#salary_parsing

df=df[df["Salary Estimate"]!="-1"]
df["salary per hour"]=df["Salary Estimate"].apply(lambda x:1 if "per hour" in x.lower() else 0)

df["employer provided salary"]= df["Salary Estimate"].apply(lambda x:1 if "employer provided salary" in x.lower() else 0)

salary=df["Salary Estimate"].apply(lambda x:x.split("(")[0])
minus_kd=salary.apply(lambda x: x.replace("K","").replace("$",""))



minus_hr=minus_kd.apply(lambda x: x.lower().replace("per hour","").replace("employer provided salary:",""))


df["min_salary"]=minus_hr.apply(lambda x:int(x.split("-")[0]))
df["max_salary"]=minus_hr.apply(lambda x:int(x.split("-")[1]))

df["salary_avg"]=(df.min_salary + df.max_salary)/2

#company name text only 


df["company_text"]=df.apply(lambda x: x["Company Name"] if x["Rating"] <0 else x["Company Name"][:-3], axis=1)

#state feild

df["state"]=df["Location"].apply(lambda x: x.split(",")[1])
print(df.state.value_counts())

df["same_state"]=df.apply(lambda x:1 if x.Location == x.Headquarters else 0, axis=1)
#age of company

df["Company_age"]=df["Founded"].apply(lambda x:(2023-x) if x>0 else x)

#python
df["python"]=df["Job Description"].apply(lambda x:1 if "python" in x.lower() else 0)

df.python.value_counts()

#remove irrelevant features
df_out=df.drop(["Unnamed: 0"],axis=1)

df_out.to_csv("salary_data_cleaned.csv",index=False)

pd.read_csv("salary_data_cleaned.csv")
