from django.contrib import admin
from .models import (
    Securities,
    Companies,
    balance_sheet,
    income_statement,
    financial_analysis,
    esg_data
)

# 配置 Securities 模型管理后台
@admin.register(Securities)
class SecuritiesAdmin(admin.ModelAdmin):
    list_display = ('securities_code', 'sec_englishname', 'ipo_date', 'exch_eng', 'country')
    search_fields = ('securities_code', 'sec_englishname')
    list_filter = ('exch_eng', 'country')
    ordering = ('ipo_date',)

# 配置 Companies 模型管理后台
@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('company_code', 'comp_name_eng', 'securities_code', 'industry_swcode_2021', 'founddate1')
    search_fields = ('comp_name_eng', 'securities_code__securities_code')
    list_filter = ('industry_swcode_2021', 'founddate1')
    ordering = ('founddate1',)

# 配置 balance_sheet 模型管理后台
@admin.register(balance_sheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = ('balance_code', 'windcode', 'tot_assets', 'tot_liab', 'eqy_belongto_parcomsh')
    search_fields = ('balance_code', 'windcode__securities_code')
    list_filter = ('tot_assets', 'tot_liab')
    ordering = ('balance_code',)

# 配置 income_statement 模型管理后台
@admin.register(income_statement)
class IncomeStatementAdmin(admin.ModelAdmin):
    list_display = ('income_code', 'balance_code', 'tot_oper_rev', 'tot_profit', 'net_profit_is')
    search_fields = ('income_code', 'balance_code__balance_code')
    list_filter = ('tot_oper_rev', 'net_profit_is')
    ordering = ('income_code',)

# 配置 financial_analysis 模型管理后台
@admin.register(financial_analysis)
class FinancialAnalysisAdmin(admin.ModelAdmin):
    list_display = ('faid', 'balance_code', 'eps_basic', 'roe_basic', 'current', 'quick')
    search_fields = ('faid', 'balance_code__balance_code')
    list_filter = ('eps_basic', 'roe_basic', 'current', 'quick')
    ordering = ('faid',)

# 配置 esg_data 模型管理后台
@admin.register(esg_data)
class ESGDataAdmin(admin.ModelAdmin):
    list_display = ('esg_reportid', 'company_code', 'esg_rating_wind', 'esg_escore_wind', 'esg_sscore_wind')
    search_fields = ('esg_reportid', 'company_code__company_code', 'esg_rating_wind')
    list_filter = ('esg_rating_wind', 'esg_escore_wind', 'esg_sscore_wind')
    ordering = ('esg_reportid',)