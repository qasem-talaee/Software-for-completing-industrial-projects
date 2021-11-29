import sqlite3


class dbClass():
    def create_tables(self):
        #project table
        self.conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS project(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                budge FLOAT NOT NULL
            );
            '''
        )
        #product table
        self.conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS product(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INT NOT NULL,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                price FLOAT NOT NULL,
                value FLOAT NOT NULL
            );
            '''
        )
    
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.execute('pragma encoding=UTF8')
        self.create_tables()
        
    def select_pro(self):
        cursor = self.conn.execute("SELECT id, name from project")
        out = []
        for row in cursor:
            out.append([row[0], row[1]])
        return len(out), out
    
    def create_project(self, name, budge):
        param = (name, budge,)
        self.conn.execute("INSERT INTO project (name, budge) VALUES (?,?);", param)
        self.conn.commit()
        print('Done!')
    
    def add_product(self, pro_id, name, unit, price, value):
        param = (pro_id, name, unit, price, value,)
        self.conn.execute("INSERT INTO product (project_id, name, unit, price, value) VALUES (?,?,?,?,?);", param)
        self.conn.commit()
        print('Done!')
        
    def get_product(self, pro_id):
        cursor = self.conn.execute("SELECT * from product WHERE project_id={pro_id}".format(pro_id=str(pro_id)))
        out = []
        for row in cursor:
            out.append([row[0], row[2], row[3], row[4], row[5]])
        return len(out), out

    def edit_product(self, id, project_id, name, unit, price, value):
        param = (name, unit, price, value, id, project_id,)
        self.conn.execute("UPDATE product set name=?, unit=?, price=?, value=? where id=? and project_id=?;", param)
        self.conn.commit()
        print('Done!')
    
    def delete_product(self, id, project_id):
        param = (id, project_id,)
        self.conn.execute("DELETE from product where ID=? and project_id=?;", param)
        self.conn.commit()
        print('Done!')
        
    def get_budge(self, project_id):
        param = (project_id,)
        cursor = self.conn.execute("SELECT budge from project where id=?", param)
        for row in cursor:
            budge = row[0]
        return budge
    
    def get_edit_project(self, project_id):
        param = (project_id,)
        cursor = self.conn.execute("SELECT * from project where id=?", param)
        out = []
        for row in cursor:
            out.append(row[1])
            out.append(row[2])
        return out

    def edit_project(self, project_id, name, budge):
        param = (name, budge, project_id,)
        self.conn.execute("UPDATE project set name=?, budge=? where id=?;", param)
        self.conn.commit()
        print('Done!')