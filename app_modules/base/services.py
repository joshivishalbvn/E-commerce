import stripe
from django.conf import settings

class StripeService:
    
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_payment_intent(self, amount, payment_method_id=None):
        try:
            payment_intent_params = {
                'amount':  int(amount * 100),  
                'currency': 'inr', 
                'confirm': True, 
                'return_url':'https://your-redirect-url.com/after-payment'
            }

            if payment_method_id:
                payment_intent_params['payment_method'] = payment_method_id
            
            payment_intent = stripe.PaymentIntent.create(**payment_intent_params)
            return payment_intent
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

    def retrieve_payment_intent(self, payment_intent_id):
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return payment_intent
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Error: {str(e)}")

    def refund_payment(self, payment_intent_id):
        try:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
            )
            return refund
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Error: {str(e)}")