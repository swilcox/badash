"""auth.py for authentication related functions"""
import hug
from jose import jwt
import requests
from models import ApiKey
from settings import settings


def _get_rsa_key(kid):
    """get known good jwks"""
    # TODO: cache this!!!
    rsa_key = {}
    response = requests.get(settings.JWKS_URL)
    if response.status_code == 200:
        jwks = response.json()
        for k in jwks['keys']:
            if k['kid'] == kid:
                rsa_key = {
                    'kty': k['kty'],
                    'kid': k['kid'],
                    'use': k['use'],
                    'n': k['n'],
                    'e': k['e']
                }
    return rsa_key


def _split_token(token):
    parts = token.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        return parts[1]
    return ''


def token_verify(token):
    """JWT token verification"""
    real_token = _split_token(token)
    if real_token:
        try:
            kid = jwt.get_unverified_header(real_token).get('kid', None)
        except (jwt.JWTClaimsError, jwt.JWTError):
            return False
        if kid:
            rsa_key = _get_rsa_key(kid)
            try:
                return jwt.decode(
                    real_token,
                    key=rsa_key,
                    audience=settings.JWT_AUDIENCE,
                    algorithms=settings.JWT_ALGORITHMS
                )
            except (jwt.JWTError, jwt.ExpiredSignatureError, jwt.JWTClaimsError):
                return False
    return False


jwt_auth = hug.authentication.token(token_verify)


def api_key_verify(api_key):
    """auth via an api key"""
    api_key_object = ApiKey.objects.filter(api_key=api_key).first()
    return api_key_object if api_key_object else False


api_key_auth = hug.authentication.api_key(api_key_verify)


def multi_verify(token, api_key):
    """multi_verify to auth via either a token or api_key"""
    if token:
        return token_verify(token)
    elif api_key:
        return api_key_verify(api_key)
    return None


@hug.authentication.authenticator
def multi_auth(request, response, verify_user, **kwargs):
    """API Key Authentication or JWT Token Authentication

    Checks for the Authorization header and verifies using the verify_user function
    """
    token = request.get_header('Authorization')
    api_key = request.get_header('X-Api-Key')
    if token or api_key:
        user = verify_user(token, api_key)
        return user if user else False
    return None


authenticated = multi_auth(multi_verify)
