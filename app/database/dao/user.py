from flask import request, Response
from app.database.models.user import UserModel
import requests
import json
from app.utils import messages
from firebase_admin import auth
from app.apis.validate.user_validate import validate_user_signup_data
from typing import Dict
from os import environ


class UserDAO:
    """Data Access Object for User"""

    @staticmethod
    def create_user(data: Dict[str, str]):
        """Creates a new user"""
        
        name = data['name']
        email = data['email']
        password = data['password']
        role = data['role']

        
        try:    
            user = auth.create_user(
                email=email,
                email_verified=False,
                password=password,
                display_name=name,
                disabled=False
                )
            
            link = auth.generate_email_verification_link(email, action_code_settings=None)
            ''' To implement, send verification link usingg # send_verification_link(email,link) '''
            
        except Exception as e:
            return {"message": str(e)}, 400
        
        try:    
            firebase_details = auth.get_user_by_email(email)
            uid = firebase_details.uid
            firebase_email = firebase_details.email
            user = UserModel(uid, name, firebase_email, password, role)
            user.save_to_db()
        except Exception as e:
            print(e)
        
        
        

        return {"verify_link": link,
                "message" : "User was created successfully. Please check your email to verify the account"
                }, 201
        
    @staticmethod
    def authenticate(email: str, password: str):
        """ User login process"""

        try:
            user = auth.get_user_by_email(email)
            if user.email_verified != True:
                return {"message": "Email is not verified, Please verify email first"}, 400
            
        except Exception as e:
            return {"message": e.args[0]}, 400
        
        
        json_string = {"email":email,"password":password,"returnSecureToken":True}
        API_KEY = environ.get('API_KEY')
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + API_KEY
        res = requests.post(url, data=json_string)
        json_res = json.loads(res.text)
        
        
        if "error" in json_res.keys():
            error_message = json_res["error"]
            if error_message["message"] == "INVALID_PASSWORD":
                return {"message": "Password is incorrect"}, 401
            else:
                return { "message": error_message["message"]}, 401    
        
        
        if "idToken" in json_res.keys():
            '''Sample response of role i.e. 0'''
            json_res["role"] = 3
            
        
        return json_res, 200
    
    @staticmethod
    def list_all_users():
        user_list = UserModel.query.all()
        list_of_users = [
            user.json()
            for user in user_list
        ]
        return list_of_users, 200
    
    @staticmethod
    def get_profile(firebase_id: str):
        user_profile = UserModel.find_by_firebase_id(firebase_id)
        return user_profile.json()