from marshmallow import Schema, fields

from challenge.model import TaskStatus


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    url = fields.String(required=True)
    parameters = fields.String(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    task_interval = fields.Integer(required=True)
    max_execution_time = fields.Integer(required=True)
    fetch_start_time = fields.DateTime(dump_only=True)
    fetch_end_time = fields.DateTime(dump_only=True)
    fetch_result = fields.Enum(TaskStatus, dump_only=True)
    max_attempt = fields.Integer(required=True)
    attempt = fields.Integer(dump_only=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class DataSchema(Schema):
    id = fields.Integer(dump_only=True)
    job_id = fields.Integer(dump_only=True)
    data_id = fields.String(dump_only=True)
    name_first = fields.String(dump_only=True)
    name_last = fields.String(dump_only=True)
    decription = fields.String(dump_only=True)


class TaskStatusSchema(Schema):
    id = fields.Integer(dump_only=True)
    last_execute_time = fields.DateTime()
    execution_time = fields.Integer()
    last_execution_status = fields.String()
    last_execution_error = fields.String()
    last_execution_data = fields.Nested(DataSchema, many=True)
