import jwt
import enum
import time
import hashlib
import collections

from uuid import uuid4

from homeaccountant import config
from homeaccountant.log.logger import getLogger

logger = getLogger(__name__)


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    def set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


class TokenType(enum.IntEnum):
    REFRESH = 0x01
    AUTH = 0x02


class TokenManager:
    def __init__(self):
        self.__mapping = {}

    def _generate_jwt_claims(self, expires_after=config.SERVER.LOGIN.AUTH_TOKEN_EXPIRE):
        t = int(time.time())
        return {
            'exp': t + expires_after,
            'iss': 'me',
            'iat': t
        }

    def _read_token(self, token):
        try:
            ujwt = jwt.decode(token, verify=False)
            secret = self.__mapping[ujwt['uid']].get(ujwt['ses'])
            return jwt.decode(token, secret)
        except Exception as e:
            logger.error(e)
            raise KeyError

    def generate_session_tokens(self, uid):
        uuid = uuid4()
        base = {
            'ses': hashlib.sha1(uuid.bytes).hexdigest()[:8],
            'uid': uid
        }
        try:
            self.__mapping[uid].set(base['ses'], uuid.hex)
        except:
            self.__mapping[uid] = LRUCache(5)
            self.__mapping[uid].set(base['ses'], uuid.hex)
        auth_token = self._generate_jwt_claims()
        auth_token.update(base, typ=int(TokenType.AUTH))
        refresh_token = self._generate_jwt_claims(expires_after=config.SERVER.LOGIN.REFRESH_TOKEN_EXIRE)
        refresh_token.update(base, typ=int(TokenType.REFRESH))
        return {'auth': jwt.encode(auth_token, uuid.hex).decode('utf8'), 'refresh': jwt.encode(refresh_token, uuid.hex).decode('utf8')}

    def get_uid(self, auth_token):
        try:
            d = self._read_token(auth_token)
            if d['typ'] == TokenType.AUTH:
                return d['uid']
            else:
                return None
        except KeyError:
            return None

    def refresh_auth_token(self, refresh_token):
        try:
            token = self._read_token(refresh_token)
            auth_token = self._generate_jwt_claims()
            auth_token.update({'ses':token['ses'], 'uid':token['uid'], 'typ':int(TokenType.AUTH)})
            return jwt.encode(auth_token, self.__mapping[token['uid']].get(token['ses'])).decode('utf8')
        except KeyError:
            return None

    def revoke_tokens(self, token):
        try:
            d = self._read_token(token)
            del self.__mapping[d['uid']][d['ses']]
        except Exception as e:
            logger.error(e)
