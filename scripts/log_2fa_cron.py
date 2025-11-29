#!/usr/bin/env python3
import sys
from datetime import datetime, timezone
from pathlib import Path

from app.totp_utils import generate_totp_code

SEED_PATH = Path("/data/seed.txt")
LOG_PATH = Path("/cron/last_code.txt")

def main():
    try:
        if not SEED_PATH.exists():
            print("Seed not found", file=sys.stderr)
            return

        hex_seed = SEED_PATH.read_text().strip()
        code = generate_totp_code(hex_seed)

        now = datetime.now(timezone.utc)
        ts = now.strftime("%Y-%m-%d %H:%M:%S")

        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a") as f:
            f.write(f"{ts} - 2FA Code: {code}\n")

    except Exception as e:
        print("Error in cron script:", e, file=sys.stderr)

if __name__ == "__main__":
    main()
