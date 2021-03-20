#!C:/Users/adzho/anaconda3/python

from flask import Flask, jsonify, request
import logging
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "message": "Bitly Challenge",
        "creator": "Adam Zhou <adzhou218@gmail.com>"
    })


@app.route('/v4/user', methods=['GET'])
def get_user():
    """
    Get user information

    Sample req: 
    curl -H "Authorization: <token>" http://localhost:5000/v4/user
    """
    endpoint = 'https://api-ssl.bitly.com/v4/user'
    auth_header = request.headers.get('Authorization')
    response = send_request(endpoint, auth_header, payload=request.args)
    return jsonify(response.json())


@app.route('/v4/bitlinks/<string:uri>/<string:suburi>/countries', methods=['GET'])
def get_clicks_by_country(uri, suburi):
    """
    Get number of clicks by country for a bitlink

    Sample request:
    curl -H "Authorization: <token>" http://localhost:5000/v4/bitlinks/<uri>/<suburi>/countries
    """
    endpoint = f'https://api-ssl.bitly.com/v4/bitlinks/{uri}/{suburi}/countries'
    auth_header = request.headers.get('Authorization')
    response = send_request(endpoint, auth_header, payload=request.args)
    return jsonify(response.json())


@app.route('/v4/groups/<string:group_id>/bitlinks', methods=['GET'])
def get_bitlinks_by_group(group_id):
    """
    Get bitlink information for a group

    Sample request:
    curl -H "Authorization: <token>" http://localhost:5000/v4/groups/<group_id>/bitlinks
    """
    endpoint = f'https://api-ssl.bitly.com/v4/groups/{group_id}/bitlinks'
    auth_header = request.headers.get('Authorization')
    response = send_request(endpoint, auth_header, payload=request.args)
    return jsonify(response.json())


@app.route('/v4/user/average')
def get_average_clicks_for_group_by_country():
    """
    Get average clicks (30 days) by country for user

    Sample request:
    curl -H "Authorization: <token>" http://localhost:5000/v4/user/average
    """
    user = get_user()
    user_default_guid = user.json['default_group_guid']

    bitlinks = get_bitlinks_by_group(user_default_guid)
    bitlinks_in_group = [links['link'] for links in bitlinks.json['links'] ]

    countries = {}
    for link in bitlinks_in_group:
        response = get_clicks_by_country('bit.ly', link.split('/')[-1])
        for group in response.json['metrics']:
            country = group['value']
            if country in countries:
                countries[country] += int(group['clicks'])
            else:
                countries[country] = int(group['clicks'])

    average_clicks = {k: v/30.0 for k, v in countries.items()}
    response = {
        'average_clicks': average_clicks,
        'group': f'{user_default_guid}'
    }
    return jsonify(response)


def send_request(endpoint, auth_header, payload={}):
    response = requests.get(endpoint, headers={'Authorization': auth_header}, params=payload)
    return response

if __name__ == '__main__':
    app.run()