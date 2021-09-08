import logging
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from flask import Flask
from flask_restful import Api

from hm_api.constants import PROJECT_ROOT, HM_DATABASE
from hm_api.database import db
from hm_api.resources.documents_resource import DocumentsResource, DOCUMENTS_ENDPOINT

# importing goods resource
from hm_api.resources.goods_resource import GoodsResource, GOODS_ENDPOINT

def create_app(db_location):
    """
    Function that creates our Flask application.
    This function creates the Flask app, Flask-Restful API,
    and Flask-SQLAlchemy connection
    :param db_location: Connection string to the database
    :return: Initialized Flask app
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("hm_api.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_location
    db.init_app(app)

    api = Api(app)
    api.add_resource(DocumentsResource, DOCUMENTS_ENDPOINT, f"{DOCUMENTS_ENDPOINT}/<id>")
    api.add_resource(GoodsResource, GOODS_ENDPOINT, f"{GOODS_ENDPOINT}/<id>")

    return app

if __name__ == "__main__":
    app = create_app(f"sqlite:////{PROJECT_ROOT}/{HM_DATABASE}")
    app.run(debug=True)
