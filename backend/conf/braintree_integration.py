import braintree
from django.conf import settings


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=settings.BRAINTREE_ENVIRONMENT,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY,
    )
)
