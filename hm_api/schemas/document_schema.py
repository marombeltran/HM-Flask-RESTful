from marshmallow import Schema, fields, post_load
from hm_api.models.document import Document

class DocumentSchema(Schema):
    """
    Document Marshmallow Schema

    Marshmallow schema used for loading/dumping Documents
    """

    field_name = fields.String(allow_none=False)
    document_id = fields.Integer()

    @post_load
    def make_document(self, data, **kwargs):
        return Document(**data)