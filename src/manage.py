import click
from sqlalchemy.orm import Session

import crud
from db.session import DBSession


@click.group()
def manage():
    pass


@click.command()
@click.argument("email")
@click.argument("password")
def createsuperuser(email, password):
    db = DBSession
    user = crud.user.create_superuser(db=db, email=email, password=password)


manage.add_command(createsuperuser)


if __name__ == "__main__":
    manage()
