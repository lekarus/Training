import re
from typing import List, Tuple, Type

from auth.auth import admin_required
from database import db
from flask import Blueprint
from flask_restful import abort, Api, Resource
from flask_restful_swagger import swagger
from flask_sqlalchemy.model import Model
from flask_sqlalchemy.session import Session
from sqlalchemy.exc import IntegrityError


def create_blueprint_with_api(print_name: str, url_prefix: str = None) -> Tuple[Blueprint, Api]:
    """return blueprint and api instances"""
    blueprint = Blueprint(print_name, __name__, url_prefix=("/" + url_prefix) if url_prefix else None)
    api = swagger.docs(
        Api(blueprint),
        apiVersion='0.1',
        api_spec_url="/swagger",
        description=f"Auto generated API docs by flask-restful-swagger for {print_name}",
    )
    return blueprint, api


class AdminResource(Resource):
    method_decorators = [admin_required()]


class ORMBaseClass:
    """Custom class to work with SQLAlchemy ORM"""
    table: Type[Model]
    args: dict

    def __init__(self, table: Type[Model] = None):
        if table is not None:
            self.table = table

    def make_select_query(self, **kwargs) -> List[Model]:
        with Session(db, expire_on_commit=False) as session:
            if not kwargs:
                return session.query(self.table).all()
            return session.query(self.table).filter_by(**kwargs).all()

    def make_create_query(self, **kwargs) -> Model:
        try:
            with Session(db, expire_on_commit=False) as session:
                new_instance = self.table(**kwargs)
                session.add(new_instance)
                session.commit()
                return new_instance
        except IntegrityError as ex:
            list_args = {index: err for index, err in zip(range(len(ex.args)), ex.args)}
            abort(400, description="bad request", errs=list_args)

    def make_update_query(self, instance: Model, new_params: dict) -> Type[Model]:
        try:
            with Session(db, expire_on_commit=False) as session:
                for param in new_params.items():
                    setattr(instance, param[0], param[1])
                session.add(instance)
                session.commit()
                return instance
        except IntegrityError as ex:
            list_args = {index: err for index, err in zip(range(len(ex.args)), ex.args)}
            abort(400, description="bad request", errs=list_args)

    def make_delete_query(self, instance_id: int):
        try:
            with Session(db, expire_on_commit=False) as session:
                deleted_objects = session.query(self.table).filter_by(id=instance_id).delete()
                session.commit()
                return deleted_objects
        except IntegrityError as ex:
            list_args = {index: err for index, err in zip(range(len(ex.args)), ex.args)}
            abort(400, description="bad request", errs=list_args)


class CRUDResource(ORMBaseClass):
    """abstract class for GET and POST method"""

    @swagger.operation(
        notes='List method of this table',
        responseMessages=[
            {
                "code": 200,
                "message": "[List of objects]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 403,
                "message": "Admins only!",
            },
        ],
    )
    def get(self) -> List[Model]:
        return self.make_select_query()

    @swagger.operation(
        notes='Create method of this table',
        responseMessages=[
            {
                "code": 201,
                "message": "[Object]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 403,
                "message": "Admins only!",
            },
            {
                "code": 400,
                "message": "[Bad Request]",
            },
        ],
    )
    def post(self) -> Tuple[List[Model], int]:
        self.load_parser()
        return [self.make_create_query(**self.args)], 201

    def load_parser(self):
        abort("parser not implemented")


class CRUDRetrieveResource(ORMBaseClass):
    """abstract class for Retrieve, PUT and DELETE method"""
    @swagger.operation(
        notes='Get method of this table',
        responseMessages=[
            {
                "code": 200,
                "message": "[Object]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 403,
                "message": "Admins only!",
            },
            {
                "code": 404,
                "message": "[Object] not found",
            },
        ],
    )
    def get(self, instance_id: str) -> Model:
        response = self.make_select_query(id=instance_id)
        if len(response) == 1:
            return response[0]
        abort(404, description=f"{self.table.__name__} not found")  # noqa: R503

    @swagger.operation(
        notes='Update method of this table',
        responseMessages=[
            {
                "code": 200,
                "message": "[Object]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 403,
                "message": "Admins only!",
            },
            {
                "code": 400,
                "message": "[Bad Request]",
            },
            {
                "code": 404,
                "message": "[Object] not found",
            },
        ],
    )
    def put(self, instance_id) -> Type[Model]:
        instance = self.make_select_query(id=instance_id)
        if not instance:
            abort(404, description=f"{self.table.__name__} not found")
        self.load_parser()
        return self.make_update_query(instance[0], self.args)

    @swagger.operation(
        notes='Delete method of this table',
        responseMessages=[
            {
                "code": 204,
                "message": "[Object] was deleted",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 403,
                "message": "Admins only!",
            },
            {
                "code": 404,
                "message": "[Object] not found",
            },
        ],
    )
    def delete(self, instance_id: int) -> Tuple[str, int]:
        output = self.make_delete_query(instance_id)
        if not output:
            abort(404, description=f"{self.table.__name__} not found")
        return f"{self.table.__name__} {instance_id} was deleted", 204

    def load_parser(self):
        abort("parser not implemented")


def mail_checker(value: str):
    """validator for email"""
    if re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", value):
        return value
    raise ValueError("wrong mail format")
