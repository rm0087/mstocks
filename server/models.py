from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy import func, Index
from datetime import datetime

from config import db


company_keyword_assoc = db.Table(
    'company_keyword_assoc', db.metadata,
    db.Column('company_id', db.Integer, db.ForeignKey('companies_table.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords_table.id'))
)

class Company(db.Model, SerializerMixin):
    __tablename__ = "companies_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ticker = db.Column(db.String, nullable=False)
    cik = db.Column(db.Integer, nullable=False)
    exchange = db.Column(db.String)
    cik_10 = db.Column(db.String)
    sic_id = db.Column(db.Integer)
    sic_title = db.Column(db.String)
    owner_org = db.Column(db.String)

    # balance_sheets = db.relationship('BalanceSheet', backref='company', lazy=True)
    keywords = db.relationship('Keyword', back_populates='companies', secondary = company_keyword_assoc)
    notes = db.relationship('Note', back_populates='company')

    income_statements = db.relationship('IncomeStatement', back_populates='company')
    balance_sheets = db.relationship('BalanceSheet', back_populates='company')
    cash_flows = db.relationship('CashFlowsStatement', back_populates='company')

    serialize_rules = ('-income_statements.company', '-balance_sheets.company', '-cash_flows.company')

    __table_args__ = (
        Index('idx_ticker', 'ticker'),
    )

    # @validates('keywords')
    # def validate_keywords(self, key, keyword):
    #     if not isinstance(keyword, Keyword):
    #         raise ValueError("Entry must be a valid Keyword class member")
    #     return keyword
    
    # @validates('balance_sheets')
    # def validate_balance_sheets(self, key, balance_sheet):
    #     if not isinstance(balance_sheet, BalanceSheet):
    #         raise ValueError("Entry must be a valid BalanceSheet class member")
    #     return balance_sheet
    
    # @validates('notes')
    # def validate_notes(self, key, note):
    #     if not isinstance(note, Note):
    #         raise ValueError("Entry must be a valid Note class member")
    #     return note
    

class BalanceSheet(db.Model, SerializerMixin):
    __tablename__ = "bs_table"

    id = db.Column(db.Integer, primary_key=True)
    company_cik = db.Column(db.Integer, db.ForeignKey('companies_table.cik'), nullable=False)
    
    total_assets = db.Column(db.Integer)
    assets_current = db.Column(db.Integer)
    assets_noncurrent = db.Column(db.Integer)

    total_liabilities = db.Column(db.Integer)
    liabilities_current = db.Column(db.Integer)
    liabilities_noncurrent = db.Column(db.Integer)
    total_liabilities_and_stockholders_equity = db.Column(db.Integer)

    total_stockholders_equity = db.Column(db.Integer)
    total_stockholders_equity_nci = db.Column(db.Integer)
    
    cash = db.Column(db.Integer)
    cash_and_equiv = db.Column(db.Integer)
    cash_all = db.Column(db.Integer)
    goodwill = db.Column(db.Integer)
    intangible_assets = db.Column(db.Integer)
    

    accn = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    filed = db.Column(db.String)
    form = db.Column(db.String)
    fp = db.Column(db.String)
    frame = db.Column(db.String)
    fy = db.Column(db.Integer)

    company = db.relationship('Company', back_populates="balance_sheets", lazy=True)

    serialize_rules = ('-company.balance_sheets',)

    __table_args__ = (
        Index('idx_company_cik', 'company_cik'),
    )

class IncomeStatement(db.Model, SerializerMixin):
    __tablename__ = "inc_table"

    id = db.Column(db.Integer, primary_key=True)
    company_cik = db.Column(db.Integer, db.ForeignKey('companies_table.cik'), nullable=False)

    total_revenue = db.Column(db.Integer)
    rev_from_ceat = db.Column(db.Integer)
    rev_net_of_ie = db.Column(db.Integer)
    rev_from_ciat = db.Column(db.Integer)
    sales_rev_net = db.Column(db.Integer)
    sales_rev_goods_net = db.Column(db.Integer)
    sales_rev_serv_net = db.Column(db.Integer)
    interest_and_div_inc_op = db.Column(db.Integer)
    net_income = db.Column(db.Integer)
    ifrs_revenue = db.Column(db.Integer)

    accn = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    filed = db.Column(db.String)
    form = db.Column(db.String)
    fp = db.Column(db.String)
    frame = db.Column(db.String)
    fy = db.Column(db.Integer)
    currency = db.Column(db.Integer)
    accounting_standard = db.Column(db.String)
    

    key = db.Column(db.String)
    rev_key = db.Column(db.String)

    company = db.relationship('Company', back_populates="income_statements", lazy=True)

    serialize_rules = ('-company.income_statements',)

class CashFlowsStatement(db.Model, SerializerMixin):
    __tablename__ = "cf_table"

    id = db.Column(db.Integer, primary_key=True)
    company_cik = db.Column(db.Integer, db.ForeignKey('companies_table.cik'), nullable=False)

    opr_cf = db.Column(db.Integer)
    inv_cf = db.Column(db.Integer)
    fin_cf = db.Column(db.Integer)
    net_cf = db.Column(db.Integer)

    accn = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    filed = db.Column(db.String)
    form = db.Column(db.String)
    fp = db.Column(db.String)
    frame = db.Column(db.String)
    fy = db.Column(db.Integer)

    op_cf_key = db.Column(db.String)
    inv_cf_key = db.Column(db.String)
    fin_cf_key = db.Column(db.String)

    company = db.relationship('Company', back_populates="cash_flows", lazy=True)

    serialize_rules = ('-company.cash_flows',)

class Keyword(db.Model, SerializerMixin):
    __tablename__ = "keywords_table"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    t = db.Column(db.String)
    description = db.Column(db.String)
    
    companies = db.relationship('Company', back_populates = 'keywords', secondary = company_keyword_assoc)
    type = db.relationship('Type', back_populates='keywords')
    type_id = db.Column(db.Integer, db.ForeignKey('keyword_types.id'))

    serialize_rules = ('-companies', '-type.keywords')

    @validates('type')
    def validate_type(self, key, type):
        if not isinstance(type, Type):
            raise ValueError("Entry must be a valid Type class member")
        return type


class Note(db.Model, SerializerMixin):
    __tablename__ = "notes_table"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies_table.id'))
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    company = db.relationship('Company', back_populates="notes")

    serialize_rules = ('-company',)

class Type(db.Model, SerializerMixin):
    __tablename__ = "keyword_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)

    keywords = db.relationship('Keyword', back_populates='type')

    serialize_rules = ('-keywords.type',)

    @validates('keywords')
    def validate_keyword(self, key, keyword):
        if not isinstance(keyword, Keyword):
            raise ValueError("Entry must be a valid Keyword class member")
        return keyword

# class Shares(db.Model, SerializerMixin):
#     __tablename__ = "shares_table"

#     id = db.Column(db.Integer, primary_key=True)
#     company_id = db.Column(db.Integer, db.ForeignKey('companies_table.id'), nullable=False)
#     date = db.Column(db.String)
#     historical_shares = db.Column(db.Integer)
#     split_coefficient = db.Column(db.Integer)
#     adjusted_shares = db.Column(db.Integer)


    