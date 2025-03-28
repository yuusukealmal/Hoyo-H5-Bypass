import base64, requests, re


def encrypt(source: str) -> str:
    public_key_pem = b"""
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4PMS2JVMwBsOIrYWRluY
    wEiFZL7Aphtm9z5Eu/anzJ09nB00uhW+ScrDWFECPwpQto/GlOJYCUwVM/raQpAj
    /xvcjK5tNVzzK94mhk+j9RiQ+aWHaTXmOgurhxSp3YbwlRDvOgcq5yPiTz0+kSeK
    ZJcGeJ95bvJ+hJ/UMP0Zx2qB5PElZmiKvfiNqVUk8A8oxLJdBB5eCpqWV6CUqDKQ
    KSQP4sM0mZvQ1Sr4UcACVcYgYnCbTZMWhJTWkrNXqI8TMomekgny3y+d6NX/cFa6
    6jozFIF4HCX5aW8bp8C8vq2tFvFbleQ/Q3CU56EWWKMrOcpmFtRmC18s9biZBVR/
    8QIDAQAB
    -----END PUBLIC KEY-----
    """
    import rsa

    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_pem)
    crypto = rsa.encrypt(source.encode("utf-8"), public_key)
    return base64.b64encode(crypto).decode("utf-8")


async def get_base_token(account, password):
    r = requests.post(
        "https://sg-public-api.hoyolab.com/account/ma-passport/api/webLoginByPassword",
        json={
            "account": encrypt(account),
            "password": encrypt(password),
            "token_type": 6,
        },
        headers={
            "x-rpc-app_id": "c9oqaq3s3gu8",
            "x-rpc-client_type": "4",
            "x-rpc-sdk_version": "2.14.1",
            "x-rpc-game_biz": "bbs_oversea",
            "x-rpc-source": "v2.webLogin",
            "x-rpc-referrer": "https://www.hoyolab.com",
            "Origin": "https://account.hoyolab.com",
            "Referer": "https://account.hoyolab.com/",
        },
    )
    if (
        r.json()["message"]
        == "Too many requests. Please refresh the page and try again later."
    ):
        raise Exception(
            "Too many requests. Please refresh the page and try again later."
        )

    if "Set-Cookie" in r.headers:
        ltuid_v2 = re.search(r"ltuid_v2=([^;]+)", r.headers["Set-Cookie"]).group(1)
        ltoken_v2 = re.search(r"ltoken_v2=([^;]+)", r.headers["Set-Cookie"]).group(1)
        ltmid_v2 = re.search(r"ltmid_v2=([^;]+)", r.headers["Set-Cookie"]).group(1)
        account_id_v2 = re.search(
            r"account_id_v2=([^;]+)", r.headers["Set-Cookie"]
        ).group(1)
        account_mid_v2 = re.search(
            r"account_mid_v2=([^;]+)", r.headers["Set-Cookie"]
        ).group(1)
        cookie_token_v2 = re.search(
            r"cookie_token_v2=([^;]+)", r.headers["Set-Cookie"]
        ).group(1)
        return {
            "ltuid_v2": ltuid_v2,
            "ltoken_v2": ltoken_v2,
            "ltmid_v2": ltmid_v2,
            "account_id_v2": account_id_v2,
            "account_mid_v2": account_mid_v2,
            "cookie_token_v2": cookie_token_v2,
        }
    else:
        raise Exception(
            "Failed to get token: Set-Cookie header not present in response"
        )


async def get_hk4e_token(region, token):
    r = requests.post(
        "https://sg-public-api.hoyoverse.com/common/badge/v1/login/account",
        params={
            "region": region["region"],
            "uid": region["uid"],
            "game_biz": "hk4e_global",
            "lang": "zh-tw",
        },
        cookies=token,
    )
    if "Set-Cookie" in r.headers:
        e_hk4e_token = re.search(
            r"e_hk4e_token=([^;]+)", r.headers["Set-Cookie"]
        ).group(1)
        return e_hk4e_token
    else:
        raise Exception(
            "Failed to get token: Set-Cookie header not present in response"
        )
