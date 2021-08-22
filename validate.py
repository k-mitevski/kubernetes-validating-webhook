from flask import Flask, request, jsonify
from os import environ
import logging

webhook = Flask(__name__)

webhook.config['LABEL'] = environ.get('LABEL')

webhook.logger.setLevel(logging.INFO)


if "LABEL" not in environ:
    webhook.logger.error("Required environment variable for label isn't set. Exiting...")
    exit(1)


@webhook.route('/validate', methods=['POST'])
def validating_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")

    if request_info["request"]["object"]["metadata"]["labels"].get(webhook.config['LABEL']):
        webhook.logger.info(f'Object {request_info["request"]["object"]["kind"]}/{request_info["request"]["object"]["metadata"]["name"]} contains the required \"{webhook.config["LABEL"]}\" label. Allowing the request.')
        return admission_response(True, uid, f"{webhook.config['LABEL']} label exists.")
    else:
        webhook.logger.error(f'Object {request_info["request"]["object"]["kind"]}/{request_info["request"]["object"]["metadata"]["name"]} doesn\'t have the required \"{webhook.config["LABEL"]}\" label. Request rejected!')
        return admission_response(False, uid, f"The label \"{webhook.config['LABEL']}\" isn't set!")


def admission_response(allowed, uid, message):
    return jsonify({"apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response":
                        {"allowed": allowed,
                         "uid": uid,
                         "status": {"message": message}
                         }
                    })


if __name__ == '__main__':
    webhook.run(host='0.0.0.0',
                port=5000)
