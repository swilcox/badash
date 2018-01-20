"""auth.py for authentication related functions"""
import hug
import jwt
from models import ApiKey
from settings import settings


def token_verify(token):
    """JWT token verification"""
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithm='HS256')
    except jwt.DecodeError:
        return False


jwt_auth = hug.authentication.token(token_verify)


def api_key_verify(api_key):
    """auth via an api key"""
    return ApiKey.objects.filter(api_key=api_key).first()


api_key_auth = hug.authentication.api_key(api_key_verify)


def multi_verify(token, api_key):
    if token:
        return token_verify(token)
    elif api_key:
        return api_key_verify(api_key)
    return None


@hug.authentication.authenticator
def multi_auth(request, response, verify_user, **kwargs):
    """Multi optional verification

    Checks for the Authorization header and verifies using the verify_user function
    """
    token = request.get_header('Authorization')
    api_key = request.get_header('X-Api-Key')
    if token or api_key:
        user = verify_user(token, api_key)
        return user if user else False
    return None


authenticated = multi_auth(multi_verify)
