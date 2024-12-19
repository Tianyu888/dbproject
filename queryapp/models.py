from django.db import models

class Securities(models.Model):
    securities_code = models.CharField(max_length=50, unique=True,  primary_key=True)
    sec_englishname = models.CharField(max_length=255)
    ipo_date = models.DateField()
    exch_eng = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.sec_englishname



class Companies(models.Model):
    company_code = models.CharField(max_length=50, primary_key=True) 
    securities_code = models.ForeignKey(Securities, on_delete=models.CASCADE, related_name="companies")
    comp_name_eng = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    industry_swcode_2021 = models.CharField(max_length=50, blank=True, null=True)
    founddate1 = models.DateField(blank=True, null=True)
    regcapital = models.FloatField(blank=True, null=True)
    employee = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.comp_name_eng



class balance_sheet(models.Model):
    balance_code = models.CharField(max_length=50, unique=True, primary_key=True)
    windcode = models.ForeignKey(Securities, on_delete=models.CASCADE, related_name="balancesheets")
    tot_assets = models.FloatField(blank=True, null=True)
    tot_cur_assets = models.FloatField(blank=True, null=True)
    inventories = models.FloatField(blank=True, null=True)
    fix_assets = models.FloatField(blank=True, null=True)
    tot_liab = models.FloatField(blank=True, null=True)
    tot_non_cur_liab = models.FloatField(blank=True, null=True)
    tot_cur_liab = models.FloatField(blank=True, null=True)
    eqy_belongto_parcomsh = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.balance_code



class income_statement(models.Model):
    income_code = models.CharField(max_length=50, unique=True, primary_key=True)
    balance_code = models.ForeignKey(balance_sheet, on_delete=models.CASCADE, related_name="incomestatements")
    tot_oper_rev = models.FloatField(blank=True, null=True)
    tot_oper_cost = models.FloatField(blank=True, null=True)
    opprofit = models.FloatField(blank=True, null=True)
    tot_profit = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    net_profit_is = models.FloatField(blank=True, null=True)
    tot_compreh_inc_parent_comp = models.FloatField(blank=True, null=True)
    selling_dist_exp = models.FloatField(blank=True, null=True)
    gerl_admin_exp = models.FloatField(blank=True, null=True)
    rd_exp = models.FloatField(blank=True, null=True)
    fin_exp_is = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.income_code



class financial_analysis(models.Model):
    faid = models.CharField(max_length=50, unique=True, primary_key=True)  
    balance_code = models.ForeignKey(balance_sheet, on_delete=models.CASCADE, related_name="financialanalysis")
    eps_basic = models.FloatField(blank=True, null=True) 
    roe_basic = models.FloatField(blank=True, null=True)  
    profittogr = models.FloatField(blank=True, null=True)  
    current = models.FloatField(blank=True, null=True)
    quick = models.FloatField(blank=True, null=True)
    fa_debttoeqy = models.FloatField(blank=True, null=True)
    invturndays = models.FloatField(blank=True, null=True)
    invturn = models.FloatField(blank=True, null=True)
    turnover_ttm = models.FloatField(blank=True, null=True)
    yoy_tr = models.FloatField(blank=True, null=True)
    yoyprofit = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.faid



class esg_data(models.Model):
    esg_reportid = models.CharField(max_length=50, unique=True, primary_key=True)
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name="esg")
    esg_rating_wind = models.CharField(max_length=50, blank=True, null=True)
    esg_escore_wind = models.FloatField(blank=True, null=True)
    esg_sscore_wind = models.FloatField(blank=True, null=True)
    esg_gscore_wind = models.FloatField(blank=True, null=True)
    esg_rating_ftserussell = models.CharField(max_length=50, blank=True, null=True)
    esg_mgmtscore_wind2 = models.FloatField(blank=True, null=True)
    esg_eventscore_wind2 = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.esg_reportid