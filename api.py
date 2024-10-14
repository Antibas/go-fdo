from fastapi import FastAPI, APIRouter, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess, os, aiomysql

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vue.js dev server
    "http://127.0.0.1:5173",  # Alternate localhost form
    # You can add more origins here as needed (e.g., production URLs)
]

# Add CORS middleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,  # Allows cookies and credentials
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

router = APIRouter()

PATH = 'scripts/'
# COMPONENTS = ["db", 'aio', 'rv', 'owner', 'manufacturer', 'device', 'reseller']

# outlog = lambda out: (out.stderr if out.stderr else out.stdout) + "\n"

def _run_command(command: str, cwd: str=None):
    out = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    if out.returncode:
        raise Exception(out.stderr)
    return out.stderr if out.stderr else out.stdout

@router.get("/start_client")
async def start_client():
    try:
        return Response(content=_run_command(f'./{PATH}start_client.bash'), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)

@router.get("/get_GUID")
async def get_GUID():
    try:
        return Response(content=_run_command(f'./{PATH}get_guid.bash'), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)
    
@router.get("/register_GUID/{GUID}")
async def register_GUID(GUID: str):
    try:
        return Response(content=_run_command(f'./{PATH}register_rv.bash {GUID}'), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)

@router.get("/exchange_keys")
async def exchange_keys():
    try:
        return Response(content=_run_command(f'./{PATH}key_exchange.bash'), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)
    
@router.get("/voucher/{GUID}")
async def get_voucher(GUID: str):
    try:
        return Response(content=_run_command(f'go run ./examples/cmd server -resale-guid {GUID} -resale-key key.pem -db ./test.db'), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)

@router.get("/generate_public_key")
async def generate_public_key():
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,  # You can choose 2048, 3072, or 4096 bits
            backend=default_backend()
        )

        # Get the public key from the private key
        public_key = private_key.public_key()

        # Serialize the public key to PEM format (text-based)
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open("key.pem", 'wb+') as k:
            k.write(pem_public_key)
            return Response(content=pem_public_key, status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)