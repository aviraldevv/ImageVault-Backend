from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from database import engine, Base, SessionLocal
from models import User, SignupRequest, DownloadRequest

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/signup")
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = User(username=request.username, password=hashed_password, downloads=[])
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "User created successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/download")
async def save_downloaded_image(
    request: DownloadRequest,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=400, detail="Invalid user")

        query = select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user:

            user.downloads.append(request.url)
            db.add(user)  
            await db.commit()
            await db.refresh(user)  

            return {"message": "Download URL saved successfully"}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@app.get("/downloads")
async def get_downloaded_images(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=400, detail="Invalid user")

        query = select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user:

            return {"downloads": user.downloads}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")