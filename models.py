from sqlalchemy import Column, Integer, TIMESTAMP, String, BOOLEAN, FLOAT, ARRAY, func, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.engine import Connection
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

# Define the Base for declarative models
Base = declarative_base()


# Define your models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class BinanceKeys(Base):
    __tablename__ = 'binance_keys'
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, index=True)
    api_secret = Column(String, index=True)


class Signals(Base):
    __tablename__ = 'signals'
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    signal = Column(String, index=True)
    entry_price = Column(String, index=True)
    indicator = Column(String, index=True)
    timestamp = Column(TIMESTAMP, server_default=func.now(), index=True)


class TradeCoins(Base):
    __tablename__ = 'trade_coins'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    quantity = Column(Integer, index=True)
    checkpoints = Column(ARRAY(FLOAT), nullable=True)
    stop_loss = Column(FLOAT, index=True)
    indicator = Column(String, index=True)
    is_finished = Column(BOOLEAN, index=True)


class IsFinished(Base):
    __tablename__ = 'is_finished'

    id = Column(Integer, primary_key=True, index=True)
    is_finished = Column(BOOLEAN, index=True)


# Create Pydantic model from SQLAlchemy model
User_Pydantic = sqlalchemy_to_pydantic(User)

# Connection URL for default 'postgres' database
DATABASE_URL = "postgresql://postgres:admin@localhost:5433/postgres"

# Connect to the default 'postgres' database
engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
connection = engine.connect()

# Create the 'miya_test' database if it doesn't exist
try:
    connection.execute(text("CREATE DATABASE miya_test"))
    print("Database 'miya_test' created successfully.")
except (ProgrammingError, OperationalError) as e:
    print(f"Database 'miya_test' creation failed or already exists: {str(e)}")

connection.close()

# Now connect to the newly created 'miya_test' database
DATABASE_URL_NEW = "postgresql://postgres:admin@pgdb:5432/miya"
engine_new = create_engine(DATABASE_URL_NEW)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_new)


# Create all tables
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
    create_tables()
