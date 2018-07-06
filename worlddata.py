# -*- coding: utf-8 -*-
"""Worlddata module.

This module to connect with MongoDB, get world_bank data and
show this data in HTML file.
"""
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'world_bank'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/world_bank'
mongo = PyMongo(app)


@app.route('/')
def index():
    """Get the data from the database to process and display them."""
    pass
