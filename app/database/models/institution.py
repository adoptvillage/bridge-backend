from app.database.sqlalchemy_extension import db


class InstitutionModel(db.Model):
    
    # Specifying table
    __tablename__ = "institution"
    __table_args__ = {"extend_existing": True}
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    district = db.Column(db.String(50))
    state = db.Column(db.String(50))
    affiliation_code = db.Column(db.String(10))
    active_applicant = db.Column(db.Integer)
    total_applicant = db.Column(db.Integer)
    
    
    def __init__(self, name, state, district, affiliation_code):
        self.name = name
        self.state = state
        self.district = district
        self.affiliation_code = affiliation_code
    
    def save_to_db(self) -> None:
        '''Add institution to database'''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        '''Deletes institution from the database.'''
        db.session.delete(self)
        db.session.commit()
    