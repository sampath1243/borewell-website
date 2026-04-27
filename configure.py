import os

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///borewell.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Razorpay Keys
    RAZORPAY_KEY = "rzp_test_xxxxx"
    RAZORPAY_SECRET = "your_secret"