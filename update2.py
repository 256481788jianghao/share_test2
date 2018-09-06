import tushare as ts
import pandas as pd
import os
import datetime

pd.set_option('max_rows',1000)

baseDir = './database2'
if not os.path.exists(baseDir):
    os.mkdir(baseDir)


ts.set_token('edd599506620c2fa4466f6ff765ff458d3dd894b136356c68b8baa32')
ts_api = ts.pro_api()



todaytime = datetime.datetime.now()
today_str = todaytime.strftime('%Y_%m_%d')
today_str2 = todaytime.strftime('%Y%m%d')


#get trade cal
stock_trade_cal_filename = baseDir+"/"+"trade_cal_"+today_str+".csv"
stock_trade_cal_info = None
if not os.path.exists(stock_trade_cal_filename):
    stock_trade_cal_info_tmp = ts_api.trade_cal(start_date='20160101',end_date=today_str2)
    stock_trade_cal_info_tmp.to_csv(stock_trade_cal_filename,encoding='utf-8')

stock_trade_cal_info = pd.read_csv(stock_trade_cal_filename,encoding='utf-8',index_col=0)


def get_stockdata_by_date(item):
    if item.is_open == 1:
        dateStr = str(item.cal_date)
        stockdata_filename = baseDir+'/stock_'+dateStr+'.csv'
        stockdata_adjust_filename = baseDir+'/stock_adjust_'+dateStr+'.csv'
        if not os.path.exists(stockdata_filename):
            try:
                data = ts_api.daily(trade_date=dateStr)
                data.to_csv(stockdata_filename,encoding='utf-8')
                print(stockdata_filename+' finish')
            except Exception as e:
                print(e)
        if not os.path.exists(stockdata_adjust_filename):
            try:
                data_adjust = ts_api.adj_factor(trade_date=dateStr)
                data_adjust.to_csv(stockdata_adjust_filename,encoding='utf-8')
                print(stockdata_adjust_filename+' finish')
            except Exception as e:
                print(e)
            
stock_trade_cal_info.apply(get_stockdata_by_date,axis=1)



#get all stock code list
stock_base_info_filename = baseDir+"/"+"baseInfo_"+today_str+".csv"
stock_base_info = None
stock_base_info_tmp = ts_api.stock_basic(list_status='L')
stock_base_info_tmp.to_csv(stock_base_info_filename,encoding='utf-8')

#stock_base_info = pd.read_csv(stock_base_info_filename,encoding='utf-8',index_col=0)
'''
report_year = ['2018']
for year in report_year:
    start_year = int(year) - 2
    startDate = str(start_year)+'0101'
    endDate = year+'0430'
    stock_len = len(stock_base_info)
    report_index = 0
    for code in stock_base_info.ts_code:
        report_index = report_index + 1
        report_income_filename = baseDir+'/report_income'+'_'+code+'.csv'
        if not os.path.exists(report_income_filename):
            report_income = ts_api.income(ts_code=code,start_date=startDate,end_date=endDate)
            report_income.to_csv(report_income_filename,encoding='utf-8')
            
        report_balancesheet_filename = baseDir+'/report_balancesheet'+'_'+code+'.csv'
        if not os.path.exists(report_balancesheet_filename):
            report_balancesheet = ts_api.balancesheet(ts_code=code,start_date=startDate,end_date=endDate)
            report_balancesheet.to_csv(report_balancesheet_filename,encoding='utf-8')

        report_cashflow_filename = baseDir+'/report_cashflow'+'_'+code+'.csv'
        if not os.path.exists(report_cashflow_filename):
            report_cashflow = ts_api.cashflow(ts_code=code,start_date=startDate,end_date=endDate)
            report_cashflow.to_csv(report_cashflow_filename,encoding='utf-8')

            
        print(code+" report "+str(report_index)+"/"+str(stock_len))



stock_len = len(stock_base_info)
stock_update_index = 0
for code in stock_base_info.ts_code:
    stock_update_index = stock_update_index + 1
    data_filename = baseDir+'/'+code+'.csv'
    data_need_update = False
    if os.path.exists(data_filename):
        data_tmp = pd.read_csv(data_filename,encoding='utf-8',index_col=0)
        data_time = datetime.datetime.strptime(str(data_tmp.trade_date.iloc[0]), "%Y%m%d")
        delta = todaytime - data_time
        if todaytime.weekday() < 5 and delta.days == 1 and todaytime.hour >= 23:
            data_need_update = True
        elif todaytime.weekday() < 5 and delta.days > 1:
            data_need_update = True
        elif todaytime.weekday() == 5 and delta.days > 1:
            data_need_update = True
        elif todaytime.weekday() == 6 and delta.days > 2:
            data_need_update = True
    else:
        data_need_update = True
    if data_need_update:
        data = ts_api.daily(ts_code=code,start_date='2016-1-1')
        data.to_csv(data_filename,encoding='utf-8')
        
    print(code+" "+str(stock_update_index)+"/"+str(stock_len))
'''
'''
exchange_id	str	交易所 SSE上交所 SZSE深交所
cal_date	str	日历日期
is_open	int	是否交易 0休市 1交易
pretrade_date	str	上一个交易日
'''

'''
ts_code	str	股票代码
trade_date	str	交易日期
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
pre_close	float	昨收价
change	float	涨跌额
pct_change	float	涨跌幅
vol	float	成交量 （手）
amount	float	成交额 （千元）
'''

'''
ts_code	str	TS股票代码
ann_date	str	公告日期
f_ann_date	str	实际公告日期，即发生过数据变更的最终日期
end_date	str	报告期
report_type	str	报告类型： 参考下表说明
comp_type	str	公司类型：1一般工商业 2银行 3保险 4证券
basic_eps	float	基本每股收益
diluted_eps	float	稀释每股收益
total_revenue	float	营业总收入
revenue	float	营业收入
int_income	float	利息收入
prem_earned	float	已赚保费
comm_income	float	手续费及佣金收入
n_commis_income	float	手续费及佣金净收入
n_oth_income	float	其他经营净收益
n_oth_b_income	float	加:其他业务净收益
prem_income	float	保险业务收入
out_prem	float	减:分出保费
une_prem_reser	float	提取未到期责任准备金
reins_income	float	其中:分保费收入
n_sec_tb_income	float	代理买卖证券业务净收入
n_sec_uw_income	float	证券承销业务净收入
n_asset_mg_income	float	受托客户资产管理业务净收入
oth_b_income	float	其他业务收入
fv_value_chg_gain	float	加:公允价值变动净收益
invest_income	float	加:投资净收益
ass_invest_income	float	其中:对联营企业和合营企业的投资收益
forex_gain	float	加:汇兑净收益
total_cogs	float	营业总成本
oper_cost	float	减:营业成本
int_exp	float	减:利息支出
comm_exp	float	减:手续费及佣金支出
biz_tax_surchg	float	减:营业税金及附加
sell_exp	float	减:销售费用
admin_exp	float	减:管理费用
fin_exp	float	减:财务费用
assets_impair_loss	float	减:资产减值损失
prem_refund	float	退保金
compens_payout	float	赔付总支出
reser_insur_liab	float	提取保险责任准备金
div_payt	float	保户红利支出
reins_exp	float	分保费用
oper_exp	float	营业支出
compens_payout_refu	float	减:摊回赔付支出
insur_reser_refu	float	减:摊回保险责任准备金
reins_cost_refund	float	减:摊回分保费用
other_bus_cost	float	其他业务成本
operate_profit	float	营业利润
non_oper_income	float	加:营业外收入
non_oper_exp	float	减:营业外支出
nca_disploss	float	其中:减:非流动资产处置净损失
total_profit	float	利润总额
income_tax	float	所得税费用
n_income	float	净利润(含少数股东损益)
n_income_attr_p	float	净利润(不含少数股东损益)
minority_gain	float	少数股东损益
oth_compr_income	float	其他综合收益
t_compr_income	float	综合收益总额
compr_inc_attr_p	float	归属于母公司(或股东)的综合收益总额
compr_inc_attr_m_s	float	归属于少数股东的综合收益总额
ebit	float	息税前利润
ebitda	float	息税折旧摊销前利润
insurance_exp	float	保险业务支出
undist_profit	float	年初未分配利润
distable_profit	float	可分配利润
'''

'''
ts_code	str	TS股票代码
ann_date	str	公告日期
f_ann_date	str	实际公告日期
end_date	str	报告期
report_type	str	报表类型：见下方详细说明
comp_type	str	公司类型：1一般工商业 2银行 3保险 4证券
total_share	float	期末总股本
cap_rese	float	资本公积金
undistr_porfit	float	未分配利润
surplus_rese	float	盈余公积金
special_rese	float	专项储备
money_cap	float	货币资金
trad_asset	float	交易性金融资产
notes_receiv	float	应收票据
accounts_receiv	float	应收账款
oth_receiv	float	其他应收款
prepayment	float	预付款项
div_receiv	float	应收股利
int_receiv	float	应收利息
inventories	float	存货
amor_exp	float	长期待摊费用
nca_within_1y	float	一年内到期的非流动资产
sett_rsrv	float	结算备付金
loanto_oth_bank_fi	float	拆出资金
premium_receiv	float	应收保费
reinsur_receiv	float	应收分保账款
reinsur_res_receiv	float	应收分保合同准备金
pur_resale_fa	float	买入返售金融资产
oth_cur_assets	float	其他流动资产
total_cur_assets	float	流动资产合计
fa_avail_for_sale	float	可供出售金融资产
htm_invest	float	持有至到期投资
lt_eqt_invest	float	长期股权投资
invest_real_estate	float	投资性房地产
time_deposits	float	定期存款
oth_assets	float	其他资产
lt_rec	float	长期应收款
fix_assets	float	固定资产
cip	float	在建工程
const_materials	float	工程物资
fixed_assets_disp	float	固定资产清理
produc_bio_assets	float	生产性生物资产
oil_and_gas_assets	float	油气资产
intan_assets	float	无形资产
r_and_d	float	研发支出
goodwill	float	商誉
lt_amor_exp	float	长期待摊费用
defer_tax_assets	float	递延所得税资产
decr_in_disbur	float	发放贷款及垫款
oth_nca	float	其他非流动资产
total_nca	float	非流动资产合计
cash_reser_cb	float	现金及存放中央银行款项
depos_in_oth_bfi	float	存放同业和其它金融机构款项
prec_metals	float	贵金属
deriv_assets	float	衍生金融资产
rr_reins_une_prem	float	应收分保未到期责任准备金
rr_reins_outstd_cla	float	应收分保未决赔款准备金
rr_reins_lins_liab	float	应收分保寿险责任准备金
rr_reins_lthins_liab	float	应收分保长期健康险责任准备金
refund_depos	float	存出保证金
ph_pledge_loans	float	保户质押贷款
refund_cap_depos	float	存出资本保证金
indep_acct_assets	float	独立账户资产
client_depos	float	其中：客户资金存款
client_prov	float	其中：客户备付金
transac_seat_fee	float	其中:交易席位费
invest_as_receiv	float	应收款项类投资
total_assets	float	资产总计
lt_borr	float	长期借款
st_borr	float	短期借款
cb_borr	float	向中央银行借款
depos_ib_deposits	float	吸收存款及同业存放
loan_oth_bank	float	拆入资金
trading_fl	float	交易性金融负债
notes_payable	float	应付票据
acct_payable	float	应付账款
adv_receipts	float	预收款项
sold_for_repur_fa	float	卖出回购金融资产款
comm_payable	float	应付手续费及佣金
payroll_payable	float	应付职工薪酬
taxes_payable	float	应交税费
int_payable	float	应付利息
div_payable	float	应付股利
oth_payable	float	其他应付款
acc_exp	float	预提费用
deferred_inc	float	递延收益
st_bonds_payable	float	应付短期债券
payable_to_reinsurer	float	应付分保账款
rsrv_insur_cont	float	保险合同准备金
acting_trading_sec	float	代理买卖证券款
acting_uw_sec	float	代理承销证券款
non_cur_liab_due_1y	float	一年内到期的非流动负债
oth_cur_liab	float	其他流动负债
total_cur_liab	float	流动负债合计
bond_payable	float	应付债券
lt_payable	float	长期应付款
specific_payables	float	专项应付款
estimated_liab	float	预计负债
defer_tax_liab	float	递延所得税负债
defer_inc_non_cur_liab	float	递延收益-非流动负债
oth_ncl	float	其他非流动负债
total_ncl	float	非流动负债合计
depos_oth_bfi	float	同业和其它金融机构存放款项
deriv_liab	float	衍生金融负债
depos	float	吸收存款
agency_bus_liab	float	代理业务负债
oth_liab	float	其他负债
prem_receiv_adva	float	预收保费
depos_received	float	存入保证金
ph_invest	float	保户储金及投资款
reser_une_prem	float	未到期责任准备金
reser_outstd_claims	float	未决赔款准备金
reser_lins_liab	float	寿险责任准备金
reser_lthins_liab	float	长期健康险责任准备金
indept_acc_liab	float	独立账户负债
pledge_borr	float	其中:质押借款
indem_payable	float	应付赔付款
policy_div_payable	float	应付保单红利
total_liab	float	负债合计
treasury_share	float	减:库存股
ordin_risk_reser	float	一般风险准备
forex_differ	float	外币报表折算差额
invest_loss_unconf	float	未确认的投资损失
minority_int	float	少数股东权益
total_hldr_eqy_exc_min_int	float	股东权益合计(不含少数股东权益)
total_hldr_eqy_inc_min_int	float	股东权益合计(含少数股东权益)
total_liab_hldr_eqy	float	负债及股东权益总计
lt_payroll_payable	float	长期应付职工薪酬
oth_comp_income	float	其他综合收益
oth_eqt_tools	float	其他权益工具
oth_eqt_tools_p_shr	float	其他权益工具(优先股)
lending_funds	float	融出资金
acc_receivable	float	应收款项
st_fin_payable	float	应付短期融资款
payables	float	应付款项
hfs_assets	float	持有待售的资产
hfs_sales	float	持有待售的负债
'''

'''
ts_code	str	TS股票代码
ann_date	str	公告日期
f_ann_date	str	实际公告日期
end_date	str	报告期
comp_type	str	报表类型：见下方详细说明
report_type	str	公司类型：1一般工商业 2银行 3保险 4证券
net_profit	float	净利润
finan_exp	float	财务费用
c_fr_sale_sg	float	销售商品、提供劳务收到的现金
recp_tax_rends	float	收到的税费返还
n_depos_incr_fi	float	客户存款和同业存放款项净增加额
n_incr_loans_cb	float	向中央银行借款净增加额
n_inc_borr_oth_fi	float	向其他金融机构拆入资金净增加额
prem_fr_orig_contr	float	收到原保险合同保费取得的现金
n_incr_insured_dep	float	保户储金净增加额
n_reinsur_prem	float	收到再保业务现金净额
n_incr_disp_tfa	float	处置交易性金融资产净增加额
ifc_cash_incr	float	收取利息和手续费净增加额
n_incr_disp_faas	float	处置可供出售金融资产净增加额
n_incr_loans_oth_bank	float	拆入资金净增加额
n_cap_incr_repur	float	回购业务资金净增加额
c_fr_oth_operate_a	float	收到其他与经营活动有关的现金
c_inf_fr_operate_a	float	经营活动现金流入小计
c_paid_goods_s	float	购买商品、接受劳务支付的现金
c_paid_to_for_empl	float	支付给职工以及为职工支付的现金
c_paid_for_taxes	float	支付的各项税费
n_incr_clt_loan_adv	float	客户贷款及垫款净增加额
n_incr_dep_cbob	float	存放央行和同业款项净增加额
c_pay_claims_orig_inco	float	支付原保险合同赔付款项的现金
pay_handling_chrg	float	支付手续费的现金
pay_comm_insur_plcy	float	支付保单红利的现金
oth_cash_pay_oper_act	float	支付其他与经营活动有关的现金
st_cash_out_act	float	经营活动现金流出小计
n_cashflow_act	float	经营活动产生的现金流量净额
oth_recp_ral_inv_act	float	收到其他与投资活动有关的现金
c_disp_withdrwl_invest	float	收回投资收到的现金
c_recp_return_invest	float	取得投资收益收到的现金
n_recp_disp_fiolta	float	处置固定资产、无形资产和其他长期资产收回的现金净额
n_recp_disp_sobu	float	处置子公司及其他营业单位收到的现金净额
stot_inflows_inv_act	float	投资活动现金流入小计
c_pay_acq_const_fiolta	float	购建固定资产、无形资产和其他长期资产支付的现金
c_paid_invest	float	投资支付的现金
n_disp_subs_oth_biz	float	取得子公司及其他营业单位支付的现金净额
oth_pay_ral_inv_act	float	支付其他与投资活动有关的现金
n_incr_pledge_loan	float	质押贷款净增加额
stot_out_inv_act	float	投资活动现金流出小计
n_cashflow_inv_act	float	投资活动产生的现金流量净额
c_recp_borrow	float	取得借款收到的现金
proc_issue_bonds	float	发行债券收到的现金
oth_cash_recp_ral_fnc_act	float	收到其他与筹资活动有关的现金
stot_cash_in_fnc_act	float	筹资活动现金流入小计
free_cashflow	float	企业自由现金流量
c_prepay_amt_borr	float	偿还债务支付的现金
c_pay_dist_dpcp_int_exp	float	分配股利、利润或偿付利息支付的现金
incl_dvd_profit_paid_sc_ms	float	其中:子公司支付给少数股东的股利、利润
oth_cashpay_ral_fnc_act	float	支付其他与筹资活动有关的现金
stot_cashout_fnc_act	float	筹资活动现金流出小计
n_cash_flows_fnc_act	float	筹资活动产生的现金流量净额
eff_fx_flu_cash	float	汇率变动对现金的影响
n_incr_cash_cash_equ	float	现金及现金等价物净增加额
c_cash_equ_beg_period	float	期初现金及现金等价物余额
c_cash_equ_end_period	float	期末现金及现金等价物余额
c_recp_cap_contrib	float	吸收投资收到的现金
incl_cash_rec_saims	float	其中:子公司吸收少数股东投资收到的现金
uncon_invest_loss	float	未确认投资损失
prov_depr_assets	float	加:资产减值准备
depr_fa_coga_dpba	float	固定资产折旧、油气资产折耗、生产性生物资产折旧
amort_intang_assets	float	无形资产摊销
lt_amort_deferred_exp	float	长期待摊费用摊销
decr_deferred_exp	float	待摊费用减少
incr_acc_exp	float	预提费用增加
loss_disp_fiolta	float	处置固定、无形资产和其他长期资产的损失
loss_scr_fa	float	固定资产报废损失
loss_fv_chg	float	公允价值变动损失
invest_loss	float	投资损失
decr_def_inc_tax_assets	float	递延所得税资产减少
incr_def_inc_tax_liab	float	递延所得税负债增加
decr_inventories	float	存货的减少
decr_oper_payable	float	经营性应收项目的减少
incr_oper_payable	float	经营性应付项目的增加
others	float	其他
im_net_cashflow_oper_act	float	经营活动产生的现金流量净额(间接法)
conv_debt_into_cap	float	债务转为资本
conv_copbonds_due_within_1y	float	一年内到期的可转换公司债券
fa_fnc_leases	float	融资租入固定资产
end_bal_cash	float	现金的期末余额
beg_bal_cash	float	减:现金的期初余额
end_bal_cash_equ	float	加:现金等价物的期末余额
beg_bal_cash_equ	float	减:现金等价物的期初余额
im_n_incr_cash_equ	float	现金及现金等价物净增加额(间接法)
'''
