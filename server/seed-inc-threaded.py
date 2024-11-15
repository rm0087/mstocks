#!/usr/bin/env python3

import time
from random import randint
import os
import json
from app import app
from models import db, Company, IncomeStatement
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

## GLOBAL VARIABLES BEGIN ############################################################################################
max_workers = 8
batch_count = 100000

income_statements = []
inc_count = 0

end_count = 0

company_tracker = {}
company_count = 0

max = 10165
r = randint(1,max)

## batch_count determines how many entries will be written to the global income_statements list before committing them to DB.


main_keys = ['NetIncomeLoss',
                        'NetIncomeLossAvailableToCommonStockholdersBasic',
                        'ComprehensiveIncomeAttributableToOwnersOfParent',
                        ]
         
all_keys =  [  'Revenues',
                        'RevenueFromContractWithCustomerExcludingAssessedTax', 
                        'RevenuesNetOfInterestExpense', 
                        'RevenueFromContractWithCustomerIncludingAssessedTax', 
                        'SalesRevenueNet',
                        'SalesRevenueGoodsNet', 
                        'SalesRevenueServicesNet',
                        'InterestAndDividendIncomeOperating',
                        # 'ProfitLoss',
                        'Revenue',
                        'RevenueFromContractsWithCustomers',
                        # 'OperatingLeaseLeaseIncome',
                        ]
## GLOBAL VARIABLES END ##############################################################################################

## FUNCTIONS BEGIN #####################################################################################################
def process_company(company):
   global income_statements, inc_count, company_count, end_count
   
   if company.cik not in company_tracker.values():
      print(company.id, company.name, company.cik)
      
      file_path = f'json/CIK{company.cik_10}.json'
      with open(file_path, 'r') as json_file:
            try:
               data = json.load(json_file)
               gaap = data.get('facts', {}).get('us-gaap')
               ifrs = data.get('facts', {}).get('ifrs-full')
               end_dates = {}
               end_count = 0
               
               abc(company, gaap if gaap else ifrs, end_dates)
               
               co_inc_dict = {inc.frame: inc for inc in income_statements if inc.company_cik == company.cik}
               
               xyz(gaap if gaap else ifrs, co_inc_dict)
               
               no_r = (inc for inc in co_inc_dict.values() if inc.total_revenue == None)
               
               for inc in no_r:
                  rceat = inc.rev_from_ceat
                  rnoie = inc.rev_net_of_ie
                  rciat = inc.rev_from_ciat
                  srn = inc.sales_rev_net
                  srgn = inc.sales_rev_goods_net
                  srsn = inc.sales_rev_serv_net
                  idio = inc.interest_and_div_inc_op
                  ifrev = inc.ifrs_revenue
                  
                  if rceat:
                        inc.total_revenue = rceat
                        print(f'{inc} added total_revenues')
                  elif rciat: 
                        inc.total_revenue = rciat
                        print(f'{inc} added total_revenues')
                  elif rnoie:
                        inc.total_revenue = rnoie
                        print(f'{inc} added total_revenues')
                  elif srn: 
                        inc.total_revenue = srn
                        print(f'{inc} added total_revenues')
                  elif srgn and srsn:
                        inc.total_revenue = srgn + srsn
                  elif srgn:
                        inc.total_revenue = srgn
                        print(f'{inc} added total_revenues')
                  elif srsn:
                        inc.total_revenue = srsn
                        print(f'{inc} added total_revenues')
                  elif idio:
                        inc.total_revenue = idio
                        print(f'{inc} added total_revenues')
                  elif ifrev:
                        inc.total_revenue = ifrev
                        print(f'{inc} added total_revenues')
                  else:
                        pass
               
               print("JSON processed")
            
            except json.JSONDecodeError:
               pass
            except IntegrityError:
               print(f'{company.id} - {company.name} row already deleted')
            except Exception as e:
               print(f'{str(e)}')
   
   with lock:
      company_count += 1
      company_tracker[company_count] = company.cik


def make_inc(company, key:str, x, currency:str, end_dates):
   global inc_count, end_count
   new_inc_statement=IncomeStatement(
      company_cik = company.cik,
      start = x.get('start'),
      end =  x.get('end'),
      net_income = x.get('val'),
      form = x.get('form'),
      filed = x.get('filed'),
      accn = x.get('accn'),
      fp = x.get('fp'),
      fy = x.get('fy'),
      frame = x.get('frame'),
      key = key,
      currency = currency
   )
   income_statements.append(new_inc_statement)
   inc_count += 1
   print(inc_count, key, currency)

   end_count += 1
   end_dates[end_count] = x.get('end')
         

def amend_inc(key:str, inc, x):
   if key == 'Revenues':
      inc.total_revenue = x.get('val')
   if key == 'RevenueFromContractWithCustomerExcludingAssessedTax':
      inc.rev_from_ceat = x.get('val')
   if key == 'RevenuesNetOfInterestExpense':
      inc.rev_net_of_ie = x.get('val')
   if key == 'RevenueFromContractWithCustomerIncludingAssessedTax':
      inc.rev_from_ciat = x.get('val')
   if key == 'SalesRevenueNet':
      inc.sales_rev_net = x.get('val')
   if key == 'SalesRevenueGoodsNet':
      inc.sales_rev_goods_net = x.get('val')
   if key == 'SalesRevenueServicesNet':
      inc.sales_rev_serv_net = x.get('val')
   if key == 'InterestAndDividendIncomeOperating':
      inc.interest_and_div_inc_op = x.get('val')
   if key == 'ComprehensiveIncomeAttributableToOwnersOfParent':
      inc.net_income = x.get('val')
   if key == 'Revenue':
      inc.ifrs_revenue = x.get('val')
   if key == 'RevenueFromContractsWithCustomers':
      inc.total_revenue = x.get('val')
   if key =='OperatingLeaseLeaseIncome':
      inc.total_revenue = x.get('val')
   inc.rev_key = key
   print(inc, key, inc.currency)
   

def abc(company, path, end_dates):
   for key in main_keys:
      if path:
         path_units = path.get(key, {}).get('units', {})
         curs = list(path_units.keys())

         if path_units and path_units.get('USD', []):
            for x in path_units.get('USD', []):
               if x.get('frame') and x.get('end') not in end_dates.values():
                  make_inc(company, key, x, 'USD', end_dates)
         else:
            for cur in curs:
               if curs and path_units.get(cur, []):
                  for x in path_units.get(cur, []):
                     if x.get('frame') and x.get('end') not in end_dates.values():
                        make_inc(company, key, x, cur, end_dates)
               else:
                  pass


def xyz(path, co_inc_dict):
   for key in all_keys:
      if path:
         path_units = path.get(key, {}).get('units', {})
         curs = list(path_units.keys())

         if path_units.get('USD'):
            for x in path_units['USD']:
               inc = co_inc_dict.get(x.get('frame'))
               if inc and inc.currency == 'USD':
                  amend_inc(key, inc, x)
               else:
                  pass
         else:
            for cur in curs:
               if path_units.get(cur):
                     for x in path_units[cur]:
                        inc = co_inc_dict.get(x.get('frame'))
                        if inc and inc.currency == cur:
                           amend_inc(key, inc, x)
                        else:
                           pass
## FUNCTIONS END #####################################################################################################

# Main execution
if __name__ == "__main__":
   start_time = time.time()
   
   with app.app_context():
      print("Starting seed...")
      
      db.session.query(IncomeStatement).delete()
      db.session.commit()
      
      companies = Company.query.filter(Company.id <= max).all()
      
      lock = Lock()
      
      with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = (executor.submit(process_company, company) for company in companies)
            
            for future in as_completed(futures):
               with lock:
                  if len(income_statements) >= batch_count:
                        print(f'Committing {len(income_statements)} sheets to DB')
                        db.session.add_all(income_statements)
                        db.session.commit()
                        print(f'Committed {len(income_statements)} sheets to DB')
                        income_statements.clear()
      
            print("Committing remaining income statements...")
            with lock:
               if len(income_statements) > 0:
                  db.session.add_all(income_statements)
                  db.session.commit()
                  print(f'Committed all new income statements to DB')
      
      end_time = time.time()
      elapsed = end_time - start_time
      print(f'{elapsed} seconds elapsed')
      print("Seed successful")