import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    height = data["board"]["height"]
    width = data["board"]["width"]
    body = data["you"]["body"]
    head = body[0]

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    # Check if move left is valid
    if {"x": head["x"] - 1, "y": head["y"]} not in body and head["x"] - 1 >= 0 and head["y"] >= 0 and head["x"] - 1 < width and head["y"] < height:
        return move_response('left')
    # Check if move down is valid
    elif {"x": head["x"], "y": head["y"] + 1} not in body and head["x"] >= 0 and head["y"] + 1 >= 0 and head["x"] < width and head["y"] + 1 < height:
        return move_response('down')
    # Check if move right is valid
    elif {"x": head["x"] + 1, "y": head["y"]} not in body and head["x"] + 1 >= 0 and head["y"] >= 0 and head["x"] + 1 < width and head["y"] < height:
        return move_response('right')
    # Check if move up is valid
    elif {"x": head["x"], "y": head["y"] - 1} not in body and head["x"] >= 0 and head["y"] - 1 >= 0 and head["x"] < width and head["y"] - 1 < height:
        return move_response('up')

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
