import urllib3
import time
import random
import os
from app import app
from models import Company
# import requests
# import json

proxy_url = 'http://cneeyhab:bdo8b3zg5pcd@38.154.227.167:5868'

http = urllib3.PoolManager()

headers = {'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'
            }

company_tracker = {}
company_count = 0

with app.app_context():
    
    companies = Company.query.all()

    for company in companies:
        if company.cik not in company_tracker.values():
            r = http.request('GET',f"https://data.sec.gov/api/xbrl/companyfacts/CIK{company.cik_10}.json",headers=headers)
            # r = http.request('GET',f"https://data.sec.gov/submissions/CIK{company.cik_10}.json",headers=headers)
            
            print(r.data)
            print(f'{company.id}/{len(companies)}')
            
            full_path = os.path.join('server/json', f'CIK{company.cik_10}.json')
            f = open(full_path, 'wb')
            f.write(r.data)
            f.close()
        else:
            pass
            
        time.sleep(random.uniform(2.434, 4.897))
        
        company_count += 1
        company_tracker[company_count] = company.cik

