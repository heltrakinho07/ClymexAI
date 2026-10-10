"""
CLYMEX AI - Authentication & RBAC API Endpoints
"""

import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app.config import settings
from app.models.auth import UserLogin, Token, UserRole, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

# Predefined institutional / role accounts for demo and testing
MOCK_USERS = {
    "admin@clymex.ai": {
        "id": "USR-001",
        "email": "admin@clymex.ai",
        "full_name": "Administrador do Sistema",
        "organization": "CLYMEX AI Operations",
        "role": UserRole.ADMIN,
        "password": "clymex2026admin"
    },
    "analyst@clymex.ai": {
        "id": "USR-002",
        "email": "analyst@clymex.ai",
        "full_name": "Especialista em Risco Hidrológico",
        "organization": "INGD Moçambique / ARA-Sul",
        "role": UserRole.ANALYST,
        "password": "analystpassword"
    },
    "partner@ingd.gov.mz": {
        "id": "USR-003",
        "email": "partner@ingd.gov.mz",
        "full_name": "Delegado Distrital da Manhiça",
        "organization": "INGD - Protecção Civil",
        "role": UserRole.INSTITUTION,
        "password": "partnerpassword"
    }
}


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais de acesso inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return Token(
        access_token=token,
        token_type="bearer",
        role=user["role"],
        full_name=user["full_name"],
        organization=user["organization"]
    )


@router.get("/me", response_model=UserOut)
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in MOCK_USERS:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = MOCK_USERS[email]
        return UserOut(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            organization=user["organization"],
            role=user["role"],
            created_at="2026-01-01T00:00:00Z"
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Não autorizado")
