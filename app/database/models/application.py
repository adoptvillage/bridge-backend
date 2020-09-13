from app.database.sqlalchemy_extension import db
from app.database.models.user import UserModel
from app.database.models.application_donor import application_donor


class ApplicationModel(db.Model):
    
    # Specifying table
    __tablename__ = "application"
    __table_args__ = {"extend_existing": True}
    
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    applicant = db.relationship(
        UserModel,
        backref="application",
        primaryjoin="ApplicationModel.applicant_id == UserModel.id",
    )
    # institution_id = 
    donor = db.relationship('UserModel', secondary=application_donor, backref=db.backref('donating', lazy = 'dynamic')) 
    # moderator_id = 
    is_open = db.Column(db.Boolean)
    verified = db.Column(db.Boolean)
    submission_date = db.Column(db.Float)
    expiration_date = db.Column(db.Float)
    amount = db.Column(db.String(15))
    remaining_amount = db.Column(db.String(15))
    no_of_donors = db.Column(db.Integer)
    # document_id = 
    
    
    def save_to_db(self) -> None:
        '''Add application to database'''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        '''Deletes application from the database.'''
        db.session.delete(self)
        db.session.commit()
    