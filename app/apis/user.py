from flask import request, Response
import requests
import json
from flask_restplus import Api, Resource, Namespace, fields, Model
import datetime
from firebase_admin import auth
import app.utils.messages as messages
from app.apis.validate.user_validate import validate_user_signup_data
from app.apis.models.user import add_models_to_namespace
from app.apis.models.user import *
from app.database.dao.user import UserDAO
from app.utils.view_decorator import token_required
import os

user_ns = Namespace('user', description='Functions related to user')
add_models_to_namespace(user_ns)

@user_ns.route('/register')
class UserRegister(Resource):
    
    @user_ns.response(201, "%s" % (
        {"message" : "User was created successfully. Please check your email to verify the account"}
    ))
    @user_ns.response(400, "%s" % (
        {"message" : "user already exists"}
    ))
    @user_ns.expect(register_user_model)
    def post(self):
        
        data = request.json
        
        not_valid = validate_user_signup_data(data)
        
        if not_valid:
            return not_valid
        
        result = UserDAO.create_user(data)
        return result
            

@user_ns.route('/login')
class UserSignIn(Resource):
    
    @user_ns.response(200, "User logged in successfully", login_response_model)
    @user_ns.response(400, "%s" % (
        {"message": "password is incorrect"}
    ))
    @user_ns.expect(login_user_model)
    def post(self):
        data = request.json
        email = data['email']
        password = data['password']
        
        login_response = UserDAO.authenticate(email, password)
        return login_response


@user_ns.route("/profile")
class ListMembers(Resource):
    
    @user_ns.doc(params={'authorization': {'in': 'header', 'description': 'An authorization token'}})
    @user_ns.response(200, "Profile Data", profile_body)
    @user_ns.response(400, "%s\n%s\n%s\n%s" % (
        messages.TOKEN_EXPIRED,
        messages.TOKEN_INVALID,
        messages.TOKEN_REVOKED,
        {"message": "cannot find account"}
    ),
    )
    @token_required
    def get(self):
        token = request.headers['authorization']
        
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        try:
            user = UserDAO.get_profile(uid)
        except Exception as e:
            return {"message": "cannot find account"}, 400
            
        return user, 200
    
    
    @user_ns.doc(params={'authorization': {'in': 'header', 'description': 'An authorization token'}})
    @user_ns.response(200, "%s" % (messages.PROFILE_UPDATE_SUCCESSFULLY))
    @user_ns.response(400, "%s\n%s\n%s\n%s" % (
        messages.TOKEN_EXPIRED,
        messages.TOKEN_INVALID,
        messages.TOKEN_REVOKED,
        {"message": "cannot find account"}
    ),
    )
    @user_ns.expect(update_profile_body)
    @token_required
    def put(self):
        data = request.json
        token = request.headers['authorization']
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        try:
            user = UserDAO.update_profile(uid, data)
            
        except Exception as e:
            return {"message": str(e)}, 400
        

        
# @user_ns.route('/resetpassword')
# class ResetPassword(Resource):
    
    
#     def get(self):
#         email = request.args.get('email')
#         try:
#             link = auth.generate_password_reset_link(email, action_code_settings=None)
#             ''' Send password reset email ''' 
#             # send_reset_link(email, link)
            
#         except Exception as e:
#             return {'message': e.args[0]}, 400
        
#         return messages.RESET_LINK_SENT, 200
    