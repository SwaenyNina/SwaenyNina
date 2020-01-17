import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
import chatterbot
from chatterbot import ChatBot, filters
from chatterbot.ext.django_chatterbot import settings
import logging

logging.basicConfig(level=logging.INFO)

class ChatterBotAppView(TemplateView):
    template_name = 'app.html'

class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """
    chatbot = ChatBot('Nina',
        logic_adapters=[
            "chatterbot.logic.BestMatch",
            'chatterbot.logic.MathematicalEvaluation'
        ], 
        filters=[filters.get_recent_repeated_responses]
    )

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatbot.get_response(input_data)

        response_data = response.serialize()

        ip = request.META.get('REMOTE_ADDR')
        with open(ip + ".log", "a") as f:
            f.write("{} asked: {} with response: {}\n".format(ip, input_data["text"], response))

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """

        return JsonResponse({
            'name': self.chatbot.name
        })
