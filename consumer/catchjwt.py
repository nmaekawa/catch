# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from dateutil import tz
import iso8601
import jwt
import logging


logger = logging.getLogger(__name__)


def decode_token(token, secret_key='', verify=False):
    try:    # decode to get consumerKey
        payload = jwt.decode(token, secret_key, verify=verify)
    except (jwt.exceptions.InvalidTokenError,
            jwt.exceptions.DecodeError) as e:
        logger.info(
            'failed to decode jwt: {}'.format(e), exc_info=True)
        return None
    else:
        return payload


def encode_token(payload, secret_key):
    return jwt.encode(payload, secret_key)


def encode_catchjwt(apikey=None, secret=None,
                    user=None, iat=None, ttl=60, override=[]):
    payload = {
        'consumerKey': apikey if apikey else str(uuid4()),
        'userId': user if user else str(uuid4()),
        'issuedAt': iat if iat else now_utc().isoformat(),
        'ttl': ttl,
        'override': override,
    }
    return encode_token(payload, secret)


def now_utc():
    return datetime.now(tz.tzutc())


def validate_token(token_payload):
    '''check for token expiration, secret-key expiration.'''

    now = now_utc()

    # check token expiration date
    issued_at = token_payload.get('issuedAt', None)
    ttl = token_payload.get('ttl', None)
    if issued_at is None or ttl is None:
        return 'missing `issuedAt` or `ttl` in auth token'
    try:
        iat = iso8601.parse_date(issued_at)
        ttl = int(ttl)
    except iso8601.ParseError as e:
        return 'invalid `issuedAt` date format, expected iso8601. {}'.format(e)
    except ValueError:
        return 'invaild `ttl` value, expected integer'

    token_exp = iat + timedelta(seconds=ttl)
    if token_exp < now:
        return 'token has expired'

    # check for issuing at future - trying to cheat expiration?
    if iat > now:
        return 'invalid `issuedAt` in the future.'

    return None

