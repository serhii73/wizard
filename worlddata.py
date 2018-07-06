# -*- coding: utf-8 -*-
"""Worlddata module.

This module to connect with MongoDB, get world_bank data and
show this data in HTML file.
"""
import pycountry
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'world_bank'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/world_bank'
mongo = PyMongo(app)


@app.route('/')
def index():
    """Get the data from the database to process and display them."""
    # Get data from MongoDB.
    need_mong_data = mongo.db.world.find(
        {'countryname': {'$nin': ['Middle East and North Africa',
                                  'East Asia and Pacific', 'South Asia',
                                  'Europe and Central Asia', 'Africa',
                                  'World']}},
        {'project_name': 1, 'countryname': 1,
         'lendprojectcost': 1, 'countrycode': 1})

    # Replace countrycode from 2 to 3 numbers, need for D3js.
    mongo_data_list = []
    for mongo_line in need_mong_data:
        for country in list(pycountry.countries):
            if mongo_line['countryname'] in str(country):
                change_name = country.alpha_3
        mongo_line['countrycode'] = change_name
        mongo_data_list.append(mongo_line)

    # Create dict - country: all lendprojectcost.
    all_country_money = {}
    for i in mongo_data_list:
        if i['countrycode'] not in all_country_money:
            all_country_money[i['countrycode']] = i['lendprojectcost']
        else:
            all_country_money[i['countrycode']] = i['lendprojectcost'] + \
                                                  all_country_money[
                                                      i['countrycode']]
    # Dict to list, need for D3js.
    data_list_with_all_money = [[k, v] for k, v in all_country_money.items()]

    # Create dict with all project_name and lendprojectcost in each country.
    all_projects_cost = {}
    for i in mongo_data_list:
        all_projects_cost[i['countrycode']] = {'project_name': []}
    for i in mongo_data_list:
        all_projects_cost[i['countrycode']]['project_name'].append({
            i['project_name']: i['lendprojectcost']
        })

    return render_template('index.html',
                           data_list_with_all_money=data_list_with_all_money,
                           all_projects_cost=all_projects_cost)


if __name__ == '__main__':
    app.run(debug=True)
