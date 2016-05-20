#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import datetime
import uuid

import sqlalchemy as sa

from a10_neutron_lbaas.db import api as db_api

Base = db_api.get_base()


def _uuid_str():
    return str(uuid.uuid4())


def _get_date():
    return datetime.datetime.now()


class A10BaseMixin(object):

    @classmethod
    def query(cls, db_session=None):
        db = db_session or db_api.get_session()
        return db.query(cls)

    @classmethod
    def find_all_by(cls, db_session=None, **kwargs):
        return cls.query(db_session).filter_by(**kwargs)

    @classmethod
    def find_by(cls, db_session=None, **kwargs):
        return cls.find_all_by(db_session, **kwargs).one_or_none()

    @classmethod
    def find_by_attribute(cls, attribute_name, attribute, db_session=None):
        return cls.query(db_session).filter(
            getattr(cls, attribute_name) == attribute).one_or_none()

    @classmethod
    def find_all(cls, db_session=None):
        return cls.query(db_session).all()

    @classmethod
    def create_and_save(cls, db_session=None, **kwargs):
        db = db_session or db_api.get_session()
        m = cls(**kwargs)
        db.add(m)
        db.commit()

    id = sa.Column(sa.String(36), primary_key=True, nullable=False, default=_uuid_str)
    created_at = sa.Column(sa.DateTime, default=_get_date)
    updated_at = sa.Column(sa.DateTime, default=_get_date, onupdate=_get_date)
