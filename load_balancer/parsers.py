from flask import jsonify


def response_parser(item, response_code=200):
    """
    Parses the response to JSON
    """
    return jsonify(item), response_code
