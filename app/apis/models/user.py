from flask_restplus import fields, Model

def add_models_to_namespace(api_namespace):
    api_namespace.models[register_user_model.name] = register_user_model
    api_namespace.models[login_user_model.name] = login_user_model
    api_namespace.models[profile_body.name] = profile_body
    api_namespace.models[login_response_model.name] = login_response_model

login_user_model = Model(
    "login User Model",
    {
        "email": fields.String(required=True, description="Email of user"),
        "password": fields.String(required=True, description="password of user")
    }
)

login_response_model = Model(
    "Login Response User Model",
    {
        "kind": fields.String(required=True, description="Kind of user"),
        "localId": fields.String(required=True, description="Firebase id"),
        "displayName": fields.String(required=True, description="Name of user"),
        "idToken": fields.String(required=True, description="Token of user"),
        "registered": fields.String(required=True, description="Bool if the user is registered"),
        "refreshToken": fields.String(required=True, description="Refresh Token"),
        "expiresIn": fields.String(required=True, description="Expiratioon duratioon of token in seconds"),
        "role": fields.Integer(required=True, description="Role of user. 0-Donor, 1-Recipient, 2-Moderator")
    }
)

register_user_model = Model(
    "Register User Model",
    {
        "name": fields.String(required=True, description="Name of user"),
        "email": fields.String(required=True, description="Email of user"),
        "password": fields.String(required=True, description="password of user"),
        "role": fields.Integer(required=True, description="Role of a user")
    }
)

profile_body = Model(
    "Get profile of a user",
    {   
        "id": fields.String(required=True, description="id of user"),
        "firebase_id": fields.String(required=True, description="firebase_id of user"),
        
        "name": fields.String(required=True, description="The name of the user"),
        "email": fields.String(
            required=True, description="Email of user"
        ),
        "is_email_verified": fields.Boolean(required=False, description="If the user is verified or not"),
        "profile_image": fields.String(
            required=False, description="Profile Image Link"
        ),
        "occupation": fields.String(
            required=False, description="Occupation of User"
        ),
        "is_donor": fields.Boolean(required=True, description="If the owner is donor"
        ),
        "is_recipient": fields.Boolean(required=True, description="If the owner is recipient"
        ),
        "is_moderator": fields.Boolean(required=True, description="If the owner is mooderator"
        )
    }
)
