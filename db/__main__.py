from db.models import (
    Topic,
    Sensor,
    MeasurementKind,
    SensorMeasurement,
    # topic_sensor,
    # measurement_sensor,
    add_measurement_record,
)

from importlib import resources

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# from sqlalchemy.sql import asc, desc, func

# from treelib import Tree


def main():
    """Main entry point of program"""

    # Connect to the database using SQLAlchemy
    with resources.path("db.data", "sensor_data.db") as sqlite_filepath:
        engine = create_engine(f"sqlite:///{sqlite_filepath}")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()

    add_measurement_record(session=session)


if __name__ == "__main__":
    main()
