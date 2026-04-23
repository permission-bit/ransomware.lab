# file: crypto/secure_file_crypto_stream.py

from __future__ import annotations

from pathlib import Path
import os
import struct

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


MAGIC = b"VNENC1"
VERSION = 1
NONCE_SIZE = 12
CHUNK_SIZE = 1024 * 1024


HARDCODED_PUBLIC_KEY = b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr/phklKfGiIMLsFmWX3l
hi/4PXm2aAqIoyDPdp+sqZQYDOjfCtKIWyDeLTKd9HPafn9gox65kOYL/51yPglj
St0r4Ab9MU9Qr1YliTaVVRZEMCN+Bc2JImaBdeaGQGcTP/zuSE2F40/8/dfpH4Tk
hm1A5EgEEloiCTX8XAu/wEjTDJrIXXdGppd33OaqIemQ4+dPxSWLhlrOu55xEbbw
QV0mhroH+Y0lEKjlnf/rMqTxfg/TDLW1osFbF+n8AW9UiYudtQZKhBnhle3OafM0
dxt/w6bkMeyDQwvqdkNdsb60n7aOjBg+FGi9dNT3sAVj77pcl1UjYoN0A2XAA5Is
SQIDAQAB
-----END PUBLIC KEY-----
"""


class SecureFileCryptoStream:
    def __init__(self) -> None:
        self.public_key = serialization.load_pem_public_key(HARDCODED_PUBLIC_KEY)

    def _build_header(self, encrypted_key: bytes, nonce: bytes) -> bytes:
        return (
            MAGIC
            + struct.pack(">B", VERSION)
            + struct.pack(">I", len(encrypted_key))
            + encrypted_key
            + nonce
        )

    def encrypt_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
    ) -> Path:
        input_path = Path(input_path)

        if not input_path.is_file():
            raise FileNotFoundError(f"File not found: {input_path}")

        if output_path is None:
            output_path = input_path.with_suffix(input_path.suffix + ".enc")
        else:
            output_path = Path(output_path)

        aes_key = os.urandom(32)
        nonce = os.urandom(NONCE_SIZE)

        encrypted_key = self.public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        header = self._build_header(encrypted_key, nonce)

        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce))
        encryptor = cipher.encryptor()
        encryptor.authenticate_additional_data(header)

        with input_path.open("rb") as fin, output_path.open("wb") as fout:
            fout.write(header)

            while chunk := fin.read(CHUNK_SIZE):
                fout.write(encryptor.update(chunk))

            fout.write(encryptor.finalize())
            fout.write(encryptor.tag)

        return output_path