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

    def add(self, session, topic_to_add):
        """Add a new topic to the database."""
        topic = (
            session.query(Topic).filter_by(topic=topic_to_add).one_or_none()
        )
        if topic is None:
            return
        session.add(Topic(topic=topic_to_add))
        session.commit()


class Sensor(Base):
    """Create sensors table data model."""

    __tablename__ = "sensors"
    sensor_num_id = Column(Integer, primary_key=True)
    sensor_id = Column(String, unique=True)

    def add(self, session, sensor_to_add):
        """Add a new sensor to the database."""
        sensor = (
            session.query(Sensor).filter_by(sensor=sensor_to_add).one_or_none()
        )
        if sensor is None:
            return
        session.add(Sensor(sensor=sensor_to_add))
        session.commit()


class MeasurementKind(Base):
    """ "Create measurements table data model."""

    __tablename__ = "measurements"
    measurement_num_id = Column(Integer, primary_key=True)
    measurement_kind = Column(String, unique=True)

    def add(self, session, measurement_to_add):
        """Add a new measurement kind to the database."""
        measurement_kind = (
            session.query(MeasurementKind)
            .filter_by(measurement_kind=measurement_to_add)
            .one_or_none()
        )
        if measurement_kind is None:
            return
        session.add(MeasurementKind(measurement_kind=measurement_to_add))
        session.commit()


class SensorMeasurement(Base):
    """Create sensor measurements table data model."""

    __tablename__ = "sensor_measurements"
    sensor_measurement_num_id = Column(Integer, primary_key=True)

    topic = relationship(
        "Topic",
        secondary=topic_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    sensor = relationship(
        "Sensor",
        secondary=sensor_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    time = Column(DateTime(timezone=True), server_default=func.now())

    measurement_kind = relationship(
        "MeasurementKind",
        secondary=measurement_kind_sensor_measurement,
        backref=backref("sensor_measurements"),
    )

    measurement_value = Column(Float)

    def __repr__(self):
        return (
            "topic: {}, sensor: {}, "
            "time: {}, "
            "measurement_kind: {}, "
            "measurement_value: {}".format(
                self.topic[0].topic,
                self.sensor[0].sensor_id,
                self.time.strftime("%Y-%m-%d %H:%M:%S"),
                self.measurement_kind[0].measurement_kind,
                self.measurement_value,
            )
        )


def add_measurement_record(
    session,
    topic="sensor_data",
    sensor="env",
    measurement_kind="temp",
    measurement_value=25.0,
):
    """Add a new measurement record to the database."""
    # create instance of SensorMeasurement
    target_topic = session.query(Topic).filter_by(topic=topic).one_or_none()
    if target_topic is None:
        target_topic = Topic(topic=topic)
        session.add(target_topic)

    sensor_id = session.query(Sensor).filter_by(sensor_id=sensor).one_or_none()
    if sensor_id is None:
        sensor_id = Sensor(sensor_id=sensor)
        session.add(sensor_id)

    target_measurement_kind = (
        session.query(MeasurementKind)
        .filter_by(measurement_kind=measurement_kind)
        .one_or_none()
    )
    if target_measurement_kind is None:
        target_measurement_kind = MeasurementKind(
            measurement_kind=measurement_kind
        )
        session.add(target_measurement_kind)
        print(measurement_kind)
        raise

    measurement_record = SensorMeasurement(
        topic=[target_topic],
        sensor=[sensor_id],
        measurement_kind=[target_measurement_kind],
        measurement_value=measurement_value,
    )
    session.add(measurement_record)
    session.commit()
    for entry in session.query(SensorMeasurement):
        try:
            print(entry)
        except Exception:
            # TODO: add logging
            continue


with resources.path("db.data", "sensor_data.db") as sqlite_filepath:
    engine = create_engine(f"sqlite:///{sqlite_filepath}")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()
