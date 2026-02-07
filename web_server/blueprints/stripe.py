"""Stripe payment integration blueprint."""

import os

from flask import Blueprint, request, jsonify, session as s
from blueprints.middleware import login_required
from utils.user_utils import subscribe
import stripe

stripe_bp = Blueprint("stripe", __name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_ENDPOINT_SECRET")

subscription = os.getenv("GANDER_SUBSCRIPTION")

@login_required
@stripe_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """
    Creates the stripe checkout session
    """
    try:
        # Checks to see who is subscribing to who
        user_id = s.get("user_id")
        streamer_id = request.args.get("streamer_id")
        checkout_session = stripe.checkout.Session.create(
            ui_mode = 'embedded',
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1QtGVsQoce1zhaP3csrztOoh',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            redirect_on_completion = 'never',
            client_reference_id = f"{user_id}-{streamer_id}"
        )
    except (ValueError, TypeError, KeyError) as e:
        return str(e), 500

    return jsonify(clientSecret=checkout_session.client_secret)

@stripe_bp.route('/session-status')  # check for payment status
def session_status():
    """
    Used to query payment status
    """
    checkout_session = stripe.checkout.Session.retrieve(
        request.args.get('session_id')
    )

    return jsonify(
        status=checkout_session.status,
        customer_email=checkout_session.customer_details.email
    )

@stripe_bp.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    """
    Webhook for handling stripe payments
    """
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    # Verifies signature is from Stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    # Handles payment success webhook
    if event['type'] == "checkout.session.completed":
        checkout_session = event['data']['object']
        product_id = stripe.checkout.Session.list_line_items(
            checkout_session['id']
        )['data'][0]['price']['product']
        if product_id == subscription:
            client_reference_id = checkout_session.get(
                "client_reference_id"
            )
            user_id, streamer_id = map(
                int, client_reference_id.split("-")
            )
            subscribe(user_id, streamer_id)

    return "Success", 200
