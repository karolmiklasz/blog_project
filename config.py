import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bardzo_tajny_klucz'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///moja_baza_danych.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

