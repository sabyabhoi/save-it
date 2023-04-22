import inquirer
import db


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

                db.create_cash_flow(
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
