from datetime import datetime
from django.shortcuts import redirect
from rest_framework.views import APIView
import stripe
from django.conf import settings
from django.http import JsonResponse
from users.models import Appointment
from users.models import TimeSlot
from datetime import datetime
import json

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

FRONTEND_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
FRONTEND_CHECKOUT_FAILED_URL = settings.CHECKOUT_FAILED_URL


class CreateCheckoutSession(APIView):
    def post(self, request):
        data_dict = dict(request.data)
        price = data_dict['price'][0]
        product_name = data_dict['product_name'][0]
        appointment_details = data_dict['metadata[appointment_details]'][0]
        appointment_dict = json.loads(appointment_details)

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': price
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=FRONTEND_CHECKOUT_SUCCESS_URL,
                cancel_url=FRONTEND_CHECKOUT_FAILED_URL,
                metadata={
                    'doctor_id': str(appointment_dict['doctor_id']),
                    'patient_id': str(appointment_dict['patient_id']),
                    'time_slot_id': str(appointment_dict['appointment_time']['id']),
                    'appointment_charge': str(appointment_dict['appointment_time']['physical_appointment_charge']),
                    'appointment_type': str(appointment_dict['appointment_type']),
                    'date': appointment_dict['appointment_date'],
                }
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)

            return e


class WebHook(APIView):

    def handle_success(self, session):
        metadata = session.metadata
        appointment = Appointment(
            patient_id=int(metadata['patient_id']),
            doctor_id=int(metadata['doctor_id']),
            time_slot_id=int(metadata['time_slot_id']),
            appointment_charge=int(metadata['appointment_charge']),
            date=datetime.strptime(
                metadata['date'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        )
        appointment.save()
        print("Appointment created:", appointment)

    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        # Handle the event
        if event.type == 'checkout.session.completed':
            session = event.data.object
            self.handle_success(session)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object
            print("--------payment_method ---------->", payment_method)
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return JsonResponse({'success': True})
