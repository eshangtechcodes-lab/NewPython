from core.database import DatabaseHelper
db = DatabaseHelper()
# T_PERIODWARNING 列名
cols = db.execute_query("SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='T_PERIODWARNING'")
pw_cols = [c['COLUMN_NAME'] for c in cols]
print("T_PERIODWARNING cols:", pw_cols)

# T_SERVERPART VALID/STATE 列名
cols2 = db.execute_query("SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='T_SERVERPART'")
sp_cols = [c['COLUMN_NAME'] for c in cols2]
state_cols = [c for c in sp_cols if 'VALID' in c or 'STATE' in c or 'ISVALID' in c.upper()]
print("T_SERVERPART STATE/VALID cols:", state_cols)
