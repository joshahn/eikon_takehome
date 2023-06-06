#/usr/bin/env python

from flask import Flask, jsonify, request

from src.db.database import initialize
from src.services import (get_user_id_from_email, 
                          get_total_experiments,
                          get_average_experiment_per_user,
                          get_most_commonly_used_compound,
                          run_etl
                         )

app = Flask(__name__)

@app.route('/api/v1/get_total_experiments', methods=['GET'])
def handle_get_total_experiments():
    user_id, message, status_code = extract_user_id(request.args)
    value = None
    if user_id > 0:
        total_exp = get_total_experiments(user_id)
        if total_exp >= 0:
            message = "Total experiments for user: {} is {}".format(user_id, total_exp)
            value = total_exp
            status_code = 200
        else:
            message: "Experiments not found for user ID: {}".format(user_id)
            status_code = 404
    app.logger.debug("{}: {}".format(status_code, message))
    return {"message": message, "value": value}, status_code


@app.route('/api/v1/get_average_experiment_per_user', methods=['GET'])
def handle_get_average_experiment_per_user():
    val = get_average_experiment_per_user()
    if val:
        resp = {
            "message": "Average experiment count per user is: {}".format(val),
            "value": val,
        }, 200
    else:
        resp = {"message": "No Content: No experiments ran"}, 204
    app.logger.debug(resp)
    return resp
    
@app.route('/api/v1/get_most_commonly_used_compound', methods=['GET'])
def handle_get_most_commonly_used_compound():
    user_id, message, status_code = extract_user_id(request.args)
    value = None
    if user_id > 0:
        most_common = get_most_commonly_used_compound(user_id)
        if most_common:
            message = "Most commonly used compound is {} for user {}".format(most_common, user_id)
            value = most_common
            status_code = 200
        else:
            message: "Experiments with compounds not found for user ID: {}".format(user_id)
            status_code = 404
    app.logger.debug("{}: {}".format(status_code, message))
    return {"message": message, "value": value}, status_code


# Your API that can be called to trigger your ETL process
@app.route('/api/v1/load', methods=['POST'])
def trigger_etl():
    success = run_etl()
    if success:
        resp = {"message": "ETL process started"}, 200
    else:
        resp = {"message": "There was error with the ETL process"}, 500 
    app.logger.debug(resp)
    return resp

@app.errorhandler(500)
def server_error(error):
    return {"message": "There is an internal server error"}, 500

def extract_user_id(args):
    user_id_val = 0
    status_code = 500
    message = ""
    user_id = args.get('user_id')
    email = args.get('email')
    if user_id:
        try:
            user_id_val = int(user_id)
            if not user_id_exists(user_id_val):
                message = "ERROR: ID not found: {}".format(user_id_val)
                status_code = 404
        except:
            message = "ERROR: Invalid id: {}".format(user_id)
            status_code = 400
    elif email:
        user_id_val = get_user_id_from_email(email)
        if user_id_val < 0:
            message = "ERROR: Multiple IDs for {}".format(email)
            status_code = 409
        elif user_id_val == 0:
            message = "ERROR: No ID found for {}".format(email)
            status_code = 404
        else:
            message = "DEBUG: Valid ID: {}".format(user_id_val)
            status_code = 200
    else:
        message = "ERROR: No id or email requested"
        status_code = 400
    return user_id_val, message, status_code
    

if __name__ == "__main__":
    # for debugging locally
    app.run(debug=True, host='0.0.0.0',port=5500)
    
    # for production
    # app.run(host='0.0.0.0', port=5000)