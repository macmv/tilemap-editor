# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tilemap.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tilemap.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rtilemap.proto\"\xa1\x01\n\x07Tilemap\x12\"\n\x05tiles\x18\x01 \x03(\x0b\x32\x13.Tilemap.TilesEntry\x12\x11\n\ttileWidth\x18\x02 \x01(\x03\x12\x12\n\ntileHeight\x18\x03 \x01(\x03\x12\r\n\x05width\x18\x04 \x01(\x03\x12\x0e\n\x06height\x18\x05 \x01(\x03\x1a,\n\nTilesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\x62\x06proto3')
)




_TILEMAP_TILESENTRY = _descriptor.Descriptor(
  name='TilesEntry',
  full_name='Tilemap.TilesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Tilemap.TilesEntry.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='Tilemap.TilesEntry.value', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=179,
)

_TILEMAP = _descriptor.Descriptor(
  name='Tilemap',
  full_name='Tilemap',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tiles', full_name='Tilemap.tiles', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tileWidth', full_name='Tilemap.tileWidth', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tileHeight', full_name='Tilemap.tileHeight', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='width', full_name='Tilemap.width', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='Tilemap.height', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TILEMAP_TILESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=179,
)

_TILEMAP_TILESENTRY.containing_type = _TILEMAP
_TILEMAP.fields_by_name['tiles'].message_type = _TILEMAP_TILESENTRY
DESCRIPTOR.message_types_by_name['Tilemap'] = _TILEMAP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Tilemap = _reflection.GeneratedProtocolMessageType('Tilemap', (_message.Message,), dict(

  TilesEntry = _reflection.GeneratedProtocolMessageType('TilesEntry', (_message.Message,), dict(
    DESCRIPTOR = _TILEMAP_TILESENTRY,
    __module__ = 'tilemap_pb2'
    # @@protoc_insertion_point(class_scope:Tilemap.TilesEntry)
    ))
  ,
  DESCRIPTOR = _TILEMAP,
  __module__ = 'tilemap_pb2'
  # @@protoc_insertion_point(class_scope:Tilemap)
  ))
_sym_db.RegisterMessage(Tilemap)
_sym_db.RegisterMessage(Tilemap.TilesEntry)


_TILEMAP_TILESENTRY._options = None
# @@protoc_insertion_point(module_scope)