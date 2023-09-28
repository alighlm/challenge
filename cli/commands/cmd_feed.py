import click

from challenge.app import create_app
from challenge.extensions import db
from challenge.model import TaskModel
from challenge.service.feed_service import feed_service

# Create an challenge context for the database connection.
app = create_app()
db.app = app


@click.command()
def cli():
    # from challenge.service.fetch_service import feachurl
    #
    # feachurl.delay("hello")

    #
    with app.app_context():
        feed_service()
    #     tasks = TaskModel.find_all_current_valid()
    #     print(tasks)
    #     for task in tasks:
    #         print(task)
