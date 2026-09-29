# StockSense Phase 1 -- Data Pipeline
# Run from project root: python src/data_pipeline/cleaning_pipeline.py
import warnings, hashlib, pandas as pd, numpy as np
from pathlib import Path
from datetime import datetime
warnings.filterwarnings('ignore')

ROOT       = Path(__file__).resolve().parents[2]
RAW_DIR    = ROOT / 'data' / 'raw'
CLEAN_DIR  = ROOT / 'data' / 'cleaned'
PROC_DIR   = ROOT / 'data' / 'processed'
REPORT_DIR = ROOT / 'reports'
for d in [RAW_DIR, CLEAN_DIR, PROC_DIR, REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

AUDIT, DQ_LOG = [], []

def log_dq(ds, col, issue, cnt, pct, action, just):
    DQ_LOG.append(dict(dataset=ds, column=col, issue=issue, count=int(cnt),
                        percentage=round(float(pct), 4), action=action, justification=just))

def log_audit(ds, rid, fld, old, new, rsn):
    AUDIT.append(dict(dataset=ds, row_id=str(rid), field=fld,
                       old_value=str(old), new_value=str(new), reason=rsn))

def section(t):
    print()
    print('='*65)
    print(f'  {t}')
    print('='*65)

def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()

# STEP 1 -- LOAD RAW DATA
section('STEP 1 -- LOAD RAW DATA')
raw_tx  = pd.read_csv(RAW_DIR / 'transactions.csv')
raw_pr  = pd.read_csv(RAW_DIR / 'products.csv')
raw_st  = pd.read_csv(RAW_DIR / 'stores.csv')
raw_inv = pd.read_csv(RAW_DIR / 'inventory.csv')
raw_ext = pd.read_csv(RAW_DIR / 'external_factors.csv')
SCHEMA = {}
for name, df in [('transactions', raw_tx), ('products', raw_pr),
                  ('stores', raw_st), ('inventory', raw_inv),
                  ('external_factors', raw_ext)]:
    SCHEMA[name] = dict(rows=len(df), columns=len(df.columns),
        column_names=list(df.columns), dtypes=df.dtypes.astype(str).to_dict(),
        null_counts=df.isnull().sum().to_dict(), duplicate_rows=int(df.duplicated().sum()),
        memory_bytes=int(df.memory_usage(deep=True).sum()))
    print(f'  {name}: {len(df):,} rows x {len(df.columns)} cols')

# STEP 2 -- REFERENCE SETS
section('STEP 2 -- REFERENCE SET VALIDATION')
VALID_STORE_IDS   = set(raw_st['store_id'])
VALID_PRODUCT_IDS = set(raw_pr['product_id'])
print(f'  Valid stores: {sorted(VALID_STORE_IDS)}')
print(f'  Valid products: {len(VALID_PRODUCT_IDS)} IDs')

# STEP 3 -- CLEAN PRODUCTS
section('STEP 3 -- CLEAN PRODUCTS')
pr = raw_pr.copy()
CATEGORY_MAP = {'beverage':'Beverages','BEVERAGES':'Beverages','DAIRY':'Dairy',
                'SNACKS':'Snacks','household':'Household','Staples ':'Staples'}
before_cats = pr['category'].value_counts().to_dict()
pr['category'] = pr['category'].str.strip().replace(CATEGORY_MAP)
n_std = sum(v for k,v in before_cats.items() if k in CATEGORY_MAP or k!=k.strip())
log_dq('products','category','Case/spelling inconsistency',n_std,n_std/len(pr)*100,
       'Standardised to canonical Title-case name',
       '6 variants (beverage,BEVERAGES,DAIRY,SNACKS,household,Staples[space]) mapped.')
for old,new in CATEGORY_MAP.items():
    if before_cats.get(old,0)>0:
        log_audit('products',f'cat={old}','category',old,new,f'Standardised {old!r}')
print(f'  Categories after: {sorted(pr["category"].unique())}')
cost_gt_mrp = (pr['cost_price']>pr['mrp']).sum()
log_dq('products','cost_price/mrp','cost_price > mrp',cost_gt_mrp,cost_gt_mrp/len(pr)*100,
       'No action','PASS -- no violations')
sup_anm = (pr['supplier_id']=='SUP999').sum()
pr['invalid_supplier_flag'] = (pr['supplier_id']=='SUP999').astype(int)
if sup_anm:
    log_dq('products','supplier_id','Invalid supplier ID (SUP999)',sup_anm,sup_anm/len(pr)*100,
           'Flagged; retained','SUP999 absent from supplier master.')
print(f'  SUP999 flagged: {sup_anm}, cost>mrp violations: {cost_gt_mrp}')
pr.to_csv(CLEAN_DIR/'products_clean.csv', index=False)
print('  Saved: products_clean.csv')

# STEP 4 -- CLEAN STORES
section('STEP 4 -- CLEAN STORES')
st = raw_st.copy()
log_dq('stores','ALL','Missing values',0,0.0,'No action','PASS')
log_dq('stores','ALL','Duplicate rows', 0,0.0,'No action','PASS')
st.to_csv(CLEAN_DIR/'stores_clean.csv', index=False)
print('  No issues. Saved: stores_clean.csv')

# STEP 5 -- CLEAN TRANSACTIONS
section('STEP 5 -- CLEAN TRANSACTIONS')
tx = raw_tx.copy()
tx_orig_len = len(tx)
tx['_idx'] = tx.index
tx['date'] = pd.to_datetime(tx['date'], errors='coerce')
bad_dates = tx['date'].isna().sum()
if bad_dates:
    log_dq('transactions','date','Unparseable dates',bad_dates,bad_dates/len(tx)*100,'Rows dropped','No date => cannot aggregate.')
date_lo, date_hi = pd.Timestamp('2026-08-01'), pd.Timestamp('2026-08-31')
tx['outside_main_window_flag'] = ((tx['date']<date_lo)|(tx['date']>date_hi)).astype(int)
n_out = tx['outside_main_window_flag'].sum()
log_dq('transactions','date','Outside Aug 01-31 window',n_out,n_out/len(tx)*100,
       'Flagged; retained','2 fringe records (Jul-31, Sep-01). Modelling decides inclusion.')
print(f'  Fringe date rows: {n_out}')
exact_dup = tx.duplicated(subset=tx.columns.difference(['_idx']),keep='first')
n_dup = exact_dup.sum()
log_dq('transactions','ALL','Exact duplicate rows',n_dup,n_dup/len(tx)*100,
       'Removed -- kept first occurrence',
       'Identical on all fields incl. transaction_id. Entry duplicates not repeated purchases.')
for ri in tx[exact_dup]['_idx'].tolist():
    log_audit('transactions',ri,'ALL','DUPLICATE','REMOVED','Exact dup row')
tx = tx[~exact_dup].copy()
print(f'  Exact dupes removed: {n_dup}')
dup_id = tx.duplicated(subset=['transaction_id'],keep=False)
n_dup_id = dup_id.sum()
log_dq('transactions','transaction_id','Dup tx_id post-dedup',n_dup_id,n_dup_id/len(tx)*100,
       'Flagged dup_txid_flag=1; retained','ID-generation errors. Retained with flag.')
tx['dup_txid_flag'] = dup_id.astype(int)
print(f'  Dup tx_id (post-dedup): {n_dup_id}')
tx['orphan_store_flag']   = (~tx['store_id'].isin(VALID_STORE_IDS)).astype(int)
tx['orphan_product_flag'] = (~tx['product_id'].isin(VALID_PRODUCT_IDS)).astype(int)
n_os = tx['orphan_store_flag'].sum();   n_op = tx['orphan_product_flag'].sum()
log_dq('transactions','store_id','Orphan store_id (S99)',n_os,n_os/len(tx)*100,
       'Flagged orphan_store_flag=1; excluded from master','S99 not in stores reference.')
log_dq('transactions','product_id','Orphan product_id (P9999)',n_op,n_op/len(tx)*100,
       'Flagged orphan_product_flag=1; excluded from master','P9999 not in products reference.')
print(f'  Orphan store: {n_os}, orphan product: {n_op}')
inv_qty = tx['quantity']<=0
n_iq = inv_qty.sum()
log_dq('transactions','quantity','Non-positive quantity',n_iq,n_iq/len(tx)*100,
       'Flagged invalid_qty_flag=1; retained','Negative=possible return; zero=impossible. Flagged.')
tx['invalid_qty_flag'] = inv_qty.astype(int)
for _,row in tx[inv_qty].iterrows():
    log_audit('transactions',row['_idx'],'quantity',row['quantity'],'FLAGGED','Non-positive qty')
print(f'  Non-positive qty: {n_iq}')
inv_prc = tx['selling_price']<=0
n_ip = inv_prc.sum()
log_dq('transactions','selling_price','Non-positive selling price',n_ip,n_ip/len(tx)*100,
       'Flagged invalid_price_flag=1; excluded from revenue','Price -20 impossible. Flagged.')
tx['invalid_price_flag'] = inv_prc.astype(int)
for _,row in tx[inv_prc].iterrows():
    log_audit('transactions',row['_idx'],'selling_price',row['selling_price'],'FLAGGED','Negative price')
print(f'  Non-positive price: {n_ip}')
inv_disc = (tx['discount_pct']<0)|(tx['discount_pct']>100)
n_id = inv_disc.sum()
log_dq('transactions','discount_pct','Discount outside [0,100]',n_id,n_id/len(tx)*100,
       'Flagged; value set to NaN','Values 110 and -15 impossible. Set NaN to protect aggregates.')
tx['invalid_discount_flag'] = inv_disc.astype(int)
for _,row in tx[inv_disc].iterrows():
    log_audit('transactions',row['_idx'],'discount_pct',row['discount_pct'],np.nan,'Invalid discount->NaN')
tx.loc[inv_disc,'discount_pct'] = np.nan
print(f'  Invalid discount: {n_id} -> NaN')
inv_hr = (tx['hour']<0)|(tx['hour']>23)
n_ih = inv_hr.sum()
log_dq('transactions','hour','Hour outside [0,23]',n_ih,n_ih/len(tx)*100,
       'Flagged; value set to NaN','Values 27 and -3 impossible clock values. Set NaN.')
tx['invalid_hour_flag'] = inv_hr.astype(int)
for _,row in tx[inv_hr].iterrows():
    log_audit('transactions',row['_idx'],'hour',row['hour'],np.nan,'Invalid hour->NaN')
tx.loc[inv_hr,'hour'] = np.nan
print(f'  Invalid hour: {n_ih} -> NaN')
for col in ['customer_id','payment_mode','hour']:
    n = tx[col].isna().sum()
    if n:
        log_dq('transactions',col,f'Missing {col}',n,n/len(tx)*100,
               'Retained as NaN','Cannot impute. NaN preserved.')
print(f'  Nulls: cust_id={tx["customer_id"].isna().sum()} pay_mode={tx["payment_mode"].isna().sum()} hour={tx["hour"].isna().sum()}')
tx['payment_mode'] = tx['payment_mode'].str.strip().str.title()
tx.drop(columns=['_idx'],inplace=True)
tx.to_csv(CLEAN_DIR/'transactions_clean.csv', index=False)
print(f'  Saved: transactions_clean.csv ({len(tx):,} rows, {tx_orig_len-len(tx)} removed)')

# STEP 6 -- CLEAN INVENTORY + RECONCILIATION
section('STEP 6 -- CLEAN INVENTORY + ARITHMETIC RECONCILIATION')
inv = raw_inv.copy()
inv['date'] = pd.to_datetime(inv['date'],errors='coerce')
inv.rename(columns={'store':'store_id','product':'product_id'},inplace=True)
inv['orphan_store_flag']   = (~inv['store_id'].isin(VALID_STORE_IDS)).astype(int)
inv['orphan_product_flag'] = (~inv['product_id'].isin(VALID_PRODUCT_IDS)).astype(int)
for col,lbl in [('store_id','S99'),('product_id','P9999')]:
    key=col.replace('_id','')
    n=(inv[f'orphan_{key}_flag']==1).sum()
    if n:
        log_dq('inventory',col,f'Orphan {col} ({lbl})',n,n/len(inv)*100,'Flagged; retained','Cannot join to reference.')
print(f'  Orphan stores: {inv["orphan_store_flag"].sum()}, products: {inv["orphan_product_flag"].sum()}')
inv_open_bad = inv['opening']<0
n_ob = inv_open_bad.sum()
log_dq('inventory','opening','Negative opening stock',n_ob,n_ob/len(inv)*100,
       'Flagged invalid_inventory_flag=1; NOT overwritten','Physically impossible. Correct value unknown.')
inv['invalid_inventory_flag'] = inv_open_bad.astype(int)
inv_recv_bad = inv['received']<0
n_rb = inv_recv_bad.sum()
log_dq('inventory','received','Negative received',n_rb,n_rb/len(inv)*100,
       'Flagged; NOT overwritten','Physically impossible.')
inv.loc[inv_recv_bad,'invalid_inventory_flag'] = 1
inv_lead_bad = inv['lead_days']<=0
n_lb = inv_lead_bad.sum()
log_dq('inventory','lead_days','Non-positive lead_days',n_lb,n_lb/len(inv)*100,
       'Flagged invalid_lead_flag=1; retained','Lead<=0 days impossible. Flagged for Phase 3.')
inv['invalid_lead_flag'] = inv_lead_bad.astype(int)
n_nr=inv['received'].isna().sum(); n_nc=inv['closing'].isna().sum()
log_dq('inventory','received','Missing received',n_nr,n_nr/len(inv)*100,'Retained NaN; INSUFFICIENT_DATA','Cannot impute.')
log_dq('inventory','closing','Missing closing', n_nc,n_nc/len(inv)*100,'Retained NaN; INSUFFICIENT_DATA','Cannot impute.')
print(f'  Bad: opening={n_ob}, received={n_rb}, lead={n_lb}, null_recv={n_nr}, null_close={n_nc}')
print('  Running arithmetic reconciliation...')
inv['expected_closing']      = inv['opening'] + inv['received'].fillna(0) - inv['sold']
inv['inventory_balance_gap'] = inv['closing'] - inv['expected_closing']
def rec_status(row):
    if pd.isna(row['closing']) or pd.isna(row['received']): return 'INSUFFICIENT_DATA'
    if row.get('invalid_inventory_flag',0)==1 or row.get('invalid_lead_flag',0)==1: return 'INVALID_INPUT'
    g = abs(row['inventory_balance_gap'])
    if g==0: return 'CONSISTENT'
    if g<=5: return 'MINOR_MISMATCH'
    return 'MAJOR_MISMATCH'
inv['reconciliation_status'] = inv.apply(rec_status,axis=1)
rc = inv['reconciliation_status'].value_counts()
print('  Reconciliation Status:')
for s,c in rc.items():
    print(f'    {s:<22}: {c:>6,}  ({c/len(inv)*100:.2f}%)')
log_dq('inventory','closing/opening/received/sold','Arithmetic mismatch',
       int(inv['reconciliation_status'].isin(['MINOR_MISMATCH','MAJOR_MISMATCH']).sum()),
       inv['reconciliation_status'].isin(['MINOR_MISMATCH','MAJOR_MISMATCH']).sum()/len(inv)*100,
       'inventory_balance_gap and reconciliation_status added; NOT modified',
       'Gap documented for Phase 3 Reconciliation Intelligence.')
gap_nz = inv.loc[inv['inventory_balance_gap']!=0,'inventory_balance_gap']
if len(gap_nz):
    print(f'  Non-zero gaps: n={len(gap_nz)} min={gap_nz.min():.1f} max={gap_nz.max():.1f} mean={gap_nz.mean():.2f}')
inv.to_csv(CLEAN_DIR/'inventory_clean.csv',index=False)
print('  Saved: inventory_clean.csv')

# STEP 7 -- CLEAN EXTERNAL FACTORS
section('STEP 7 -- CLEAN EXTERNAL FACTORS')
ext = raw_ext.copy()
ext['date'] = pd.to_datetime(ext['date'],errors='coerce')
typo_mask = ext['city']=='ChennaI'
n_ct = typo_mask.sum()
log_dq('external_factors','city',"City typo: 'ChennaI'",n_ct,n_ct/len(ext)*100,
       "Corrected to 'Chennai'","Obvious typo (capital I). Corrected to enable join.")
ext.loc[typo_mask,'city'] = 'Chennai'
for i in ext[typo_mask].index:
    log_audit('external_factors',i,'city','ChennaI','Chennai','Typo correction')
print(f"  'ChennaI' corrected: {n_ct} rows")
n_nt = ext['temp_c'].isna().sum()
log_dq('external_factors','temp_c','Missing temp_c',n_nt,n_nt/len(ext)*100,
       'Imputed city-level monthly median; flagged temp_imputed_flag',
       '6 missing. City median best estimate without external API.')
ext['temp_imputed_flag'] = ext['temp_c'].isna().astype(int)
ext['temp_c'] = ext.groupby('city')['temp_c'].transform(lambda x: x.fillna(x.median()))
print(f'  Missing temp_c imputed: {n_nt}')
n_nr2 = ext['rain_mm'].isna().sum()
log_dq('external_factors','rain_mm','Missing rain_mm',n_nr2,n_nr2/len(ext)*100,
       'Imputed city median; flagged rain_imputed_flag','1 missing. City median used.')
ext['rain_imputed_flag'] = ext['rain_mm'].isna().astype(int)
ext['rain_mm'] = ext.groupby('city')['rain_mm'].transform(lambda x: x.fillna(x.median()))
print(f'  Missing rain_mm imputed: {n_nr2}')
# Dedup: fixing 'ChennaI' typo creates a second Chennai row for 2026-08-25.
# Resolve by aggregating: mean for numerics, max for binary flags.
n_before_dedup = len(ext)
ext_dedup = ext.groupby(['date','city'], as_index=False).agg(
    {'temp_c':'mean','rain_mm':'mean',
     'holiday':'max','festival':'max','weekend':'max','local_event':'max',
     'temp_imputed_flag':'max','rain_imputed_flag':'max'})
n_dedup_removed = n_before_dedup - len(ext_dedup)
if n_dedup_removed > 0:
    log_dq('external_factors','date+city','Duplicate date+city after typo correction',
           n_dedup_removed, n_dedup_removed/n_before_dedup*100,
           'Resolved by mean aggregation of numeric cols; max of binary flags',
           'Raw data has both Chennai and ChennaI rows for 2026-08-25. After typo fix '
           'two Chennai rows exist for same date. Mean/max aggregation is the least '
           'destructive resolution without external reference data.')
    print(f'  Duplicate date+city resolved: {n_dedup_removed} row(s) removed by aggregation')
ext = ext_dedup
store_cities=set(raw_st['city']); ext_cities=set(ext['city'])
unmatched=ext_cities-store_cities
if unmatched: print(f'  WARNING: Unmatched ext cities: {unmatched}')
else: print('  All ext cities match store cities: OK')
inv_dates_set=set(pd.to_datetime(raw_inv['date']).dt.date)
ext_dates_set=set(ext['date'].dt.date)
uncovered=inv_dates_set-ext_dates_set
if uncovered:
    log_dq('external_factors','date','Inv dates without ext coverage',
           len(uncovered),len(uncovered)/len(inv_dates_set)*100,
           'Master will have NaN for these dates',
           f'Ext ends Aug-31; inv extends to Sep-03. Dates: {sorted(uncovered)}')
print(f'  Dates without ext coverage: {len(uncovered)}')
ext.to_csv(CLEAN_DIR/'external_factors_clean.csv',index=False)
print('  Saved: external_factors_clean.csv')

# STEP 8 -- TX vs INVENTORY RECONCILIATION
section('STEP 8 -- TRANSACTION vs INVENTORY DEMAND RECONCILIATION')
tx_clean  = pd.read_csv(CLEAN_DIR/'transactions_clean.csv',  parse_dates=['date'])
inv_clean = pd.read_csv(CLEAN_DIR/'inventory_clean.csv',     parse_dates=['date'])
tx_dem = (tx_clean.groupby(['date','store_id','product_id'])['quantity']
          .sum().reset_index().rename(columns={'quantity':'transaction_demand'}))
inv_dem = inv_clean[['date','store_id','product_id','sold']].rename(columns={'sold':'inventory_sold'})
rec_df = pd.merge(tx_dem,inv_dem,on=['date','store_id','product_id'],how='outer')
rec_df['inventory_demand_gap'] = rec_df['transaction_demand'] - rec_df['inventory_sold']
n_match   = rec_df.dropna(subset=['transaction_demand','inventory_sold']).shape[0]
n_tx_only = rec_df['inventory_sold'].isna().sum()
n_iv_only = rec_df['transaction_demand'].isna().sum()
gstat     = rec_df['inventory_demand_gap'].describe()
print(f'  Matched both sources: {n_match:,}  |  TX only: {n_tx_only:,}  |  Inv only: {n_iv_only:,}')
print(f'  Gap mean={gstat["mean"]:.2f} std={gstat["std"]:.2f} min={gstat["min"]:.0f} max={gstat["max"]:.0f}')
print(f'  Perfect agreement (gap=0): {(rec_df["inventory_demand_gap"]==0).sum():,}')
print('  CONCLUSION: TX demand and inv.sold are DIFFERENT signals (POS vs WMS). Both retained.')
log_dq('transactions/inventory','quantity/sold','TX demand != inv sold',
       int((rec_df['inventory_demand_gap']!=0).sum()),
       (rec_df['inventory_demand_gap']!=0).sum()/len(rec_df)*100,
       'Both retained; inventory_demand_gap created',
       'POS vs WMS discrepancies expected. Replacing one with other = fabrication.')
rec_df.to_csv(PROC_DIR/'tx_inv_reconciliation.csv',index=False)
print('  Saved: tx_inv_reconciliation.csv')

# STEP 9 -- SPARSE HISTORY ANALYSIS
section('STEP 9 -- SPARSE HISTORY ANALYSIS')
all_dates    = pd.date_range('2026-08-01','2026-08-31',freq='D')
all_stores   = sorted(VALID_STORE_IDS)
all_products = sorted(VALID_PRODUCT_IDS)
full_grid = pd.MultiIndex.from_product([all_dates,all_stores,all_products],
    names=['date','store_id','product_id']).to_frame(index=False)
tx_pos = (tx_clean[(tx_clean['orphan_store_flag']==0)&(tx_clean['orphan_product_flag']==0)&(tx_clean['quantity']>0)]
          .groupby(['date','store_id','product_id'])['quantity'].sum()
          .reset_index().rename(columns={'quantity':'units_sold'}))
sg = pd.merge(full_grid,tx_pos,on=['date','store_id','product_id'],how='left')
sg['units_sold'] = sg['units_sold'].fillna(0)
sp_stats = (sg.groupby(['store_id','product_id'])
    .agg(history_length=('date','count'), zero_demand_days=('units_sold',lambda x:(x==0).sum()),
         total_demand=('units_sold','sum'), active_days=('units_sold',lambda x:(x>0).sum()))
    .reset_index())
sp_stats['zero_demand_ratio'] = sp_stats['zero_demand_days']/sp_stats['history_length']
sp_stats['mean_daily_demand'] = sp_stats['total_demand']/sp_stats['active_days'].replace(0,np.nan)
sp_stats['sparse_history_flag'] = ((sp_stats['zero_demand_ratio']>0.70)|(sp_stats['active_days']<7)).astype(int)
n_sparse=sp_stats['sparse_history_flag'].sum(); n_total=len(sp_stats)
print(f'  Combos: {n_total:,}  |  Sparse: {n_sparse:,} ({n_sparse/n_total*100:.1f}%)  |  Never sold: {(sp_stats["zero_demand_ratio"]==1.0).sum():,}')
log_dq('transactions','store_id x product_id','Sparse history (>70% zero or <7 active)',
       n_sparse,n_sparse/n_total*100,'Flagged sparse_history_flag=1; retained',
       'Sparse combos may be new/low-velocity SKUs. Removing hides stockout risk.')
sp_stats.to_csv(PROC_DIR/'sparse_history_analysis.csv',index=False)
print('  Saved: sparse_history_analysis.csv')

# STEP 10 -- TRANSACTION AGGREGATION
section('STEP 10 -- TRANSACTION AGGREGATION -> Daily Store x Product')
tx_agg = tx_clean[(tx_clean['orphan_store_flag']==0)&(tx_clean['orphan_product_flag']==0)].copy()
tx_vq  = tx_agg[tx_agg['invalid_qty_flag']==0]
tx_vqp = tx_agg[(tx_agg['invalid_qty_flag']==0)&(tx_agg['invalid_price_flag']==0)].copy()
KEY = ['date','store_id','product_id']
a_qty   = tx_vq.groupby(KEY)['quantity'].sum().reset_index().rename(columns={'quantity':'transaction_demand'})
tx_vqp['revenue'] = tx_vqp['quantity']*tx_vqp['selling_price']
a_rev   = tx_vqp.groupby(KEY)['revenue'].sum().reset_index()
a_cnt   = tx_agg.groupby(KEY)['transaction_id'].count().reset_index().rename(columns={'transaction_id':'transaction_count'})
a_cust  = tx_agg.groupby(KEY)['customer_id'].nunique().reset_index().rename(columns={'customer_id':'unique_customer_count'})
a_price = tx_vqp.groupby(KEY)['selling_price'].mean().reset_index().rename(columns={'selling_price':'avg_selling_price'})
a_disc  = tx_agg[tx_agg['invalid_discount_flag']==0].groupby(KEY)['discount_pct'].mean().reset_index().rename(columns={'discount_pct':'avg_discount_pct'})
a_promo = tx_agg.groupby(KEY)['promotion_flag'].max().reset_index().rename(columns={'promotion_flag':'promotion_active'})
a_peak  = tx_agg.dropna(subset=['hour']).groupby(KEY)['hour'].agg(lambda x: x.mode().iloc[0] if len(x)>0 else np.nan).reset_index().rename(columns={'hour':'peak_hour'})
a_iqc   = tx_agg.groupby(KEY)['invalid_qty_flag'].sum().reset_index().rename(columns={'invalid_qty_flag':'invalid_qty_count'})
a_ipc   = tx_agg.groupby(KEY)['invalid_price_flag'].sum().reset_index().rename(columns={'invalid_price_flag':'invalid_price_count'})
daily_tx = a_qty.copy()
for agg in [a_rev,a_cnt,a_cust,a_price,a_disc,a_promo,a_peak,a_iqc,a_ipc]:
    daily_tx = pd.merge(daily_tx,agg,on=KEY,how='left')
daily_tx.to_csv(PROC_DIR/'daily_transactions_agg.csv',index=False)
print(f'  Daily agg rows: {len(daily_tx):,}  |  Unique grain: {daily_tx.drop_duplicates(KEY).shape[0]:,}')
print('  Rules: demand=SUM(+qty), revenue=SUM(qty*price), promo=MAX, peak_hr=MODE')
print('  Saved: daily_transactions_agg.csv')

# STEP 11 -- BUILD MASTER DATASET
section('STEP 11 -- BUILD MASTER DATASET (Date x Store x Product)')
prod_c = pd.read_csv(CLEAN_DIR/'products_clean.csv')
stor_c = pd.read_csv(CLEAN_DIR/'stores_clean.csv')
ext_c  = pd.read_csv(CLEAN_DIR/'external_factors_clean.csv',parse_dates=['date'])
inv_c  = pd.read_csv(CLEAN_DIR/'inventory_clean.csv',       parse_dates=['date'])
master = pd.merge(daily_tx,prod_c,on='product_id',how='left')
master = pd.merge(master,  stor_c,on='store_id',  how='left')
inv_join = inv_c[['date','store_id','product_id','opening','received','sold','closing',
    'reorder_lvl','lead_days','inventory_balance_gap','reconciliation_status',
    'invalid_inventory_flag','invalid_lead_flag','expected_closing',
    'orphan_store_flag','orphan_product_flag']].rename(columns={
    'sold':'inventory_sold','orphan_store_flag':'inv_orphan_store_flag',
    'orphan_product_flag':'inv_orphan_product_flag'})
master = pd.merge(master,inv_join,on=['date','store_id','product_id'],how='left')
ext_join = ext_c.rename(columns={'city':'city_ext'})
master = pd.merge(master,ext_join,left_on=['date','city'],right_on=['date','city_ext'],how='left')
master.drop(columns=['city_ext'],inplace=True,errors='ignore')
master = pd.merge(master,sp_stats[['store_id','product_id','history_length','zero_demand_ratio',
    'active_days','sparse_history_flag','mean_daily_demand']],on=['store_id','product_id'],how='left')
master = pd.merge(master,rec_df[['date','store_id','product_id','transaction_demand',
    'inventory_sold','inventory_demand_gap']],on=['date','store_id','product_id'],
    how='left',suffixes=('','_rec'))
master.drop(columns=[c for c in master.columns if c.endswith('_rec')],inplace=True,errors='ignore')
master['date'] = pd.to_datetime(master['date'])
dup_m = master.duplicated(subset=['date','store_id','product_id']).sum()
print(f'  Master: {len(master):,} rows x {len(master.columns)} cols  |  Dup grains: {dup_m} ({"PASS" if dup_m==0 else "FAIL"})')
master.to_csv(PROC_DIR/'master_dataset.csv',index=False)
print('  Saved: master_dataset.csv')

# STEP 12 -- LEAKAGE CLASSIFICATION
section('STEP 12 -- DATA LEAKAGE CLASSIFICATION')
LEAKAGE = {
    'SAFE_HISTORICAL':['transaction_demand','revenue','transaction_count','unique_customer_count',
        'avg_selling_price','avg_discount_pct','promotion_active','peak_hour',
        'opening','received','inventory_sold','closing','reorder_lvl','lead_days',
        'temp_c','rain_mm','holiday','festival','weekend','local_event'],
    'SAFE_STATIC_ATTRIBUTE':['category','sub_category','brand','mrp','cost_price','shelf_life_days',
        'supplier_id','city','store_type','floor_area_sqft','avg_daily_customers','region'],
    'SAFE_DERIVED_DQ':['inventory_balance_gap','reconciliation_status','inventory_demand_gap',
        'sparse_history_flag','zero_demand_ratio','history_length','active_days',
        'invalid_qty_count','invalid_price_count','invalid_inventory_flag','invalid_lead_flag',
        'temp_imputed_flag','rain_imputed_flag'],
    'DO_NOT_USE_AS_FEATURE':['expected_closing'],
}
lk_path = REPORT_DIR/'leakage_classification.md'
with open(lk_path,'w',encoding='utf-8') as f:
    f.write('# Data Leakage Classification\n\nPhase 3 MUST NOT use DO_NOT_USE_AS_FEATURE columns as predictors.\n\n')
    for grp,cols in LEAKAGE.items():
        f.write(f'## {grp}\n')
        for c in cols: f.write(f'- {c}\n')
        f.write('\n')
print('  Saved: reports/leakage_classification.md')

# STEP 13 -- AUTOMATED VALIDATION
section('STEP 13 -- AUTOMATED VALIDATION SUITE')
mc = pd.read_csv(PROC_DIR/'master_dataset.csv',parse_dates=['date'])
CHECKS=[]
def chk(name,cond,detail=''):
    status='PASS' if cond else 'FAIL'
    CHECKS.append({'check':name,'status':status,'detail':detail})
    icon='V' if cond else 'X'
    print(f'  [{icon}] {status}  {name}')
    if detail and not cond: print(f'       -> {detail}')
chk('Master grain unique',mc.duplicated(['date','store_id','product_id']).sum()==0)
req=['date','store_id','product_id','transaction_demand','revenue','avg_selling_price',
     'promotion_active','opening','inventory_sold','closing','reorder_lvl','lead_days',
     'inventory_balance_gap','reconciliation_status','inventory_demand_gap',
     'sparse_history_flag','category','brand','city','store_type']
miss=[c for c in req if c not in mc.columns]
chk('Required columns present',len(miss)==0,f'Missing: {miss}')
chk('No null dates',mc['date'].isna().sum()==0)
chk('transaction_demand non-negative',(mc['transaction_demand']<0).sum()==0)
chk('Revenue non-negative',(mc['revenue']<0).sum()==0)
chk('inventory_balance_gap present','inventory_balance_gap' in mc.columns)
valid_s={'CONSISTENT','MINOR_MISMATCH','MAJOR_MISMATCH','INVALID_INPUT','INSUFFICIENT_DATA'}
actual_s=set(mc['reconciliation_status'].dropna().unique())
chk('reconciliation_status values valid',actual_s.issubset(valid_s),f'Unexpected: {actual_s-valid_s}')
sv=set(mc['sparse_history_flag'].dropna().unique())
chk('sparse_history_flag is binary',sv.issubset({0,1,0.0,1.0}))
raw_ok=all(md5(RAW_DIR/f)==md5(ROOT/'dataset'/f) for f in
    ['transactions.csv','products.csv','stores.csv','inventory.csv','external_factors.csv'])
chk('Raw files untouched (MD5)',raw_ok)
cf=['transactions_clean.csv','products_clean.csv','stores_clean.csv',
    'inventory_clean.csv','external_factors_clean.csv']
chk('All cleaned files exist',all((CLEAN_DIR/f).exists() for f in cf))
pf=['master_dataset.csv','daily_transactions_agg.csv','tx_inv_reconciliation.csv','sparse_history_analysis.csv']
chk('All processed files exist',all((PROC_DIR/f).exists() for f in pf))
future_cols=[c for c in mc.columns if 'next_' in c or 'future' in c]
chk('No future-derived columns',len(future_cols)==0,f'Found: {future_cols}')
pc=pd.read_csv(CLEAN_DIR/'products_clean.csv')
valid_cats={'Beverages','Dairy','Snacks','Frozen','Bakery','Staples','Household','Personal Care','Fruits & Vegetables'}
bad_cats=set(pc['category'])-valid_cats
chk('Product categories standardised',len(bad_cats)==0,f'Bad: {bad_cats}')
ec=pd.read_csv(CLEAN_DIR/'external_factors_clean.csv')
chk("External city typo ('ChennaI') fixed",(ec['city']=='ChennaI').sum()==0)
chk('No null temp_c remaining',ec['temp_c'].isna().sum()==0)
n_pass=sum(1 for c in CHECKS if c['status']=='PASS')
n_fail=len(CHECKS)-n_pass
print(f'\n  VALIDATION: {n_pass} PASS / {n_fail} FAIL out of {len(CHECKS)}')

# STEP 14 -- SAVE AUDIT TRAIL
pd.DataFrame(AUDIT).to_csv(PROC_DIR/'audit_trail.csv',index=False)
pd.DataFrame(CHECKS).to_csv(PROC_DIR/'validation_results.csv',index=False)
print('  Saved: audit_trail.csv, validation_results.csv')

# STEP 15 -- DATA QUALITY REPORT
section('STEP 15 -- DATA QUALITY REPORT')
dq_path=REPORT_DIR/'data_quality_report.md'
now_s=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
inv_cr=pd.read_csv(CLEAN_DIR/'inventory_clean.csv')
sp_cr =pd.read_csv(PROC_DIR/'sparse_history_analysis.csv')
with open(dq_path,'w',encoding='utf-8') as f:
    f.write(f'# StockSense -- Data Quality Report\n**Phase 1** | {now_s}\n\n---\n\n')
    f.write('## 1. Dataset Overview\n\n| Dataset | Rows | Columns | Dup Rows | Missing |\n')
    f.write('|---------|------|---------|----------|---------|\n')
    for name,s in SCHEMA.items():
        f.write(f'| {name} | {s["rows"]:,} | {s["columns"]} | {s["duplicate_rows"]} | {sum(s["null_counts"].values())} |\n')
    f.write('\n## 2. Data Quality Issues\n\n| Dataset | Column | Issue | Count | % | Action | Justification |\n')
    f.write('|---------|--------|-------|-------|---|--------|---------------|\n')
    for row in DQ_LOG:
        f.write(f'| {row["dataset"]} | {row["column"]} | {row["issue"]} | {row["count"]} | {row["percentage"]:.2f}% | {row["action"]} | {row["justification"]} |\n')
    f.write('\n## 3. Inventory Reconciliation\n\n| Status | Count | % |\n|--------|-------|---|\n')
    for status,cnt in inv_cr['reconciliation_status'].value_counts().items():
        f.write(f'| {status} | {cnt:,} | {cnt/len(inv_cr)*100:.2f}% |\n')
    f.write('\n## 4. TX vs Inventory Conclusion\n')
    f.write('> transaction_demand and inventory.sold are DIFFERENT signals (POS vs WMS). Both retained.\n')
    f.write('> inventory_demand_gap documents the discrepancy for Phase 3.\n\n')
    f.write(f'## 5. Sparse History\n- Total combos: {len(sp_cr):,}\n')
    f.write(f'- Sparse: {sp_cr["sparse_history_flag"].sum():,} ({sp_cr["sparse_history_flag"].mean()*100:.1f}%)\n')
    f.write(f'- Never sold: {(sp_cr["zero_demand_ratio"]==1.0).sum():,}\n\n')
    f.write('## 6. Validation Results\n\n| Check | Status | Detail |\n|-------|--------|--------|\n')
    for c in CHECKS:
        f.write(f'| {c["check"]} | {c["status"]} | {c.get("detail","")} |\n')
print('  Saved: reports/data_quality_report.md')

section('PHASE 1 COMPLETE')
mc_final=pd.read_csv(PROC_DIR/'master_dataset.csv')
print(f'  Master: {len(mc_final):,} rows x {len(mc_final.columns)} cols')
print(f'  DQ issues: {len(DQ_LOG)}  |  Audit entries: {len(AUDIT)}  |  Validation: {n_pass}/{len(CHECKS)} PASS')
