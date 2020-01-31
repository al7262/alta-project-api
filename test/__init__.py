import pytest, logging, hashlib
from app import app, cache
from blueprints import db
from flask import Flask, request, json

def reset_db():
    db.drop_all()
    db.create_all()
    newUser = Users('al7262', 'azzahra@lamuri.com', 'Alt3rr4')
    db.session.add(newUser)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)