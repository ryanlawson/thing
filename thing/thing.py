import uuid
from thing.dynamodb import delete_item, get_item, put_item, query

def create_thing(thing):
    new_thing_id = str(uuid.uuid4())
    return put_item(thing | {'thingId': new_thing_id}, allow_replacement=False)

def retrieve_all_things():
    return query()

def retrieve_thing(thing_id):
    return get_item(thing_id)

def replace_thing(thing_id, thing):
    return put_item(thing | {'thingId': thing_id})

def delete_thing(thing_id):
    return delete_item(thing_id)
