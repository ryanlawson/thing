import json, re
from thing.logger import logger
from thing.thing import create_thing, delete_thing, replace_thing, retrieve_all_things, retrieve_thing

DELETE = 'DELETE'
GET = 'GET'
POST = 'POST'
PUT = 'PUT'

HEALTH_PATH = 'health'
THING_PATH = 'thing'
THING_PATH_WITH_ID_REGEX = '^thing/[0-9A-Za-z-]$'

def handler(event, _):
    method = event['httpMethod'].upper()
    path = event['path'].strip('/').lower()

    logger.info(f'Received request: {method} {path}')
    logger.debug(f'Request event: {str(event)}')
    
    if method == GET and path == HEALTH_PATH:
        logger.info('Responding to Health Check request')
        return respond(200)
    
    if method == GET and path == THING_PATH:
        logger.info('Responding to Retrieve All Things request')
        all_things, error = retrieve_all_things
        if error != None:
            return error_response(error)
        return respond(200, all_things)
    
    if method == POST and path == THING_PATH:
        logger.info('Responding to Create Thing request')
        try:
            thing = json.loads(event['body'])
        except:
            return respond(400)
        thing_id, error = create_thing(thing)
        if error != None:
            return error_response(error)
        return respond(204, None, {'Location': f'/thing/{thing_id}'})
    
    if method == GET and re.fullmatch(path, THING_PATH_WITH_ID_REGEX):
        logger.info('Responding to Retrieve Thing request')
        thing_id = path.split('/').pop()
        thing, error = retrieve_thing(thing_id)
        if error != None:
            return error_response(error)
        return respond(200, thing)
    
    if method == PUT and re.fullmatch(path, THING_PATH_WITH_ID_REGEX):
        logger.info('Responding to Replace Thing request')
        try:
            thing = json.loads(event['body'])
        except:
            return respond(400)
        thing_id = path.split('/').pop()
        error = replace_thing(thing_id, thing)
        if error != None:
            return error_response(error)
        return respond(204)
 
    if method == DELETE and re.fullmatch(path, THING_PATH_WITH_ID_REGEX):
        logger.info('Responding to Delete Thing request')
        thing_id = path.split('/').pop()
        error = delete_thing(thing_id, thing)
        if error != None:
            return error_response(error)
        return respond(204)
    
    logger.error('Unable to map the request to a function')
    return respond(404)

def respond(http_status, body=None, headers={}):
    response = {
        'httpStatus': http_status,
        'body': None,
        'isBase64Encoded': False,
        'headers': headers
    }

    logger.info(f'Responding with HTTP status: {http_status}')

    if body != None:
        response['body'] = json.dumps(body)
        response['headers'] = headers | {'Content-Type': 'application/json'}
        logger.debug(f'Responding with body: {str(body)}')
    
    logger.info(f'Responding with headers: {str(headers)}')

    return response

def error_response(error_code):
    logger.info(f'Error thrown: {error_code}')

    if error_code == 1:
        return respond(400, {'error': 'Improper JSON request'})

    if error_code == 2:
        return respond(404, {'error': 'Item not found'})

    return respond(500, {'error': 'Unable to process the request'})
