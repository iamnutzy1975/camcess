from di import container
from services import IConfigService
from services import ILoggerService
from services import IEmailService

config = container.instance(IConfigService)
assert isinstance(config, IConfigService)

logger = container.instance(ILoggerService)
assert isinstance(logger, ILoggerService)

email = container.instance(ILoggerService)
assert isinstance(email, IEmailService)

def gmailxfr(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Gmail account processed!'
