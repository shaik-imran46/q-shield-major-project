from fastapi import APIRouter
from app.database.schemas import (
    QRNGRequest, QRNGResponse, QKDRequest, QKDResponse,
    PQCKeygenResponse, PQCEncapRequest, PQCEncapResponse,
    PQCDecapRequest, PQCDecapResponse, PQCSignRequest, PQCSignResponse,
    PQCVerifyRequest, PQCVerifyResponse
)
from app.quantum.qrng import qrng_service
from app.quantum.qkd import qkd_service
from app.quantum.pqc import pqc_service

router = APIRouter(prefix="/quantum", tags=["Post-Quantum & Quantum Simulation"])

@router.post("/qrng", response_model=QRNGResponse)
def generate_qrng_bits(req: QRNGRequest = QRNGRequest()):
    res = qrng_service.generate_random_bits(num_bits=req.num_bits, num_qubits=req.num_qubits)
    return QRNGResponse(**res)

@router.post("/qkd", response_model=QKDResponse)
def run_bb84_simulation(req: QKDRequest = QKDRequest()):
    res = qkd_service.simulate_key_exchange(
        num_qubits=req.num_qubits,
        eavesdropper_present=req.eavesdropper_present
    )
    return QKDResponse(**res)

@router.post("/pqc/keygen")
def generate_pqc_keys():
    kem_keys = pqc_service.kem_generate_keypair()
    dsa_keys = pqc_service.dsa_generate_keypair()
    return {
        "kem": kem_keys,
        "dsa": dsa_keys,
        "standard": "NIST Post-Quantum Cryptography Standardization (FIPS 203 / FIPS 204)"
    }

@router.post("/pqc/encapsulate", response_model=PQCEncapResponse)
def pqc_encapsulate(req: PQCEncapRequest):
    res = pqc_service.kem_encapsulate(public_key=req.public_key)
    return PQCEncapResponse(**res)

@router.post("/pqc/decapsulate", response_model=PQCDecapResponse)
def pqc_decapsulate(req: PQCDecapRequest):
    res = pqc_service.kem_decapsulate(private_key=req.private_key, ciphertext=req.ciphertext)
    return PQCDecapResponse(**res)

@router.post("/pqc/sign", response_model=PQCSignResponse)
def pqc_sign(req: PQCSignRequest):
    res = pqc_service.dsa_sign(message=req.message, private_key=req.private_key)
    return PQCSignResponse(**res)

@router.post("/pqc/verify", response_model=PQCVerifyResponse)
def pqc_verify(req: PQCVerifyRequest):
    res = pqc_service.dsa_verify(message=req.message, signature=req.signature, public_key=req.public_key)
    return PQCVerifyResponse(**res)
