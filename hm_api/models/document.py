from hm_api.database import db

class Document(db.Model):
    """
    Document Flask-SQLAlchemy Model

    Represents objects contained in the Document table
    """

    __tablename__ = "document"

    document_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return (
            f"**Document** "
            f"Field Name: {self.field_name} "
            f"**Document** "
        )