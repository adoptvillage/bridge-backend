from flask import request, Response
from app.database.models.user import UserModel
from app.database.models.application import ApplicationModel
from app.database.models.documents import DocumentsModel
from app.database.models.invites import InvitesModel
from app.database.models.institution import InstitutionModel
import requests
import json
from app.utils import messages
from firebase_admin import auth
from app.apis.validate.application_validate import validate_application_submit_data
from typing import Dict
from os import environ
from app.database.sqlalchemy_extension import db
from app.database.models.preferred_location import PreferredLocationModel
from app.utils.email_utils import send_invite_mod_email
import random


class ApplicationDAO:
    """Data Access Object for Application"""

    @staticmethod
    def create_application(firebase_id: str, data: Dict[str, str]):
        
        user = UserModel.find_by_firebase_id(firebase_id)
        user_application = user.application
        
        if user.is_recipient == False:
            return {"message": "This user cannot submit application"}, 403
        
        # data = request.json
        ''' Personal information '''
        applicant_first_name = data["applicant_first_name"]
        applicant_last_name = data["applicant_last_name"]
        contact_number = data["contact_number"]
        aadhaar_number = data["aadhaar_number"]
        state = data["state"]
        district = data["district"]
        sub_district = data["sub_district"]
        area = data["area"]
        
        
        ''' Institution details '''
        institute_name = data["institute_name"]
        institute_state = data["institute_state"]
        institute_district = data["institute_district"]
        institution_affiliation_code = data["institution_affiliation_code"]
        year_or_semester = data["year_or_semester"]
        course_name = data["course_name"]
        amount = data["amount"]

        ''' Documents details '''
        offer_letter = data["offer_letter"]
        fee_structure = data["fee_structure"]
        bank_statement = data["bank_statement"]
        
        if user_application:
            if any(application.is_open == True for application in user_application):
                    return {"message": "Application already in progress."}, 400
            
            '''Use this is list of application'''
            # for application in user_application:
            #     end_date = application.expiration_date
            #     format_str = '%Y-%m-%d' # The format
            #     expiration_date = datetime.strptime(end_date, format_str) # Expiration date string to date object
            #     if expiration_date < date.today() and application.is_open:
            
        
        
        application = ApplicationModel(applicant_first_name, applicant_last_name, contact_number, 
                                       aadhaar_number, state, district, sub_district, 
                                       area, year_or_semester, course_name, amount)
        application.applicant = user
        
        
        documents = DocumentsModel(offer_letter, fee_structure, bank_statement)
        documents.application = application
        documents.save_to_db()
        
        application.insittute = InstitutionModel(institute_name, institute_state, institute_district, institution_affiliation_code)
        application.save_to_db()
        # institute = InstitutionModel(institute_name, institute_state, institute_district, institution_affiliation_code)
        # institute.save_to_db()
        
        
        # already_exist_application = ApplicationModel.query.filter_by(name='reza')
        
        return {"message": "Success! Application submitted"}, 200
        
    @staticmethod
    def accept_application(firebase_id: str, data: Dict[str, str]):
        try:
            user = UserModel.find_by_firebase_id(firebase_id)
        except Exception as e:
            return messages.CANNOT_FIND_USER, 400
        
        if user.is_donor == False:
            return {"message": "This user cannot accept application"}, 403
        
        application_id = data["application_id"]
        donating_full_amount = data["donating_full_amount"]
        amount = data["amount"]
        moderator_email = data["moderator_email"]
        
        application = ApplicationModel.find_by_id(application_id)
        
        if application in user.donating:
            return {"message": "Already donating to this application"}, 409
        
        if application.remaining_amount == 0:
            return {"message": "No further amount needed"}, 409
        
        if donating_full_amount:
            application.remaining_amount = 0
        else:
            application.remaining_amount = application.remaining_amount - amount
        
        application.donor.append(user)
        application.no_of_donors = application.no_of_donors + 1
        
        
        ''' Find existing moderator '''
        moderator = UserModel.find_by_email(moderator_email.lower())
        
        if moderator:
            if moderator.is_moderator:
                application.moderator.append(moderator)
                application.moderator_email = moderator.email
                application.save_to_db()
                if moderator.firebase_id == "":
                    return {"message": "Application accepted. Moderator is already invited, please ask moderator to register by code given earlier."}, 200
                else:
                    return {"message": "Application accepted"}, 200
            else:
                role = "donor" if moderator.is_donor else "recipient" if moderator.is_recipient else "moderator"
                return {"message": f"Invited Moderator is register as a {role}"}, 409
        else:
            temp_mod_user = UserModel("","",moderator_email.lower(), "",2)
            temp_mod_user.save_to_db()
            application.moderator.append(temp_mod_user)
            application.save_to_db()
            ''' Send invite to moderator '''
            invite_code = random.randint(111111,999999)
            invite = InvitesModel(user, temp_mod_user, moderator_email, invite_code)
            invite.save_to_db()
            send_invite_mod_email(user.name, invite_code, moderator_email)
            
            return {"message": "Application accepted. Waiting for moderator to accept the inivite"}, 200
            
        
        return {"message": "Application accepted"}, 200
    
    
    @staticmethod
    def list_application():
        applications = ApplicationModel.query.all()
        apps = list()
        for app in applications:
            apps.append(app.json())
        return {"message": apps}, 200
            
        