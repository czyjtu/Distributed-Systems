# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cv.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x08\x63v.proto\x12\x02\x63v\"3\n\x07NpArray\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x12\x0c\n\x04rows\x18\x02 \x01(\r\x12\x0c\n\x04\x63ols\x18\x03 \x01(\r\"4\n\rKmeansRequest\x12\x18\n\x03img\x18\x01 \x01(\x0b\x32\x0b.cv.NpArray\x12\t\n\x01k\x18\x02 \x01(\r24\n\rEdgeDetection\x12#\n\x05\x63\x61nny\x12\x0b.cv.NpArray\x1a\x0b.cv.NpArray\"\x00\x32:\n\x0cSegmentation\x12*\n\x06kmeans\x12\x11.cv.KmeansRequest\x1a\x0b.cv.NpArray\"\x00\x62\x06proto3')



_NPARRAY = DESCRIPTOR.message_types_by_name['NpArray']
_KMEANSREQUEST = DESCRIPTOR.message_types_by_name['KmeansRequest']
NpArray = _reflection.GeneratedProtocolMessageType('NpArray', (_message.Message,), {
  'DESCRIPTOR' : _NPARRAY,
  '__module__' : 'cv_pb2'
  # @@protoc_insertion_point(class_scope:cv.NpArray)
  })
_sym_db.RegisterMessage(NpArray)

KmeansRequest = _reflection.GeneratedProtocolMessageType('KmeansRequest', (_message.Message,), {
  'DESCRIPTOR' : _KMEANSREQUEST,
  '__module__' : 'cv_pb2'
  # @@protoc_insertion_point(class_scope:cv.KmeansRequest)
  })
_sym_db.RegisterMessage(KmeansRequest)

_EDGEDETECTION = DESCRIPTOR.services_by_name['EdgeDetection']
_SEGMENTATION = DESCRIPTOR.services_by_name['Segmentation']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NPARRAY._serialized_start=16
  _NPARRAY._serialized_end=67
  _KMEANSREQUEST._serialized_start=69
  _KMEANSREQUEST._serialized_end=121
  _EDGEDETECTION._serialized_start=123
  _EDGEDETECTION._serialized_end=175
  _SEGMENTATION._serialized_start=177
  _SEGMENTATION._serialized_end=235
# @@protoc_insertion_point(module_scope)
