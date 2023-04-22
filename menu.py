import inquirer
import db
import datetime


def prompt_cash_flow(con):
    cf_questions = [inquirer.List('type',
                                  message='Inflow or Outflow?',
                                  choices=['Inflow', 'Outflow']),
                    inquirer.Text(
                        'name', message='Name of cash inflow')
                    ]
    cf = inquirer.prompt(cf_questions)

    db.create_cash_flow(
        con, cf['name'],
        inflow=True if cf['type'] == 'Inflow' else False)


def prompt_daily_entry(con):
    date = inquirer.text(
        'Enter the date', default=datetime.date.today().strftime('%Y-%m-%d'))

    # Inflows
    print('Inflows:')
    inflows = db.get_all_cash_flows(con)

    questions = [
        inquirer.Text(inflow[0],
                      message=inflow[1])
        for inflow in inflows
    ]
    answers = inquirer.prompt(questions)

    for key, val in answers.items():
        if len(val) != 0:
            con.execute('INSERT INTO DAILY_INFLOW VALUES(?, ?, ?)',
                        [date, key, float(val.strip())])

    # Outflows
    print('Outflows:')
    outflows = db.get_all_cash_flows(con, inflow=False)

    questions = [
        inquirer.Text(outflow[0],
                      message=outflow[1])
        for outflow in outflows
    ]
    answers = inquirer.prompt(questions)

    for key, val in answers.items():
        if len(val) != 0:
            con.execute('INSERT INTO DAILY_OUTFLOW VALUES(?, ?, ?)',
                        [date, key, float(val.strip())])


def menu(con):
    questions = [
        inquirer.List('choice',
                      message='Select a Choice',
                      choices=[('Create daily entry', 'daily'),
                               ('View daily entry', 'dailyview'),
                               ('Create cash flow', 'cf'),
                               ('View cash flow', 'cfv'),
                               ('None', 'n')])
    ]
    answer = inquirer.prompt(questions)
    while answer['choice'] != 'n':
        match answer['choice']:
            case 'daily':
                prompt_daily_entry(con)
            case 'dailyview':
                print('Daily inflows:')
                db.get_daily_cash_flows(con).show()
                print('Daily outflows:')
                db.get_daily_cash_flows(con, inflow=False).show()
            case 'cf':
                prompt_cash_flow(con)
            case 'cfv':
                cf = inquirer.list_input('Inflow or Outflow?',
                                         choices=[('Inflow', 'CASH_INFLOW'),
                                                  ('Outflow', 'CASH_OUTFLOW')])
                con.table(cf).show()

            case _:
                pass
        answer = inquirer.prompt(questions)
