from flask_restplus import fields, Model

def add_models_to_namespace(api_namespace):
    api_namespace.models[register_user_model.name] = register_user_model
    api_namespace.models[login_user_model.name] = login_user_model

login_user_model = Model(
    "login User Model",
    {
        "email": fields.String(required=True, description="Email of user"),
        "password": fields.String(required=True, description="password of user")
    }
)

register_user_model = Model(
    "Register User Model",
    {
        "name": fields.String(required=True, description="Name of user"),
        "email": fields.String(required=True, description="Email of user"),
        "password": fields.String(required=True, description="password of user")
    }
)
