import click

from ERG3010_project import app, db
from ERG3010_project.models import Singer, Song


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    """Initialize the database."""
    if (drop):
        click.confirm("Confirm?", abort=True)
        db.drop_all()
        click.echo("Drop tables")
    db.create_all()
    click.echo("init database")


@app.cli.command()
@click.option("--count", default=20, help="Quantity of messages, default is 20.")
def forge(count):
    """Generate fake messages."""
    from faker import Faker

    # db.drop_all()
    # db.create_all()
    singer_table = Singer.query.all()
    song_table = Song.query.all()
    for index in range(len(singer_table)):
        db.session.delete(singer_table[index])
        db.session.delete(song_table[index])

    db.session.commit()

    fake = Faker("en_US")
    click.echo("Generating")

    for i in range(count):
        singers = Singer(
            singer_id=str(fake.random_int(min=0, max=9999999)),
            gender=str(fake.random_int(min=0, max=1)),
            region=fake.random_int(min=0, max=1),
            age=str(fake.random_int(min=0, max=99)),
            singer_name=fake.name()
        )
        db.session.add(singers)

        songs = Song(
            song_id=str(fake.random_int(min=0, max=999999)),
            play_times=fake.random_int(min=0, max=999),
            lyrics=fake.paragraph(),
            song_name=fake.word()
        )
        db.session.add(songs)

    db.session.commit()
    click.echo(f"Create {count} fake")
