from app.models import db, Tag


def get_or_create_tags(tag):
    tags = [t.strip() for t in tag.split(',') if t.strip()]
    if not tags:
        tags = ['indefinie']
    tag_objs = []
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
    db.session.commit()
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        tag_objs.append(tag)
    return tag_objs


def serialize_list(lst):
    return {
        "id": lst.id,
        "name": lst.name,
        "tags": [tag.name for tag in lst.tags],
        "creation_date": lst.creation_date.isoformat()
    }


def serialize_item(item):
    return {
        "id": item.id,
        "quantity": item.quantity,
        "done": item.done,
        "text": item.suggestion.text
    }


def serialize_suggestion(suggestion):
    return {
        "id": suggestion.id,
        "text": suggestion.text,
        "tag": suggestion.tag
    }
