import re
from typing import Type

from flask import Blueprint
from flask import current_app
from flask_restful import Api, Resource, abort
from flask_sqlalchemy.model import Model
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.auth import admin_required


def create_blueprint_with_api(print_name, url_prefix=None):
    blueprint = Blueprint(print_name, __name__, url_prefix="/" + url_prefix)
    api = Api(blueprint)
    return blueprint, api


class AdminResource(Resource):
    method_decorators = [admin_required()]


class ORMBaseClass:
    table: Type[Model]
    args: dict

    def __init__(self):
        self.engine = create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"])
        super().__init__()

    def make_select_query(self, **kwargs):
        with Session(self.engine, expire_on_commit=False) as session:
            if not kwargs:
                return session.query(self.table).all()
            return session.query(self.table).filter_by(**kwargs).all()

    def make_create_query(self):
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                new_instance = self.table(**self.args)
                session.add(new_instance)
                session.commit()
                return new_instance
        except IntegrityError as ex:
            list_args = {index: err for index, err in zip(range(len(ex.args)), ex.args)}
            abort(400, description="bad request", errs=list_args)

    def make_update_query(self, instance, new_params: dict):
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                for param in new_params.items():
                    setattr(instance, param[0], param[1])
                session.add(instance)
                session.commit()
                return instance
        except IntegrityError as ex:
            list_args = {index: err for index, err in zip(range(len(ex.args)), ex.args)}
            abort(400, description="bad request", errs=list_args)

    def make_delete_query(self, instance_id):
        try:
            with Session(self.engine, expire_on_commit=False) as session:
                deleted_objects = session.query(self.table).filter(self.table.id == instance_id).delete()
                session.commit()
                return deleted_objects
        except IntegrityError as ex:
            list_args = {index: err for index, err in zip(range(len(ex.args)), ex.args)}
            abort(400, description="bad request", errs=list_args)


class CRUDResource(ORMBaseClass):
    def get(self):
        return self.make_select_query()

    def post(self):
        self.load_parser()
        return [self.make_create_query()], 201


class CRUDRetrieveResource(ORMBaseClass):

    def get(self, instance_id):
        response = self.make_select_query(id=instance_id)
        if len(response) == 1:
            return response[0]
        else:
            abort(404, description=f"{self.table.__name__} not found")

    def put(self, instance_id):
        instance = self.make_select_query(id=instance_id)
        if not instance:
            abort(404, description=f"{self.table.__name__} not found")
        self.load_parser()
        return self.make_update_query(instance[0], self.args)

    def delete(self, instance_id):
        output = self.make_delete_query(instance_id)
        if not output:
            abort(404, description=f"{self.table.__name__} not found")
        return f"{self.table.__name__} {instance_id} was deleted", 204


def mail(value):
    if re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", value):
        return value
    else:
        raise ValueError("wrong mail format")
