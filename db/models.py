from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Float,
    DateTime,
    create_engine,
)

from importlib import resources

from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

topic_sensor_measurement = Table(
    "topic_sensor_measurement",
    Base.metadata,
    Column("topic_num_id", Integer, ForeignKey("topics.topic_num_id")),
    Column(
        "sensor_measurement_num_id",
        Integer,
        ForeignKey("sensor_measurements.sensor_measurement_num_id"),
    ),
)

sensor_sensor_measurement = Table(
    "sensor_sensor_measurement",
    Base.metadata,
    Column("sensor_num_id", Integer, ForeignKey("sensors.sensor_num_id")),
    Column(
        "sensor_measurement_num_id",
        Integer,
        ForeignKey("sensor_measurements.sensor_measurement_num_id"),
    ),
)

measurement_kind_sensor_measurement = Table(
    "measurement_kind_sensor_measurement",
    Base.metadata,
    Column(
        "measurement_num_id",
        Integer,
        ForeignKey("measurements.measurement_num_id"),
    ),
    Column(
        "sensor_measurement_num_id",
        Integer,
        ForeignKey("sensor_measurements.sensor_measurement_num_id"),
    ),
)


class Topic(Base):
    """Create a topic table data model."""

    __tablename__ = "topics"
    topic_num_id = Column(Integer, primary_key=True)
    topic = Column(String, unique=True)


class Sensor(Base):
    """Create sensors table data model."""

    __tablename__ = "sensors"
    sensor_num_id = Column(Integer, primary_key=True)
    sensor_id = Column(String, unique=True)


class MeasurementKind(Base):
    """ "Create measurements table data model."""

    __tablename__ = "measurements"
    measurement_num_id = Column(Integer, primary_key=True)
    measurement_label = Column(String, unique=True)


class SensorMeasurement(Base):
    """Create sensor measurements table data model."""

    __tablename__ = "sensor_measurements"
    sensor_measurement_num_id = Column(Integer, primary_key=True)

    # topic_foreign_key = Column(Integer, ForeignKey("topics.topic_num_id"))
    topic = relationship(
        "Topic",
        secondary=topic_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    # sensor_foreign_key = Column(Integer, ForeignKey("sensors.sensor_num_id"))
    sensor = relationship(
        "Sensor",
        secondary=sensor_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    time = Column(DateTime(timezone=True), server_default=func.now())

    # measurment_foreign_key = Column(
    # Integer, ForeignKey("measurements.measurement_num_id")
    # )
    measurement_kind = relationship(
        "MeasurementKind",
        secondary=measurement_kind_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    measurement_value = Column(Float)

    def __repr__(self):
        return (
            f"topic: '{self.topic[0].topic}', sensor: '{self.sensor}', "
            "time: '{self.time}',"
            "measurement_kind: '{self.measurement_kind}', "
            "measurement_value: '{self.measurement_value}'"
        )


# Relationship Tables


# topic_sensor = Table(
#    "topic_sensor",
#    Base.metadata,
#    Column("topic_num_id", Integer, ForeignKey("topics.topic_num_id")),
#    Column("sensor_num_id", Integer, ForeignKey("sensors.sensor_num_id")),
# )
#
# measurement_sensor = Table(
#    "measurement_sensor",
#    Base.metadata,
#    Column(
#        "measurement_num_id",
#        Integer,
#        ForeignKey("measurements.measurement_num_id"),
#    ),
#    Column(
#        "sensor_num_id",
#        Integer,
#        ForeignKey("sensors.sensor_num_id"),
#    ),
# )

# create method to write measurements to database
def add_measurement_record(
    session,
    topic="sensor_data",
    sensor="env",
    measurement_label="temp",
    measurement_value=25.0,
):
    """Add a new measurement record to the database."""
    # create instance of SensorMeasurement
    measurement_record = SensorMeasurement(
        topic=[Topic(topic=topic)],
        sensor=[Sensor(sensor_id=sensor)],
        measurement_kind=[
            MeasurementKind(measurement_label=measurement_label)
        ],
        measurement_value=measurement_value,
    )
    session.add(measurement_record)
    session.commit()
    for entry in session.query(SensorMeasurement):
        print(entry)


with resources.path("db.data", "sensor_data.db") as sqlite_filepath:
    engine = create_engine(f"sqlite:///{sqlite_filepath}")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()
