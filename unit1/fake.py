from faker import Faker
import psycopg2
from psycopg2 import OperationalError

fake = Faker()
generated_ids = set()

def create_connection():
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        print("Connection to PostgreSQL DB successful")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None



def generate_data(conn, table_name, num_samples):
    cursor = conn.cursor()
    for _ in range(num_samples):
        event_id =fake.uuid4()
        event_name = fake.word()
        event_address = fake.address()
        event_desc = fake.text()

        query = f"INSERT INTO {table_name} (id,event_name, event_address, event_desc) VALUES (%s,%s, %s, %s)"
        cursor.execute(query, (event_id,event_name, event_address, event_desc))

    conn.commit()
    cursor.close()
    print(f"Inserted {num_samples} records into {table_name}.")
    insert_data(conn, 'public.events', event_id)

def insert_data(conn, table_name, event_id):
    cursor = conn.cursor()
    event_name = fake.word()
    event_address = fake.address()
    event_desc = fake.text()

    query = f"INSERT INTO {table_name} (id,event_name, event_address, event_desc) VALUES (%s,%s, %s, %s)"
    cursor.execute(query, (event_id, event_name, event_address, event_desc))


    conn.commit()
    cursor.close()
    print(f"Inserted event with the id {event_id}  into {table_name}.")

conn = create_connection()
generate_data(conn, 'public.more_events', 10)
conn.close()
