from app.database.sqlalchemy_extension import db
from app.database.models.user import UserModel


class DocumentsModel(db.Model):
    
    # Specifying table
    __tablename__ = "documents"
    __table_args__ = {"extend_existing": True}
    
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    application = db.relationship(
        UserModel,
        backref="documents",
        primaryjoin="DocumentsModel.application_id == ApplicationModel.id",
    )
    
    
    offer_letter = db.Column(db.Text())
    bank_statement = db.Column(db.Text())
    affiliation_letter = db.Column(db.Text())
    passbook = db.Column(db.Text())
    aadhar = db.Column(db.Text())
    fee_statement = db.Column(db.Text())
    scholarship_letter = db.Column(db.Text())
    
    def save_to_db(self) -> None:
        '''Add document details to database'''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        '''Deletes document details from the database.'''
        db.session.delete(self)
        db.session.commit()