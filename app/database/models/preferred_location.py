from app.database.sqlalchemy_extension import db
from app.database.models.user import UserModel

class PreferredLocationModel(db.Model):

    # Specifying table
    __tablename__ = "preferred_location"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(
        UserModel,
        backref="preferred_location",
        primaryjoin="PreferredLocationModel.user_id == UserModel.id",
    )
    state = db.Column(db.String(50))
    district = db.Column(db.String(50))
    sub_district = db.Column(db.String(50))
    area = db.Column(db.String(50))
    
    def __init__(self, user_id, state, district, sub_district, area):
        self.user_id = user_id
        self.state = state
        self.district = district
        self.sub_district = sub_district
        self.area = area
    
    def save_to_db(self) -> None:
        """Saves the model to the database."""
        db.session.add(self)
        db.session.commit()