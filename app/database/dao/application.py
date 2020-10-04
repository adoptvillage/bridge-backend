from flask import request, Response
from app.database.models.user import UserModel
from app.database.models.application import ApplicationModel
from app.database.models.documents import DocumentsModel
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


class ApplicationDAO:
    """Data Access Object for Application"""

    @staticmethod
    def create_application(firebase_id: str, data: Dict[str, str]):
        
        user = UserModel.find_by_firebase_id(firebase_id)
        user_application = user.application
        
        if user.is_recipient == False:
            return {"message": "This user cannot submit application"}, 400
        
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
        application.save_to_db()
        
        
        documents = DocumentsModel(offer_letter, fee_structure, bank_statement)
        documents.application = application
        documents.save_to_db()
        
        institute = InstitutionModel(institute_name, institute_state, institute_district, institution_affiliation_code)
        institute.save_to_db()
        
        
        # already_exist_application = ApplicationModel.query.filter_by(name='reza')
        
        return {"message": "Success! Application submitted"}, 200
        
        
        