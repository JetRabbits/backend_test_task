# coding=utf-8
import uuid

from flask import g
from sqlalchemy import text
from werkzeug.exceptions import BadRequest

from app.classes.handling.storage import StorageBadRequest
from app.classes.node import Node, NodeReader, NodeWriter, NODE_TYPE_FILE, NODE_DIRECTORY_TYPES
from app.constants import FILE_PROVIDER_MAPPING, GET_NODE_IDS_BY_PATH, SERVER_DATA_PROVIDER_ID
from app.functions import REST_GUIDE
from app.functions.base.date import now
from app.functions.base.json import empty_json_object, empty_json_array, to_json_array
from app.functions.base.uuid import generate_uuid
from app.functions.crud.bulk_post import merge_entity
from app.functions.io.response import success, make_json_response
from app.functions.utils.context import session_scope
from app.functions.utils.decorator import auth_required
from app.functions.utils.file import get_file_extension
from app.functions.utils.query import select
from app.storages import DataStorageFactory


@auth_required('get_by_id', '/rest/v1/nodes')
def search(body):
    # TODO: Implement search functions
    return make_json_response(empty_json_array('nodes'), 200)


@auth_required('get_by_id', '/rest/v1/nodes')
def get_node_by_id(id, token):
    # TODO: Implement get by id function
    return make_json_response(empty_json_array('nodes'), 200)


@auth_required('remove', '/rest/v1/nodes')
def delete_node(id, token):
    # TODO: Implement search functions
    return success('REMOVE /nodes', 200, 'Success', REST_GUIDE + 'nodes.post_nodes')


@auth_required('get_all', '/rest/v1/nodes')
def get_nodes(token):
    with session_scope() as session:
        nodes = session.query(Node).all()
        nodes_json = to_json_array(nodes)
        enrich_nodes_json(nodes_json)
    json = empty_json_array('nodes')
    json['nodes'] = nodes_json
    return make_json_response(json, 200)


@auth_required('post', '/rest/v1/nodes')
def post_nodes(body):
    with session_scope() as session:
        for node_json in body['nodes']:
            post_node(body, node_json, session)

    return success('POST /nodes', 200, 'Success', REST_GUIDE + 'nodes.post_nodes')


@auth_required('post', '/rest/v1/nodes')
def upload(token, id, file, body=None):
    check_write_grant(uuid.UUID(id))
    with session_scope() as session:
        node_db = session.query(Node).filter_by(id=id)
        node = node_db.first()
        if node is None:
            raise_node_not_found(id)
        if node.node_type in NODE_DIRECTORY_TYPES:
            raise StorageBadRequest('unable to upload directory resource')

        node.size_in_bytes = get_file_size(file)
        node.name = file.filename
        session.add(node)
        provider = FILE_PROVIDER_MAPPING[node.provider_id]
        path = get_node_paths(node.id).get(node.id)
        data_storage = DataStorageFactory.create_storage({'provider': provider})
    return data_storage.upload(path, file)


def download(id):
    path, provider = get_node_path_by_id(id)
    data_storage = DataStorageFactory.create_storage({'provider': provider})
    return data_storage.download(path)


def post_node(body, node_json, session):
    body['instance'] = ''
    setup_node(node_json)
    parent_id = node_json.get('parent_id')
    if parent_id is not None:
        check_write_grant(uuid.UUID(parent_id))
    readers = None
    if "readers" in node_json:
        readers = node_json.pop('readers')
    writers = None
    if "writers" in node_json:
        writers = node_json.pop('writers')
    merge_entity(Node, node_json, body, session)
    node_instance = body['instance']
    if readers is not None:
        post_node_users(session, NodeReader, body, readers, 'reader_id', node_json['id'], node_instance)
    if writers is not None:
        post_node_users(session, NodeWriter, body, writers, 'writer_id', node_json['id'], node_instance)


def setup_node(json):
    if 'node_type' not in json:
        raise BadRequest("'node_type' must be specified")
    if json['node_type'] == NODE_TYPE_FILE and '.' not in json.get('name'):
        raise StorageBadRequest('please specify correct file name')
    if 'parent_id' not in json:
        json['parent_id'] = None
    if 'provider_id' not in json:
        json['provider_id'] = SERVER_DATA_PROVIDER_ID
    if 'description' not in json:
        json['description'] = ''
    if 'id' not in json:
        json['id'] = generate_uuid()
    with session_scope() as session:
        prepare_default_rights(json, session)
    return json


def prepare_default_rights(json, session):
    is_new_node = \
        'id' not in json or session.query(Node).filter_by(id=uuid.UUID(json['id'])).first() is None
    if is_new_node:
        if 'created_by' not in json:
            json['created_by'] = g.user_id
        if 'created_when' not in json:
            json['created_when'] = now()
        if 'owner_id' not in json:
            json['owner_id'] = g.user_id
    else:
        if 'modified_by' not in json:
            json['modified_by'] = g.user_id
        if 'modified_when' not in json:
            json['modified_when'] = now()


def get_nodes_users(clazz, user_key, node_ids, session):
    node_users = session.query(clazz).filter(clazz.node_id.in_(node_ids)).all()
    node_users_map = {}
    for node_user in node_users:
        node_id = node_user.node_id
        user_id = getattr(node_user, user_key)
        user_ids = node_users_map.get(node_id, [])
        user_ids.append(user_id)
        node_users_map[node_id] = user_ids
    return node_users_map


def get_file_size(file):
    import os
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0, os.SEEK_SET)
    return file_size


def post_node_users(session, clazz, body, users, user_key, node_id, node_instance):
    new_users = []
    if users is not None:
        for user_id in users:
            body['instance'] = node_instance
            user_json = empty_json_object()
            user_json['node_id'] = node_id
            user_json[user_key] = user_id
            user_db = session.query(clazz).filter_by(**{'node_id': node_id, user_key: user_id})
            merge_entity(clazz, user_json, body, session, 'node_id', user_db)
            new_users.append(user_id)
    session.query(clazz). \
        filter_by(node_id=node_id). \
        filter(getattr(clazz, user_key).notin_(new_users)). \
        delete(synchronize_session=False)


def search_nodes_by_path(path):
    node_rows = select(text(GET_NODE_IDS_BY_PATH), path=path + '%')
    node_ids = []
    for node_row in node_rows:
        node_ids.append(node_row['id'])
    return node_ids


def get_node_path_by_id(id):
    with session_scope() as session:
        node = session.query(Node).filter_by(id=id).first()
        if node is None:
            raise_node_not_found(id)
        provider = FILE_PROVIDER_MAPPING[node.provider_id]
        paths = get_node_paths(node.id)
        path = paths[node.id]
        return path, provider


def raise_node_not_found(id):
    raise BadRequest("can't find node by id '%s'" % str(id))


def enrich_nodes_json(nodes_json):
    node_ids, parent_ids = [], []
    for node_json in nodes_json:
        node_ids.append(node_json.get('id'))
        parent_id = node_json.get('parent_id')
        if parent_id is not None:
            parent_ids.append(parent_id)
    parent_paths = get_node_paths(*parent_ids)
    for node_json in nodes_json:
        parent_id = node_json.get('parent_id')
        if parent_id is not None:
            node_json['parent_path'] = parent_paths.get(uuid.UUID(parent_id))
    with session_scope() as session:
        node_readers = get_nodes_users(NodeReader, 'reader_id', node_ids, session)
        node_writers = get_nodes_users(NodeWriter, 'writer_id', node_ids, session)
    for node_json in nodes_json:
        node_id_str = node_json.get('id')
        node_id = uuid.UUID(node_id_str)
        node_json['readers'] = node_readers.get(node_id, [])
        node_json['writers'] = node_writers.get(node_id, [])
        if node_json['node_type'] in NODE_DIRECTORY_TYPES:
            node_json.pop('size_in_bytes')


def check_read_grant(*node_ids):
    # TODO: Implement function
    return None


def check_write_grant(*node_ids):
    # TODO: Implement function
    return None


def get_node_paths(*node_ids):
    if len(node_ids) == 0:
        return {}

    # TODO: Refactor query if needed
    query = '''
        with recursive n as (
            select id, parent_id, text(id) as resource, 1 as level from nodes where id in :node_ids
            union all
            select n.id, t.parent_id, text(t.id) as resource, n.level + 1 from nodes t join n on t.id = n.parent_id
        )
        select r.id, r.path, n.node_type, n.name from (
        select t.id, '/' || string_agg(t.resource, '/') as path
          from (select id, resource from n order by id, level desc) t
         group by t.id
        ) r, nodes n where r.id = n.id'''
    paths = select(text(query), node_ids=node_ids).fetchall()

    paths_map = {}
    for id, path, node_type, name in paths:
        extension = ''
        if node_type == NODE_TYPE_FILE:
            extension = '.' + get_file_extension(name)
        paths_map[id] = path + extension
    return paths_map






