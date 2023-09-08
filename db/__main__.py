from db.models import (
    add_measurement_record,
)

from importlib import resources

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def main():
    """Main entry point of program"""
    with resources.path("db.data", "sensor_data.db") as sqlite_filepath:
        engine = create_engine(f"sqlite:///{sqlite_filepath}")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()

    add_measurement_record(session=session)
    add_measurement_record(
        session=session, measurement_kind="humidity", measurement_value=99.0
    )


if __name__ == "__main__":
    main()
