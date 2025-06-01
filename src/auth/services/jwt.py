from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from src.auth.schemas import TokenPairSchema
from src.config import settings
from src.users.models import User


def get_payload(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid token claims")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_token_pair(user: User) -> TokenPairSchema:
    now = datetime.now(timezone.utc)

    access_payload = {
        'sub': str(user.id),
        'exp': now + timedelta(settings.JWT_ACCESS_TOKEN_EXPIRE),
        'type': 'access',
    }

    refresh_payload = {
        'sub': str(user.id),
        'exp': now + timedelta(settings.JWT_REFRESH_TOKEN_EXPIRE),
        'type': 'refresh',
    }

    access = jwt.encode(access_payload, **settings.get_auth_data)
    refresh = jwt.encode(refresh_payload, **settings.get_auth_data)

    token_pair = TokenPairSchema(access_token=access, refresh_token=refresh)
    return token_pair