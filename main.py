import os
import click

from commands import users_commands
from commands.rooms_commands import update_topic
from database import database
from rooms import rooms_service
from users import users_service


def set_user_login(obj, login, password):
    with obj["session"]:
        cursor = obj["session"]
        user = users_service.login(cursor, login, password)
        if user is None:
            print("Wrong credentials!")
            exit(1)

        obj["user"] = user


@click.group()
@click.pass_context
def run_command(ctx):
    ctx.obj = {"session": database.get_session()}


@run_command.group("run")
def run_server_command():
    pass


root_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__))))


@run_server_command.command("as-server")
def as_server_command():
    import uvicorn

    uvicorn.run(
        "server:run",
        **{
            "reload": True,
            "reload_dirs": [root_dir],
            "factory": True,
            "port": 6543,
            "host": "localhost",
            "loop": "asyncio",
        }
    )


@run_command.group("user")
def user_command():
    pass


@user_command.command("register")
@click.option("--login", required=True, prompt=True)
@click.password_option()
@click.pass_obj
def register_command(obj, login, password):
    out = users_commands.register(obj["session"], login, password)
    if out is not None:
        print(out)
        exit(1)


@user_command.group("login")
@click.option("--login", required=True, prompt=True)
@click.password_option(confirmation_prompt=False)
@click.pass_obj
def login_command(obj, login, password):
    set_user_login(obj, login, password)


@login_command.command("list")
@click.pass_obj
@click.option("--filter", required=False)
def list_command(obj, filter):
    for user in users_service.get_all_users(obj["session"]):
        if filter is None:
            print(user.login)
        elif user.login.find(filter) > -1:
            print(user.login)


@login_command.command("remove")
@click.pass_obj
@click.option("--login-to-remove", required=True, prompt=True)
def remove_command(obj, login):
    with obj["session"]:
        users_service.remove_user(obj["session"].cursor(), login)


@run_command.group("session")
def db_command():
    pass


@db_command.command("initialize")
def initialize_command():
    database.init_db()


@run_command.group("room")
@click.option("--login", required=True, prompt=True)
@click.password_option(confirmation_prompt=False)
@click.pass_obj
def rooms_command(obj, login, password):
    set_user_login(obj, login, password)


@rooms_command.command("create")
@click.password_option("--room-password", confirmation_prompt=True)
@click.option("--name", confirmation_prompt=True)
@click.pass_obj
def create_command(obj, room_password, name):
    with obj["session"]:
        rooms_service.create_room(
            obj["session"], obj["user"].id, room_password, name
        )


@rooms_command.command("delete")
@click.option("--room-id", required=True, prompt=True, type=click.types.INT)
@click.pass_obj
def delete_room_command(obj, room_id):
    with obj["session"]:
        cursor = obj["session"]

        room = rooms_service.get_room(cursor, room_id)
        if room is None:
            print("Wrong room id!")
            exit(1)

        if room.owner_id != obj["user"].id:
            print("Wrong room id!")
            exit(1)

        rooms_service.delete_room_by_id(cursor, room_id)


@rooms_command.command("join")
@click.option("--room-id", required=True, prompt=True, type=click.types.INT)
@click.password_option("--room-password", confirmation_prompt=False)
@click.pass_obj
def join_room_command(obj, room_id, room_password):
    with obj["session"]:
        if not rooms_service.join_room(
            obj["session"], obj["user"].id, room_id, room_password
        ):
            print("Wrong room id or passowrd!")
            exit(1)


@rooms_command.command("set-topic")
@click.option("--room-id", required=True, prompt=True, type=click.types.INT)
@click.option("--new-topic", required=True, prompt=True)
@click.pass_obj
def set_topic_command(obj, room_id, new_topic):
    with obj["session"]:
        cursor = obj["session"]
        room = rooms_service.get_room(cursor, room_id)
        if room is None:
            print("Unknown room!")
            exit(1)

        if room.owner_id != obj["user"].id:
            print("Unknown room!")
            exit(1)

        update_topic(cursor, room_id, new_topic)


@rooms_command.command("vote")
@click.option("--topic-id", required=True, prompt=True, type=click.types.INT)
@click.option("--value", required=True, prompt=True, type=click.types.FLOAT)
@click.pass_obj
def vote_command(obj, topic_id, value):
    with obj["session"]:
        cursor = obj["session"]
        topic = rooms_service.get_topic_by_id(cursor, topic_id)
        if topic is None:
            print("Wrong topic!")
            exit(1)

        if not rooms_service.joined_room(cursor, obj["user"].id, topic.room_id):
            print("Wrong topic!")
            exit(1)

        rooms_service.add_vote(cursor, topic_id, value, obj["user"].id)


if __name__ == "__main__":
    run_command()
