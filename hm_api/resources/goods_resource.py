import json
import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from hm_api.database import db
from hm_api.models.good import Good
from hm_api.schemas.good_schema import GoodSchema

GOODS_ENDPOINT = "/api/goods"
logger = logging.getLogger(__name__)

class GoodsResource(Resource):
    def get(self, id=None):
        """
        GoodsResource GET method. Retrieves all documment found in the HM
        Stats database, unless the id path parameter is provided. If this id
        is provided then the good with the associated good_id is retrieved.
        :param id: Good ID to retrieve, this path parameter is optional
        :return: Good, 200 HTTP status code
        """
        if not id:
            index = request.args.get("index")
            logger.info(
                f"Retrieving all goods, optionally filtered by index={index}"
            )

            return self._get_all_goods(index), 200
        
        logger.info(f"Retrieving good by id {id}")

        try:
            return self._get_good_by_id(id), 200
        except NoResultFound:
            abort(404, message="Good no found")
    
    def _get_good_by_id(self, good_id):
        good = Good.query.filter_by(good_id=good_id).first()
        good_json = GoodSchema().dump(good)

        if not good_json:
            raise NoResultFound()

        logger.info(f"good retrieved from database {good_json}")
        return good_json
    
    def _get_all_goods(self, index):
        if index:
            goods = Good.query.filter_by(index=index).all()
        else:
            goods = Good.query.all()

        goods_json = [GoodSchema().dump(good) for good in goods]

        logger.info("goods successfully retrieved.")
        return goods_json
    
    def post(self):
        """
        GoodResorce POST method. Adds a new Good to the database.
        :return: Good.good_id, 201 HTTP status code.
        """
        req_json = request.get_json()

        goods_added = [];
        for _good in req_json:
            good = GoodSchema().load(_good)
            
            try:
                db.session.add(good)
                db.session.commit()
            except IntegrityError as e:
                logger.warning(
                    f"Integrity Error, this tuple is already in the database. Error: {e}"
                )

                abort(500, message="Unexpected Error!")
            else:
                goods_added.append(good.good_id)

        return goods_added, 201
