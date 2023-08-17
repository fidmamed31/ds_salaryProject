import glassdoor_scraper as gs 
import pandas as pd 

path = "C:/Users/mafidma/Documents/ds_salary_proj/chromedriver"

df = gs.get_jobs('data scientist',100, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)