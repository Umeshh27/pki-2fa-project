from pathlib import Path
from app.totp_utils import generate_totp_code, verify_totp_code, seconds_remaining_in_period

if __name__ == "__main__":
    hex_seed = "0e62d2ace8987302230b267a635719ae48b08ba650e9c089e2ab2f535df415b7"
    code = generate_totp_code(hex_seed)
    print("Code:", code, "valid_for:", seconds_remaining_in_period())
    print("Verify:", verify_totp_code(hex_seed, code))
