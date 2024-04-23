
from flask import jsonify
def response_parser(item):
    """
    Parses the response to JSON
    """
    return jsonify(item)