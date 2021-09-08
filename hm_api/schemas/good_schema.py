from marshmallow import Schema, fields, post_load
from hm_api.models.good import Good

class GoodSchema(Schema):
    """
    Good Marshmallow Schema

    Marshmallow schema used for loading/dumping Goods
    """

    name = fields.String(allow_none=False)
    good_id = fields.Integer()

    @post_load
    def make_good(self, data, **kwargs):
        return Good(**data)