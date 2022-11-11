from rooms import rooms_service
from sqlalchemy.orm.session import Session



def update_topic(session: Session, room_id: int, new_topic: str):
    topic = rooms_service.get_topic(session, room_id)
    if topic is not None:
        rooms_service.remove_all_votes(session, topic.id)
        rooms_service.remove_topic(session, room_id)

    rooms_service.create_topic(session, room_id, new_topic)
