import menu
import db

if __name__ == '__main__':
    con = db.get_db('file.db')
    menu.menu(con)

    con.commit()
    con.close()
