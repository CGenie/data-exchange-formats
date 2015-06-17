# Apache Avro

## General notes

Schema-based -- when Avro data is read, the schema is used.

Avro data is always serialized with its schema.

Lauguage syntax looks like JSON combined with JSONSchema.

No manually-assigned IDs. To allow version changes, old and new schemas
are stored with the data which allows to remap old data to new schema.