import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

schema_v1 = avro.schema.make_avsc_object({
    'namespace': 'example.avro',
    'type': 'record',
    'name': 'User',
    'fields': [
        {'name': 'email', 'type': 'string'},
        {'name': 'username', 'type': 'string'},
    ]
}, avro.schema.Names())

schema_v2 = avro.schema.make_avsc_object({
    'namespace': 'example.avro',
    'type': 'record',
    'name': 'User',
    'fields': [
        {'name': 'email', 'type': 'string'},
        {'name': 'username', 'type': 'string'},
        {'name': 'firstName', 'type': 'string', 'default': ''},
        {'name': 'lastName', 'type': 'string', 'default': ''},
    ]
}, avro.schema.Names())


def get_writer(schema):
    return DataFileWriter(open('/tmp/users.avro', 'w'), DatumWriter(), schema)


def get_reader(writer_schema, reader_schema):
    return DataFileReader(open('/tmp/users.avro', 'r'), DatumReader(writer_schema, reader_schema))


writer_v1 = get_writer(schema_v1)
writer_v1.append({'email': 'president@whitehouse.gov', 'username': 'MrPresident'})
writer_v1.close()

reader_v1 = get_reader(schema_v1, schema_v1)
for user in reader_v1:
    print 'V1 -> V1: {}'.format(user)
reader_v1.close()

reader_v2 = get_reader(schema_v1, schema_v2)
for user in reader_v2:
    print 'V1 -> V2: {}'.format(user)
reader_v2.close()


writer_v2 = get_writer(schema_v2)
writer_v2.append({'email': 'president@whitehouse.gov', 'username': 'MrPresident', 'firstName': 'Frank', 'lastName': 'Underwood'})
writer_v2.close()

reader_v1 = get_reader(schema_v2, schema_v1)
for user in reader_v1:
    print 'V2 -> V1: {}'.format(user)
reader_v1.close()

reader_v2 = get_reader(schema_v2, schema_v2)
for user in reader_v2:
    print 'V2 -> V2: {}'.format(user)
reader_v2.close()
