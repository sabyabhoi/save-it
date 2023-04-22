import duckdb


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

    print(table_name + ':')
    con.table(table_name).show()


def menu(con):
    print('Enter option:')
    print('1. Create cash inflow')
    print('2. Create cash outflow')
    chosen = int(input().strip())
    if chosen == 1:
        print('Enter inflow name: ', end='')
        name = input().strip()
        create_cash_flow(con, name, inflow=True)
    elif chosen == 2:
        print('Enter outflow name: ', end='')
        name = input().strip()
        create_cash_flow(con, name, inflow=False)


if __name__ == '__main__':
    con = get_db('file.db')
    menu(con)

    con.commit()
    con.close()
