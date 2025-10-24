import psycopg2


class DatabaseExecution:

    def __init__(self, dbconfig):
        self.con = psycopg2.connect(**dbconfig)
        self.cur = self.con.cursor()
        print("Database connected")

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                model_name VARCHAR(255) UNIQUE, 
                release_date VARCHAR(255),
                display TEXT,
                battery VARCHAR(100),
                camera TEXT,
                ram_storage_options TEXT,
                price INT
            );
        """)
        self.con.commit()
        print("Table 'phones' is ready.")

    def table_exists(self):
        """Check if 'phones' table exists"""
        self.cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'phones'
            );
        """)
        return self.cur.fetchone()[0]

    def is_table_empty(self, table_name="phones"):
        self.cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = self.cur.fetchone()[0]
        return count == 0

    def insert_data(self, phone_list):
        if not phone_list:
            print("No data to insert")
            return

        data_to_insert = []
        for phone in phone_list:
            row = (
                phone['model_name'],
                phone['release_date'],
                phone['display'],
                phone['battery'],
                phone['camera'],
                phone['ram_storage_options'],
                phone['price']
            )

            data_to_insert.append(row)
        sql_query = """
            INSERT INTO phones (
                model_name , 
                release_date ,
                display ,
                battery ,
                camera ,
                ram_storage_options ,
                price
            ) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        try:
            self.cur.executemany(sql_query, data_to_insert)
            self.con.commit()
            print("Data saved to database")
        except Exception as e:
            self.con.rollback()
            print(f"Database insert error: {e}")
            raise

    def close(self):
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()
            print("Database connection closed")



