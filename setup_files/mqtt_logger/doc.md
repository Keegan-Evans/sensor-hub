# tables
    - [x]  measurement_recordings (sensor, topic, timestamp, measurement_label, measurement_value)
    - [x]  sensors
    - [x]  topics
    - [x]  measurment_labels
# other things to do:
    - [ ] update access client(mqtt)
    - [ ] update message generation functionality in sensor-hub drivers
    - [ ] REST api to access db
    - [ ] Visualiztion server to serve dashboard
    - [ ] Determine best way to parse mqtt messages into database.
        - 1 mqtt client just hands complete message packet in and parsing is handled on database model side of things
        - 2 mqtt client parses message packet and runs seperate db update for each message segment.

    - [x] related to above, create read-logger function
    - [x] main function to actually run the thing
    - [x] implement update functions to add new entries to Topic, Sensor, and MeasurementKind tables.
    - [ ] change automation on sensor hub setup files to implement this database.
    - [ ] modify add_measurment_record to add_measurement_records, which will all writing an arbitrary number of measurements from the same mqtt packet
    - [ ] wire mqtt logger client to use "add_measurement_records"
