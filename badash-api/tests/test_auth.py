"""test_auth.py"""
import requests_mock

from jose import jwt
import pytest

import auth
from models import ApiKey
from settings import settings

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQDdlatRjRjogo3WojgGHFHYLugdUWAY9iR3fy4arWNA1KoS8kVw33cJibXr8bvwUAUparCwlvdbH6dvEOfou0/gCFQsHUfQrSDv+MuSUMAe8jzKE4qW+jK+xQU9a03GUnKHkkle+Q0pX/g6jXZ7r1/xAK5Do2kQ+X5xK9cipRgEKwIDAQABAoGAD+onAtVye4ic7VR7V50DF9bOnwRwNXrARcDhq9LWNRrRGElESYYTQ6EbatXS3MCyjjX2eMhu/aF5YhXBwkppwxg+EOmXeh+MzL7Zh284OuPbkglAaGhV9bb6/5CpuGb1esyPbYW+Ty2PC0GSZfIXkXs76jXAu9TOBvD0ybc2YlkCQQDywg2R/7t3Q2OE2+yo382CLJdrlSLVROWKwb4tb2PjhY4XAwV8d1vy0RenxTB+K5Mu57uVSTHtrMK0GAtFr833AkEA6avx20OHo61Yela/4k5kQDtjEf1N0LfI+BcWZtxsS3jDM3i1Hp0KSu5rsCPb8acJo5RO26gGVrfAsDcIXKC+bQJAZZ2XIpsitLyPpuiMOvBbzPavd4gY6Z8KWrfYzJoI/Q9FuBo6rKwl4BFoToD7WIUS+hpkagwWiz+6zLoX1dbOZwJACmH5fSSjAkLRi54PKJ8TFUeOP15h9sQzydI8zJU+upvDEKZsZc/UhT/SySDOxQ4G/523Y0sz/OZtSWcol/UMgQJALesy++GdvoIDLfJX5GBQpuFgFenRiRDabxrE9MNUZ2aPFaFp+DyAe+b4nDwuJaW2LURbr8AEZga7oQj0uYxcYw==
  -----END RSA PRIVATE KEY-----  """

OTHER_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAsOAlnW2ytxF41kV0qtXcxI4Tf3fReOP6ycQXLCIJhN50DPkg
513dtXeAD3zR+zNP6zHetKEXvveJu31VhODSS85fIi6785fkEQlFd7QkCwrvMYNd
tpE0YeehI3N8z9/rVbs4Gzv/w+dWqr5D9bBqEyOvpbjGBaaOADZKDCbwCHzLshGd
fN3psG2eEM1OP796JhBis2XqJcWxf4ONhwhEwZxljVEngnvzT36r9REzH7P7iozk
giTUkAprvk88Id4f+ciC5ys89RtnK6oRqz4xwNcKaQzj6CyYpLPLcYtpz+TVfSvd
b692uDj3uRGMRYbSoQIIcJepkCMW+5Ur9VB94QIDAQABAoIBABmMJqK4h4m9slBw
s8tBHKQfSV2t9smZVE30TsyHFgzk/KorCb+hZTaizhJumv3HiZGVIG/CnOVuZ6x3
C/Una/ibFE6hpXAnzj9PsYL6uAIIUEg8izqleoVxqWqvcaWs2BcH9bCpV+X58iCz
XqmME6Y0D1jGeYOzbOtG7CcZMK5o6oFRO6J2fVNjdIanYdbLaq1SrOAn+PnwTTCG
YKeoPk3L0M1j0hWf1roT9ZP2Z1KMos4d1G7zqxY9hMyd2jMCn9e4OF/p70+3g3JI
9erPJVducmrdicWYT4Y9aaICit/+OgeVVbSzVzuUXeAXTi4uBSSNWfBNpINmjUrX
Qd4sMAECgYEA4w7Q8uzUtRgDeCJnQYPYohB2S5NXOGFN6hQzhSqH1tDu5AnIQiE/
Iq3VYjMOkoS9mBkIpsUCumhIOk292VtPBqstWHX/c1u8tJFH8TZbhUY1WXCna6pA
Gjx/tesgMwsS3gdq+8Yijfbovo5qv5o0fCAYkrQNH7teum367TUlT8ECgYEAx2vR
tJPDwwNhVYao47rywf8QidL1Z4+I8tRq/aah6UKsIzSMiL3WvaYT9acTJMV6HGe1
m+Kq8c7SLNarRacchEjRJLSArErrZ2z+APvAwZyorDqn33dBU/ymidSgMlGwwXwn
LoVWSCRcIzHCYI+Dyv6Ltio+XCcBrc9pw0hOtiECgYEAy2+3+SAHCOamHRo+B645
CCPVyasPB73vEF7fNl4/7VGv6PN20QF2zvyPZne2g8KZGNC9Nqbn5dqPdGW5RykP
ajsu2saGhXZZYjOVEOMSJxwbqrJL3yRgYOF5z6YGaJVwZyygR0tkJGxoZmu160wf
4GLlgXP/GkJIAqONosDuWEECgYBVS4F7agQ+IfD8wsbz+J8iaLUrLgb2z4a0zjQg
36e6/GBiAnTle8Uggqtg06A1hx1ujtE3pqCVIm/067B/7zUcQ4To3Sd4Cedb6ltO
El/kr9vZJpFs3DYd9R9KLp6CRzyB1Vdw52j7HEooZ30LDfdB2NPrC3B2u9xU+jTz
aLb54QKBgHi4F+N01nTEUZg08HOmSaIcjkK91chJzrSFipH9EM3zTEssoNQ2pzfZ
RchDmuwWHzRVAhUJVMMIXQjP1ahCrnQou19gxbyYONASb1ETG3WHZcxxifzMi61x
kd+7VA0Ra9IFUcyj1m8zIJg6fYGxRt7HkVgAaOUUAL7BxCfnzt7d
-----END RSA PRIVATE KEY-----
"""

JWKS_RESP = """
{"keys": [
    {
        "kty": "RSA",
        "n": "3ZWrUY0Y6IKN1qI4BhxR2C7oHVFgGPYkd38uGq1jQNSqEvJFcN93CYm16_G78FAFKWqwsJb3Wx-nbxDn6LtP4AhULB1H0K0g7_jLklDAHvI8yhOKlvoyvsUFPWtNxlJyh5JJXvkNKV_4Oo12e69f8QCuQ6NpEPl-cSvXIqUYBCs",
        "e": "AQAB",
        "alg": "RS256",
        "kid": "test",
        "use": "sig"
    }
    ]
}
"""

@pytest.fixture(scope='function')
def token():
    """token fixture"""
    return 'Bearer {}'.format(jwt.encode({'user': 'tester'}, key=PRIVATE_KEY, headers={'kid': 'test'}, algorithm=jwt.ALGORITHMS.RS256))
    # return jwt.encode({'user': 'tester'}, settings.JWT_SECRET)


@pytest.fixture(scope='function')
def api_key():
    """api_key fixture"""
    yield ApiKey.objects.create(user='test_me').api_key
    ApiKey.objects.all().delete()


def test_token_verify(token):
    """test token auth verify"""
    with requests_mock.mock() as m:
        m.get(settings.JWKS_URL, text=JWKS_RESP)
        assert auth.token_verify(token) == {'user': 'tester'}
        token_2 = jwt.encode(
            {'user': 'invalid'},
            OTHER_PRIVATE_KEY,
            headers={'kid': 'test'},
            algorithm=jwt.ALGORITHMS.RS256
        )
        assert auth.token_verify(token_2) is False
        assert auth.token_verify('Bearer asdfasdfasdfasdf') is False
        assert auth.token_verify(token[0:-1]) is False


def test_api_key_verify(api_key):
    """test api_key auth verify"""
    assert auth.api_key_verify(api_key).user == 'test_me'
    assert auth.api_key_verify('invalid-api-key') is False


def test_multi_verify(token, api_key):
    """test the multi_verify method"""
    with requests_mock.mock() as m:
        m.get(settings.JWKS_URL, text=JWKS_RESP)
        assert auth.multi_verify(token, api_key) == {'user': 'tester'}
        assert auth.multi_verify(None, api_key).user == 'test_me'
        assert auth.multi_verify(None, None) is None


def test_split_token():
    """test the _split_token function"""
    assert auth._split_token('badtokenvalue') == ''
