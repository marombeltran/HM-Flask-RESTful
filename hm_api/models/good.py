from hm_api.database import db

class Good(db.Model):
    """
    Good Flask-SQLAlchemy Model

    Represent objects contained in the Goods table
    """

    __tablename__ = "goods"

    name = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    good_id = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return (
            f"**Good** "
            f"Field Name: {self.name} "
            f"Field ID Good: {self.good_id} "
            f"**Good** "
        )
