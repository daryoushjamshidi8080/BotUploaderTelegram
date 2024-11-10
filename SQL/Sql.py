import psycopg2 # libary connect to databas

class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None #attribute connect to data base 
        self.cur = None
        self.open()
    # Open database
    def open(self):
        #connet database with library pycopg2
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        self.cur =self.conn.cursor()#Database stability
    #close of database 
    def close(self):
        self.cur.close()
        self.conn.close()

    #insert data path link
    def insert_path_link(self, information):
        try:
            self.open()
            self.cur.execute("INSERT INTO path_link(link_id) VALUES (%s)",  (information,))
            self.conn.commit()#seting qeury to database
        except Exception as e :
            print(f"Error insert path link: {e}")
            self.conn.rollback()#Remove half operations
        finally:
            self.close()

    #insert data path media
    def insert_path_media(self, information):
        try:
            self.open()
            self.cur.execute("INSERT INTO path_movie(path_movie, PlinkID) VALUES (%s, %s)",  tuple(information))
            self.conn.commit()#seting qeury to database
        except Exception as e :
            print(f"Error insert path link: {e}")
            self.conn.rollback()#Remove half operations
        finally:
            self.close()

    # fetch path link 
    def fetch_path_link(self):
        try:
            self.open()
            self.cur.execute("SELECT * FROM path_link  ORDER BY PLinID DESC LIMIT 1")
            results_data = self.cur.fetchall()
            return results_data
        except Exception as e :
            print('Error in fetch user_id of show id is : ',e)
        finally:
            self.close()