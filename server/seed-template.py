#!/usr/bin/env python3

# Standard library imports
from random import random, randint, choice as rc
import os
import json


# Remote library imports


# Local imports
from app import app
from models import db, Company
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

to_db = []

with app.app_context():
   
   companies = Company.query.all()
   print("Starting seed...")
   for company in companies:


      db.session.refresh(company)
      print(company.id, company.name, company.cik)
      
      
      file_path = f'json/submissions/CIK{company.cik_10}.json'
      json_file = open(file_path,'r')
      
      try:
         data = json.load(json_file)
         # company.sic_id = data['sic']
         # company.sic_title = data['sicDescription']
         company.owner_org = data['ownerOrg']
         to_db.append(company)
      
      except json.JSONDecodeError:
         pass
      except IntegrityError:
         print(f'{company.id} - {company.name} row already deleted')
      except Exception as e:
         print(f'{str(e)}')

   
   if len(to_db) > 0:
      db.session.add_all(to_db)
      db.session.commit()
   print("Seed successful")
