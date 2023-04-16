# Hospital Management System
This is a Django web application for managing hospital-related activities. It provides features such as user authentication, payments, and appointment management. The application is built using the **Django framework**, and utilizes several third-party packages, including **Django REST Framework** and **Stripe**.

## Disclaimer
* You will need a Stripe Account, Stripe API keys, Gmail Account and Gmail App Password.

## Installation
* Clone the repository
* Install the required packages using pip install -r requirements.txt
* Set up environment variables for EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, STRIPE_SECRET_KEY, and STRIPE_WEBHOOK_SECRET.
* Run python manage.py migrate to create the database schema.
* Start the development server using python manage.py runserver.

## Features
### User authentication and management
### Patient, Doctors and Admin functionality
### Appointment management
### Stripe payment integration
### Review System
### JWT-based authentication for API endpoints

## Dependencies
* asgiref==3.6.0
* autopep8==2.0.2
* backports.zoneinfo==0.2.1
* certifi==2022.12.7
* charset-normalizer==3.1.0
* Django==4.2
* django-cors-headers==3.14.0
* django-environ==0.10.0
* djangorestframework==3.14.0
* djangorestframework-simplejwt==5.2.2
* idna==3.4
* pycodestyle==2.10.0
* PyJWT==2.6.0
* pytz==2023.3
* requests==2.28.2
* sqlparse==0.4.3
* stripe==5.4.0
* tomli==2.0.1
* urllib3==1.26.15


