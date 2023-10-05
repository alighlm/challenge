import json

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from challenge.model import TaskModel, TaskStatus, JobModel, DataModel
from challenge.resource.schemas import TaskSchema, TaskStatusSchema
from lib.access_level_decorator import admin_required

blp = Blueprint("tasks", __name__, description="Operation on tasks")


@blp.route("/tasks/<int:task_id>")
class Task(MethodView):
    @admin_required()
    @blp.response(200, TaskSchema())
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

    # add type hint
    @admin_required()
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        task.delete()
        return {"message": "Task id {} is deleted".format(task_id)}


@blp.route("/tasks/<int:task_id>/reset-attempt")
class TaskResetAttempt(MethodView):
    @admin_required()
    def post(self, task_id):
        TaskModel.reset_attempt(task_id)
        return {
            "message": "Max attempt of task id {} is has been reset".format(task_id)
        }


@blp.route("/tasks/<int:task_id>/status")
class TaskStatusAPI(MethodView):
    @admin_required()
    @blp.response(200, TaskStatusSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        job = JobModel.find_last_job_by_task_id(task.id)
        data = DataModel.find_by_job_id(job.id)
        response = dict()
        response["id"] = task.id
        response["last_execute_time"] = task.fetch_end_time
        if task.fetch_result == TaskStatus.Finished:
            response["execution_time"] = (
                task.fetch_end_time - task.fetch_start_time
            ).total_seconds()
            response["last_execution_error"] = ""
            response["last_execution_data"] = data
        else:
            response["execution_time"] = 0
            response["last_execution_error"] = job.response
            response["last_execution_data"] = None

        response["last_execution_status"] = task.fetch_result

        return response


@blp.route("/tasks")
class TaskList(MethodView):
    @admin_required()
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()

    @admin_required()
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, item_data):
        item = TaskModel(**item_data)
        try:
            item.save()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the task")

        return item
