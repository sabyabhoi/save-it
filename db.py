import duckdb
import utils


def get_db(filename):
    con = duckdb.connect(filename)

    con.sql('''CREATE TABLE IF NOT EXISTS CASH_INFLOW(
    IID INTEGER PRIMARY KEY,
    CATEGORY VARCHAR(50) NOT NULL
    )''')
    con.sql('CREATE SEQUENCE IF NOT EXISTS seq_inflowid START 1')

    con.sql('''CREATE TABLE IF NOT EXISTS CASH_OUTFLOW(
    OID INTEGER PRIMARY KEY,
    CATEGORY VARCHAR(50) NOT NULL
    )''')
    con.sql('CREATE SEQUENCE IF NOT EXISTS seq_outflowid START 1')

    con.sql('''CREATE TABLE IF NOT EXISTS DAILY_INFLOW(
    ENTRY_DATE DATE,
    INFLOW INTEGER,
    AMOUNT DOUBLE DEFAULT 0.0,
    PRIMARY KEY(ENTRY_DATE, INFLOW),
    FOREIGN KEY (INFLOW) REFERENCES CASH_INFLOW(IID)
    )''')

    con.sql('''CREATE TABLE IF NOT EXISTS DAILY_OUTFLOW(
    ENTRY_DATE DATE PRIMARY KEY,
    OUTFLOW INTEGER,
    AMOUNT DOUBLE DEFAULT 0.0,
    FOREIGN KEY (OUTFLOW) REFERENCES CASH_OUTFLOW(OID)
    )''')

    return con


def create_cash_flow(con, name, inflow=True):
    table_name = 'CASH_INFLOW' if inflow else 'CASH_OUTFLOW'
    seq_name = 'seq_inflowid' if inflow else 'seq_outflowid'

    con.execute(
        "SELECT * FROM " + table_name + " WHERE UPPER(CATEGORY) LIKE ?",
        [name])

    if len(con.fetchall()) == 0:
        con.execute("INSERT INTO " + table_name + " VALUES(nextVal(?), ?)",
                    [seq_name, name])

    con.table(table_name).show()


def get_all_cash_flows(con, inflow=True):
    table_name = 'CASH_INFLOW' if inflow else 'CASH_OUTFLOW'

    return con.sql("SELECT * FROM " + table_name).fetchall()


def get_daily_cash_flows(con, date, inflow=True):
    query = '''SELECT ENTRY_DATE, CATEGORY, AMOUNT
    FROM DAILY_{0}, CASH_{0}
    WHERE {0}={1} AND ENTRY_DATE=\'{2}\'
    '''.format('INFLOW' if inflow else 'OUTFLOW', 'IID' if inflow else 'OID',
               date)
    return con.sql(query)


def get_weekly_cash_flows(con, inflow=True):
    query = '''SELECT CATEGORY, SUM(AMOUNT) AS AMOUNT
    FROM DAILY_{0}, CASH_{0}
    WHERE {0}={1} AND ENTRY_DATE BETWEEN '{2}' AND '{3}'
    GROUP BY CATEGORY
    '''.format(
        'INFLOW' if inflow else 'OUTFLOW',
        'IID' if inflow else 'OID',
        utils.get_today_formatted(7),
        utils.get_today_formatted(),
    )
    return con.sql(query)
