from django.http import HttpResponse

class StripeWH_Handler:
    """Handle strpe webhooks"""

    def __init__(self, request):
        self.request = request

    
    def handle_even(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)