from fpdf import FPDF, XPos, YPos
import db

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0,
         10,
         'Weekly Budget Report',
         align='C',
         new_x=XPos.LMARGIN,
         new_y=YPos.NEXT)


def new_line():
    return pdf.cell(0, 10, '', new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def df_to_table(df, caption=''):
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, caption, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 12)
    with pdf.table(width=100) as table:
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


new_line()
pdf.set_font('Helvetica', '', 10)
con = db.get_db('file.db')

df = db.get_weekly_cash_flows(con).fetchdf()
df_to_table(df, 'Cash Inflow')

df = db.get_weekly_cash_flows(con, inflow=False).fetchdf()
df_to_table(df, 'Cash Outflow')

con.close()

pdf.output('output.pdf')
