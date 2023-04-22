import menu
import db

if __name__ == '__main__':
    con = db.get_db('file.db')
    try:
        menu.menu(con)
    except Exception:
        pass

    con.commit()
    con.close()
