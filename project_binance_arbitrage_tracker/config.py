# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "671e4bc8fb9d3fb172b3dc6defc37b9a5f1fc7412ddd2f15"

# Secret key for signing cookies
SECRET_KEY = "bfa5ed8dd1f52f3617ded1a3e820859cd0a2e2a534ec5579"

api_key = "5DB2Idd8d1sKhSj63C3iEObtygrjsvJtqD1tux7vnaSezVM0TT0HWhOpGux8krwo"

api_secret = "X1M6I5LTewMP36fGwCukUx245TaYFPALfV6D367bKLKCWYRc6AHGgbMxpQzBv2K2"
