from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Float,
    DateTime,
)

# from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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


class Measurement(Base):
    """ "Create measurements table data model."""

    __tablename__ = "measurements"
    measurement_num_id = Column(Integer, primary_key=True)
    measurement = Column(String, unique=True)


class SensorMeasurement(Base):
    """Create sensor measurements table data model."""

    __tablename__ = "sensor_measurements"
    sensor_measurement_num_id = Column(Integer, primary_key=True)

    topic = Column(String, ForeignKey("topics.topic_num_id"))

    sensor = Column(String, ForeignKey("sensors.sensor_num_id"))

    time = Column(DateTime(timezone=True), server_default=func.now())

    measurement_label = Column(
        String, ForeignKey("measurements.measurement_num_id")
    )
    measurement_value = Column(Float)


# Relationship Tables

topic_sensor = Table(
    "topic_sensor",
    Base.metadata,
    Column("topic_num_id", Integer, ForeignKey("topics.topic_num_id")),
    Column("sensor_num_id", Integer, ForeignKey("sensors.sensor_num_id")),
)

measurement_sensor = Table(
    "measurement_sensor",
    Base.metadata,
    Column(
        "measurement_num_id",
        Integer,
        ForeignKey("measurements.measurement_num_id"),
    ),
    Column(
        "sensor_num_id",
        Integer,
        ForeignKey("sensors.sensor_num_id"),
    ),
)
