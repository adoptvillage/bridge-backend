from flask import request, Response
import requests
import json
from flask_restplus import Api, Resource, Namespace, fields, Model
import datetime
from firebase_admin import auth
import app.utils.messages as messages
from app.apis.validate.user_validate import validate_user_signup_data
from app.apis.models.user import add_models_to_namespace
from app.apis.models.user import login_user_model, register_user_model
import os

user_ns = Namespace('user', description='Functions related to user')
add_models_to_namespace(user_ns)

@user_ns.route('/register')
class UserRegister(Resource):
    
    @user_ns.expect(register_user_model)
    def post(self):
        
        data = request.json
        not_valid = validate_user_signup_data(data)
        
        if not_valid:
            return not_valid
        
        name = data['name']
        email = data['email']
        password = data['password']
        role = data['role']
        role_name = ""
        
        if role == 0:
            role_name = "donor"
        elif role == 1:
            role_name = "recipient"
        elif role == 2:
            role_name = "moderator" 

         
        try:    
            user = auth.create_user(
                email=email,
                email_verified=False,
                password=password,
                display_name=name,
                disabled=False
                )
            
            link = auth.generate_email_verification_link(email, action_code_settings=None)
            print(link)
            ''' To implement, send verification link usingg # send_verification_link(email,link) '''
            
        except Exception as e:
            return {"message": str(e)}, 400
        
        return {"verify_link": link,
                "message" : "Please check your email to verify the account"
                }, 200
            

@user_ns.route('/login')
class UserSignIn(Resource):
    
    @user_ns.expect(login_user_model)
    def post(self):
        data = request.json
        email = data['email']
        password = data['password']
        
        try:
            user = auth.get_user_by_email(email)
            if user.email_verified != True:
                return {"message": "Email is not verified, Please verify email first"}, 400
        
        except Exception as e:
            return {"message": e.args[0]}, 400
        
        
        json_string = {"email":email,"password":password,"returnSecureToken":True}
        API_KEY = os.getenv('API_KEY')
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + API_KEY
        res = requests.post(url, data=json_string)

        json_res = json.loads(res.text)
        if "idToken" in json_res.keys():
            json_res["role"] = 0
        
        
        
        return json_res, 200



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
    