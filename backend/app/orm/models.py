import uuid

from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func

from core import config


Base = declarative_base()


class Request(Base):
    __tablename__ = "requests"
    __table_args__ = {"schema": config.db_scheme}

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_on = Column(DateTime, server_default=func.now())
    request_id = Column(String, index=True, default=lambda: str(uuid.uuid4()))
    request_body = Column(JSON)

    response = relationship("Response", back_populates="request", uselist=False)


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = {"schema": config.db_scheme}

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String, ForeignKey('requests.request_id'))
    response_datetime = Column(DateTime, server_default=func.now())

    request = relationship("Request", back_populates="response")
    extracts = relationship("Extract", back_populates="response")


class Extract(Base):
    __tablename__ = "extracts"
    __table_args__ = {"schema": config.db_scheme}

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    image_number = Column(Integer, default=0)
    original_image_s3_url = Column(String)
    processed_image_s3_url = Column(String)
    extracted_text_s3_url = Column(String)
    extracted_text = Column(String)
    response_id = Column(String, ForeignKey('responses.id'))

    response = relationship("Response", back_populates="extracts")


class LLMDocumentCorrections(Base):
    __tablename__ = "llm_document_corrections"
    __table_args__ = {"schema": config.db_scheme}

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    llm_prompt = Column(String, nullable=True)
    llm_response = Column(String, nullable=True)
    document_type_code = Column(Integer, ForeignKey('document_type.code'))

    response_id = Column(String, ForeignKey('responses.id'))

    response = relationship("Response", back_populates="llm_document_corrections")
    document_type = relationship("DocumentType", back_populates="llm_document_corrections")


class DocumentType(Base):
    __tablename__ = "document_type"
    __table_args__ = {"schema": config.db_scheme}

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    code = Column(Integer, primary_key=True)

    llm_document_corrections = relationship("LLMDocumentCorrections", back_populates="document_type")
