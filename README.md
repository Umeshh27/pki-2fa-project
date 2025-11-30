# PKI + TOTP 2FA Authentication Microservice

## 📌 Project Overview

This project implements a secure containerized microservice that demonstrates real-world authentication using **Public Key Infrastructure (PKI)** and **Time-based One-Time Password (TOTP)** two-factor authentication.

The service uses:

- **RSA-4096 encryption** for secure seed transmission
- **RSA-PSS digital signatures** for commit verification
- **TOTP authentication** (6-digit codes, 30s period)
- **FastAPI REST API**
- **Docker multi-stage build**
- **Cron job scheduling**
- **Persistent Docker volumes**

The application decrypts a securely provided seed, generates TOTP codes, verifies codes with time-window tolerance, and logs active codes every minute using cron with UTC timestamps.

---

## 🔐 Cryptography

### RSA Configuration

- **Key size:** 4096 bits
- **Public exponent:** 65537
- **Padding (decryption / encryption):** RSA-OAEP + SHA-256 + MGF1
- **Signatures:** RSA-PSS + SHA-256 (maximum salt length)

### Key Files

| File                    | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| `student_private.pem`   | Decrypt instructor-encrypted seed + sign commit   |
| `student_public.pem`    | Provided to instructor API during seed generation |
| `instructor_public.pem` | Encrypts signed commit proof                      |

---

## 🔢 Two-Factor Authentication (TOTP)

| Setting                | Value                                  |
| ---------------------- | -------------------------------------- |
| Algorithm              | SHA-1                                  |
| Digits                 | 6                                      |
| Period                 | 30 seconds                             |
| Seed format            | 64-character hex → converted to Base32 |
| Verification tolerance | ±1 time window (±30 seconds)           |

The decrypted seed is persisted inside the Docker volume:

```text
/data/seed.txt
```
