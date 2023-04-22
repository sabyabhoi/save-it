import duckdb
import inquirer


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
    questions = [
        inquirer.List('choice',
                      message='Select a Choice',
                      choices=[('Create cash flow', 'cf'),
                               ('View cash flow', 'cfv'),
                               ('None', 'n')])
    ]
    answer = inquirer.prompt(questions)
    while answer['choice'] != 'n':
        match answer['choice']:
            case 'cf':
                cf_questions = [inquirer.List('type',
                                              message='Inflow or Outflow?',
                                              choices=['Inflow', 'Outflow']),
                                inquirer.Text(
                                    'name', message='Name of cash inflow')
                                ]
                cf = inquirer.prompt(cf_questions)

                create_cash_flow(
                    con, cf['name'],
                    inflow=True if cf['type'] == 'Inflow' else False)

            case 'cfv':
                cf = inquirer.list_input('Inflow or Outflow?',
                                         choices=[('Inflow', 'CASH_INFLOW'),
                                                  ('Outflow', 'CASH_OUTFLOW')])
                con.table(cf).show()

            case _:
                pass
        answer = inquirer.prompt(questions)


if __name__ == '__main__':
    con = get_db('file.db')
    menu(con)

    con.commit()
    con.close()
