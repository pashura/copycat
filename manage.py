from flask.cli import FlaskGroup

from app import app, db, Transformations

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(Transformations(
        email="mpashura@spscommerce.com",
        design_name='Target_RSX_7.7_Invoices_to_X12_4010_Transaction-810')
    )
    db.session.commit()


if __name__ == "__main__":
    cli()
