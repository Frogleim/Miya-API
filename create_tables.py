from models import Base, engine, create_engine  # Assuming your models are in a file named `models.py`
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, OperationalError

DATABASE_URL = "postgresql://postgres:admin@localhost:5433/postgres"
connection = engine.connect()


def create_database():
    try:
        connection.execute(text("CREATE DATABASE miya_test"))
        print("Database 'miya_test' created successfully.")
    except (ProgrammingError, OperationalError) as e:
        print(f"Database 'miya_test' creation failed or already exists: {str(e)}")

    connection.close()


DATABASE_URL_NEW = "postgresql://postgres:admin@localhost:5433/miya_test"

engine_new = create_engine(DATABASE_URL_NEW)


def create_tables():
    try:
        # Check the connection first
        with engine_new.connect() as conn:
            print("Successfully connected to the database.")

        # Create the tables
        Base.metadata.create_all(bind=engine_new)
        print("All tables created successfully.")
    except Exception as e:
        print(f"An error occurred while creating tables: {str(e)}")



if __name__ == "__main__":
    create_database()
    create_tables()
