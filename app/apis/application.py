from flask import request, Response
import requests
import json
from flask_restplus import Api, Resource, Namespace, fields, Model
import datetime
from firebase_admin import auth
import app.utils.messages as messages
from app.apis.models.application import add_models_to_namespace
from app.apis.models.application import *
from app.apis.validate.application_validate import validate_application_submit_data
from app.database.dao.application import ApplicationDAO
from app.utils.view_decorator import token_required

app_ns = Namespace('application', description='Functions related to application submission')
add_models_to_namespace(app_ns)

@app_ns.route('/submit')
class SubmitApplication(Resource):
    
    @app_ns.doc(params={'authorization': {'in': 'header', 'description': 'An authorization token'}})
    @token_required
    @app_ns.expect(application_submit_model)
    def post(self):
        data = request.json
        
        token = request.headers['authorization']
        
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        not_valid = validate_application_submit_data(data)
        
        if not_valid:
            return not_valid
        
        submit_application_response = ApplicationDAO.create_application(uid, data)
        
        return submit_application_response