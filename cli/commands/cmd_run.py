import time

import click

from challenge.app import create_app
from challenge.extensions import db
from challenge.model import TaskModel
from challenge.service.feed_service import feed_service


app = create_app()
db.app = app


@click.command()
def cli():
    with app.app_context():
        while True:
            feed_service()
            time.sleep(1)
