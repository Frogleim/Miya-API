# create_tables.py
from models import Base, engine  # Assuming your models are in a file named `models.py`


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
