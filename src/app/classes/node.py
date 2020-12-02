from app.classes import Base
from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

NODE_TYPE_DIRECTORY = 1
NODE_TYPE_FILE = 2
NODE_TYPE_PART_OF_FILE = 3
NODE_TYPE_LINK = 4
NODE_TYPE_PUBLIC_DIRECTORY = 5

NODE_PROVIDER_SERVER = 1
NODE_PROVIDER_YANDEX_DISK = 2

NODE_DIRECTORY_TYPES = [NODE_TYPE_DIRECTORY, NODE_TYPE_PUBLIC_DIRECTORY]


class Node(Base):
    __tablename__ = 'nodes'
    id = Column(UUID(as_uuid=True), primary_key=True)
    node_type = Column(BigInteger)
    parent_id = Column(UUID(as_uuid=True))
    provider_id = Column(BigInteger)
    size_in_bytes = Column(BigInteger)
    name = Column(String(100))
    description = Column(String)
    owner_id = Column(UUID(as_uuid=True))
    created_by = Column(UUID(as_uuid=True))
    created_when = Column(TIMESTAMP(timezone=True))
    modified_by = Column(UUID(as_uuid=True))
    modified_when = Column(TIMESTAMP(timezone=True))

    def __init__(self, id, node_type, provider_id, name, parent_id=None, size_in_bytes=None, description=None,
                 owner_id=None, created_by=None, created_when=None, modified_by=None, modified_when=None):
        self.id = id
        self.node_type = node_type
        self.parent_id = parent_id
        self.provider_id = provider_id
        self.size_in_bytes = size_in_bytes
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.created_by = created_by
        self.created_when = created_when
        self.modified_by = modified_by
        self.modified_when = modified_when

    def __repr__(self):
        return "<Node('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % \
               (self.id, self.node_type, self.parent_id, self.provider_id, self.size_in_bytes, self.name,
                self.description, self.owner_id, self.created_by, self.created_when, self.modified_by,
                self.modified_when)


class NodeReader(Base):
    __tablename__ = 'node_readers'
    node_id = Column(UUID(as_uuid=True), primary_key=True)
    reader_id = Column(UUID(as_uuid=True), primary_key=True)

    def __init__(self, node_id, reader_id):
        self.node_id = node_id
        self.reader_id = reader_id

    def __repr__(self):
        return "<NodeReader('%s', '%s')" % (self.node_id, self.reader_id)


class NodeWriter(Base):
    __tablename__ = 'node_writers'
    node_id = Column(UUID(as_uuid=True), primary_key=True)
    writer_id = Column(UUID(as_uuid=True), primary_key=True)

    def __init__(self, node_id, writer_id):
        self.node_id = node_id
        self.writer_id = writer_id

    def __repr__(self):
        return "<NodeWriter('%s', '%s')" % (self.node_id, self.writer_id)
