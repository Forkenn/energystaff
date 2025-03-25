import src.config as config

from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

cookie_transport = CookieTransport(
    cookie_name='energystaff_token',
    cookie_max_age=config.TOKEN_EXPIRE_SECONDS,
    cookie_secure=False,
    cookie_httponly=True
)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config.SECRET_TOKEN, lifetime_seconds=config.TOKEN_EXPIRE_SECONDS)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
