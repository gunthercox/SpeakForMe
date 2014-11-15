from flask.views import View


class Api(View):

    def dispatch_request(self):
        from flask import request, jsonify

        data = {}

        return jsonify(data)
