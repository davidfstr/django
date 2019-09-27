from django.conf import settings
from django.contrib.messages.storage import default_storage
from django.utils.deprecation import MiddlewareMixin


class MessageMiddleware(MiddlewareMixin):
    """
    Middleware that handles temporary messages.
    """

    async def process_request(self, request):
        request._messages = default_storage(request)

    async def process_response(self, request, response):
        """
        Update the storage backend (i.e., save the messages).

        Raise ValueError if not all messages could be stored and DEBUG is True.
        """
        # A higher middleware layer may return a request which does not contain
        # messages storage, so make no assumption that it will be there.
        if hasattr(request, '_messages'):
            # TODO: Consider supporting third-party message storage backends
            #       that expose an async interface. No built-in storages in
            #       Django currently require an async interface.
            unstored_messages = request._messages.update(response)
            if unstored_messages and settings.DEBUG:
                raise ValueError('Not all temporary messages could be stored.')
        return response
