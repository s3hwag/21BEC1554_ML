from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# SQLAlchemy Base class
Base = declarative_base()

# Create an engine connected to the PostgreSQL database
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

# SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define the Document model
class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    url = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    embeddings = relationship("Embedding", back_populates="document")


# Define the Embedding model
class Embedding(Base):
    __tablename__ = 'embeddings'

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    vector = Column(Text)  # Store vector as a JSON-encoded string or use a vector database
    similarity_score = Column(Float)
    document = relationship("Document", back_populates="embeddings")


# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    request_count = Column(Integer, default=0)


# Define the Log model
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    endpoint = Column(String)
    timestamp = Column(DateTime)
    response_time = Column(Float)
    status_code = Column(Integer)


# Create all tables
Base.metadata.create_all(bind=engine)
