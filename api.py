from fastapi import FastAPI, APIRouter, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess, os

app = FastAPI()

origins = [
    "http://localhost:5174", 
    "http://127.0.0.1:5174", 
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

PATH = '/media/panagiotis-antivasis/Data7/FIDO/go-fdo/'

def _run_command(command: str, cwd: str=None):
    out = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    if out.returncode:
        raise Exception(out.stderr)
    return (out.stderr if out.stderr else out.stdout)

@router.get("/start_client")
async def start_client(init: bool=True):
    try:
        if init:
            _run_command(f'go run ./examples/cmd client -di http://{os.getenv("SERVER_IP", "127.0.0.1")}:{os.getenv("SERVER_PORT", "9999")}')
        out = _run_command('go run ./examples/cmd client')
        return Response(content=out, status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)

@router.get("/get_GUID")
async def get_GUID():
    try:
        _run_command(f'go run ./examples/cmd client -di http://{os.getenv("SERVER_IP", "127.0.0.1")}:{os.getenv("SERVER_TO0_PORT", "9997")}')
        return Response(content=_run_command("go run ./examples/cmd client -print | grep GUID | awk '{print $2}'"), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)
    
@router.get("/register_GUID/{GUID}")
async def register_GUID(GUID: str):
    try:
        _run_command(f'go run ./examples/cmd server -http {os.getenv("SERVER_IP", "127.0.0.1")}:{os.getenv("SERVER_TO0_PORT", "9997")} -to0 http://{os.getenv("SERVER_IP", "127.0.0.1")}:{os.getenv("SERVER_TO0_PORT", "9997")} -to0-guid {GUID} -db ./test.db')
        return Response(content=_run_command('go run ./examples/cmd client -rv-only'), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)

@router.get("/exchange_keys")
async def exchange_keys():
    try:
        _run_command(f'go run ./examples/cmd client -di http://{os.getenv("SERVER_IP", "127.0.0.1")}:{os.getenv("SERVER_PORT", "9999")} -di-key rsa2048')
        
        return Response(content=_run_command('go run ./examples/cmd client -kex ASYMKEX2048'), status_code=200)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)
    
@router.get("/voucher/{GUID}")
async def get_voucher(GUID: str):
    try:
        # return Response(content=_run_command(f'go run ./examples/cmd server -resale-guid {GUID} -resale-key key.pem -db ./test.db'), status_code=200)
        out = _run_command(f'go run ./examples/cmd server -resale-guid {GUID} -resale-key key.pem -db ./test.db')
        with open("voucher.pem", 'w+') as k:
            from starlette.responses import FileResponse
            k.write(out)
            # return Response(content=pem_public_key, status_code=200)
            return FileResponse(f"{PATH}{k.name}", media_type='application/octet-stream',filename=k.name)
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)

@router.get("/tpm")
async def test_with_TPM():
    try:
        _run_command(f'go run -tags tpmsim ./examples/cmd client -di http://{os.getenv("SERVER_IP", "127.0.0.1")}:{os.getenv("SERVER_PORT", "9999")} -di-key rsa2048 -tpm simulator')
        return Response(content=_run_command("go run -tags tpmsim ./examples/cmd client -di-key rsa2048 -tpm simulator"), status_code=200)
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
            key_size=2048, 
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
            from starlette.responses import FileResponse
            k.write(pem_public_key)
            # return Response(content=pem_public_key, status_code=200)
            return FileResponse(f"{PATH}{k.name}", media_type='application/octet-stream',filename=k.name)
            # return Response(
            #     content=k.read(),
            #     media_type=k.content_type,
            #     headers={"Content-Disposition": f"attachment; filename='key.pem'"}
            # )
    except Exception as e:
        return Response(content=e.__str__(), status_code=500)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("api:app", host=os.getenv("API_IP", "0.0.0.0"), port=os.getenv("API_PORT", 8000), reload=True)