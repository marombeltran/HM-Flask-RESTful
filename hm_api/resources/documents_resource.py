import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from hm_api.database import db
from hm_api.models.document import Document
from hm_api.schemas.document_schema import DocumentSchema

DOCUMENTS_ENDPOINT = "/api/documents"
logger = logging.getLogger(__name__)

class DocumentsResource(Resource):
    def get(self, id=None):
        """
        DocumentsResource GET method. Retrieves all documents found in the HM
        Stats database, unless the id path parameter is provided. If this id
        is provided then the document with the associated document_id is retrieved.
        :param id: Document ID to retrieve, this path parameter is optional
        :return: Document, 200 HTTP status code
        """
        if not id:
            position = request.args.get("position")
            logger.info(
                f"Retrieving all documents, optionally filtered by position={position}"
            )

            return self._get_all_documents(position), 200

        logger.info(f"Retrieving document by id {id}")

        try:
            return self._get_document_by_id(id), 200
        except NoResultFound:
            abort(404, message="Document not found")

    def _get_document_by_id(self, document_id):
        document = Document.query.filter_by(document_id=document_id).first()
        document_json = DocumentSchema().dump(document)

        if not document_json:
            raise NoResultFound()

        logger.info(f"document retrieved from database {document_json}")
        return document_json

    def _get_all_documents(self, position):
        if position:
            documents = Document.query.filter_by(position=position).all()
        else:
            documents = Document.query.all()

        documents_json = [DocumentSchema().dump(document) for document in documents]

        logger.info("documents successfully retrieved.")
        return documents_json

    def post(self):
        """
        DocumentResource POST method. Adds a new Document to the database.
        :return: Document.document_id, 201 HTTP status code.
        """
        document = DocumentSchema().load(request.get_json())

        try:
            db.session.add(document)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this tuple is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return document.document_id, 201