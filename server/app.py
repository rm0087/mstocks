#!/usr/bin/env python3

# Standard library imports

# Remote library imports
# from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from models import Company, Keyword, company_keyword_assoc, Note, BalanceSheet, IncomeStatement, CashFlowsStatement
from sqlalchemy import not_
import json
import os

# Local imports
from config import app, db, api


@app.post('/companies')
def get_all_companies():
    data = request.json
    try:
        company = Company.query.filter(Company.ticker == data.upper()).first()
        return jsonify(company.to_dict()), 200
    except Exception as e:
        return{'error': str(e)}, 404

# @app.get('/balance_sheets/<int:cik>')
# def get_balancesheets(cik):
#     balance_sheets = BalanceSheet.query.filter(BalanceSheet.company_cik == cik
#                                                ).order_by(BalanceSheet.end).all()
#     if not balance_sheets:
#         return jsonify({"error": "Balance sheets not found"}), 404
#     return jsonify([bs.to_dict() for bs in balance_sheets]), 200

# @app.get('/income_statements/<int:cik>')
# def get_income_statements(cik):
#     income_statements = IncomeStatement.query.filter(IncomeStatement.company_cik == cik, 
#                                                      IncomeStatement.frame.like('%Q%')
#                                                      ).order_by(IncomeStatement.end).all()
#     if not income_statements:
#         return jsonify({"error": "Balance sheets not found"}), 404
#     return jsonify([income_statement.to_dict() for income_statement in income_statements]), 200

# @app.get('/cf_statements/<int:cik>')
# def get_cf_statements(cik):
#     cf_statements = CashFlowsStatement.query.filter(CashFlowsStatement.company_cik == cik, 
#                                                      not_(CashFlowsStatement.frame.like('%Q%'))
#                                                      ).order_by(CashFlowsStatement.end).all()
#     if not cf_statements:
#         return jsonify({"error": "Balance sheets not found"}), 404
#     return jsonify([cf_statement.to_dict() for cf_statement in cf_statements]), 200

# @app.get('/companyfacts2/<string:ticker>')
# def get_companyfacts_ticker(ticker):
#     company = Company.query.filter(Company.ticker == ticker.upper()).first()
#     file_path = f'json/CIK{company.cik_10}.json'
#     with open(file_path, 'r') as file:
#         data = file.read()
#     return data, 200, {'Content-Type': 'application/json'}

# @app.post('/companies')
# def post_companies():
#     try:    
#         data = request.json
#         companies = [Company(cik=company[0], name=company[1], ticker=company[2], exchange=company[3]) for company in data['companies']]
#         db.session.add_all(companies)
#         db.session.commit()
#         return {'success': 'companies posted'},200
#     except Exception as e:
#         return {'error': str(e)}, 400
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)

