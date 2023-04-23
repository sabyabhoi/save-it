from fpdf import FPDF, XPos, YPos
import db


def new_line(pdf):
    return pdf.cell(0, 10, '', new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def df_to_table(pdf, df, caption=''):
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, caption, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    with pdf.table(width=80) as table:
        row = table.row()
        for col in df.columns:
            row.cell(col, align='C')
        for i in range(len(df)):
            row = table.row()
            for r in range(len(df.iloc[i])):
                if type(df.iloc[i, r]) is str:
                    row.cell(df.iloc[i, r])
                else:
                    row.cell(str(df.iloc[i, r]), align='R')


def generate_report(con, filename):
    pdf = FPDF()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.add_page()
    pdf.cell(0,
             10,
             'Weekly Budget Report',
             align='C',
             new_x=XPos.LMARGIN,
             new_y=YPos.NEXT)
    new_line(pdf)
    pdf.set_font('Helvetica', '', 10)

    df = db.get_weekly_cash_flows(con).fetchdf()
    df_to_table(pdf, df, 'Cash Inflow')

    df = db.get_weekly_cash_flows(con, inflow=False).fetchdf()
    df_to_table(pdf, df, 'Cash Outflow')

    pdf.output(filename)
