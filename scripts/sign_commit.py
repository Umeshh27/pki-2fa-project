import base64
import subprocess
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

STUDENT_PRIVATE_KEY_PATH = Path("student_private.pem")
INSTRUCTOR_PUBLIC_KEY_PATH = Path("instructor_public.pem")


def load_private_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_private_key(data, password=None)


def load_public_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_public_key(data)


def get_latest_commit_hash() -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def sign_message(message: str, private_key) -> bytes:
    message_bytes = message.encode("utf-8")
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext


def main():
    commit_hash = get_latest_commit_hash()
    print("Commit Hash:", commit_hash)

    student_priv = load_private_key(STUDENT_PRIVATE_KEY_PATH)
    instr_pub = load_public_key(INSTRUCTOR_PUBLIC_KEY_PATH)

    signature = sign_message(commit_hash, student_priv)
    encrypted_signature = encrypt_with_public_key(signature, instr_pub)

    enc_sig_b64 = base64.b64encode(encrypted_signature).decode("utf-8")
    print("Encrypted Signature (Base64):")
    print(enc_sig_b64)


if __name__ == "__main__":
    main()
