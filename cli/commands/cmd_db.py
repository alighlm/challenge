import random

import click

from datetime import datetime, timezone, timedelta
from sqlalchemy_utils import database_exists, create_database
from faker import Faker

from challenge.app import create_app
from challenge.extensions import db
from challenge.model import TaskModel

# Create an challenge context for the database connection.
app = create_app()
db.app = app
fake = Faker()


@click.group()
def cli():
    """Run mysql related tasks."""
    pass


@click.command()
@click.option(
    "--with-testdb/--no-with-testdb", default=True, help="Create a test db too?"
)
def init(with_testdb):
    with app.app_context():
        db.drop_all()
        db.create_all()

    if with_testdb:
        db_uri = "{0}_test".format(app.config["SQLALCHEMY_DATABASE_URI"])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


@click.command()
def seed():
    """
    Generate fake tasks.
    @return:
    """

    random_names = []
    data = []
    click.echo("Working...")

    # Ensure we get about 100 unique random emails.
    for i in range(0, 10):
        random_names.append(fake.name())

    random_names = list(set(random_names))
    url = [
        "https://s3-us-west-2.amazonaws.com/eb-python-challenge/php-architecture/",
        "https://s3-us-west-2.amazonaws.com/eb-python-challenge/php-architecture/",
        "https://s3-us-west-2.amazonaws.com/eb-python-challenge/php-architecture/",
    ]

    url_params = [
        '{"eventfile":"salesmeeting2020.json", "token":"mytoken123", "apiuser" : "test"}',
        '{"eventfile":"amazingexpo2020.json", "token":"mytoken123", "apiuser" : "test"}',
        '{"eventfile":"ceosummersummit2020.json", "token":"mytoken123", "apiuser" : "test"}',
    ]

    while True:
        if len(random_names) == 0:
            break

        name = random_names.pop()
        fake_start_time = datetime.now(timezone.utc) - timedelta(days=10)

        fake_end_time = datetime.now(timezone.utc) + timedelta(days=10)

        random_index = random.randint(0, 2)
        params = {
            "name": name,
            "url": url[random_index],
            "parameters": url_params[random_index],
            "start_time": fake_start_time,
            "task_interval": 2,
            "end_time": fake_end_time,
            "max_execution_time": 100,
        }

        task = TaskModel(**params)
        with app.app_context():
            task.save()


@click.command()
@click.option(
    "--with-testdb/--no-with-testdb", default=False, help="Create a test db too?"
)
@click.pass_context
def reset(ctx, with_testdb):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(seed)

    return None


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
