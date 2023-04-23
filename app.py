#!/usr/bin/env python3
import menu
import db

if __name__ == '__main__':
    con = db.get_db('/home/cognusboi/workspace/userfiles/Media/Documents/file.db')
    try:
        menu.menu(con)
    except Exception as e:
        print(e)

    con.commit()
    con.close()
