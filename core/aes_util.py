# -*- coding: utf-8 -*-
"""
AES 加解密工具
移植自 C# CommercialApi.GeneralMethod.AES.AESUtil

重要说明：
C# 中 ToSimplifyEncrypt/ToSimplifyDecrypt 调用的是自定义的 CryptoJS 模拟类，
其中 aesBlockEncrypt/aesBlockDecrypt 使用的是简单 XOR（非标准 AES），
配合 CBC 模式和 PKCS7 填充。

同时保留标准 AES-CBC 解密方法（ToEncrypt/ToDecrypt 使用标准 AES）。
"""
import base64
import json

# AES 密钥和 IV（与 C# Web.config / AppSettings.cs 一致）
AES_KEY = "7tRqYw4XgL9Kv2Ef"
AES_IV = "P5mDn8ZsB3HjT6cN"


# ===== 简化版（兼容前端JS，XOR-CBC）=====
# 对应 C# 的 ToSimplifyEncrypt / ToSimplifyDecrypt

def _xor_block(a: bytes, b: bytes) -> bytes:
    """XOR 两个等长字节块"""
    return bytes(x ^ y for x, y in zip(a, b))


def _pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """PKCS7 填充"""
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len] * pad_len)


def _pkcs7_unpad(data: bytes) -> bytes:
    """PKCS7 去填充"""
    if not data:
        raise ValueError("输入数据为空")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16 or len(data) < pad_len:
        raise ValueError(f"无效的填充: pad_len={pad_len}, data_len={len(data)}")
    for i in range(len(data) - pad_len, len(data)):
        if data[i] != pad_len:
            raise ValueError(f"填充字节不一致，位置 {i}")
    return data[:-pad_len]


def simplify_encrypt(plain_text: str) -> str:
    """加密（XOR-CBC，兼容小程序 JS），返回 Base64"""
    key = AES_KEY.encode("utf-8")
    iv = AES_IV.encode("utf-8")
    data = plain_text.encode("utf-8")
    padded = _pkcs7_pad(data)
    encrypted = bytearray()
    prev = iv
    for i in range(0, len(padded), 16):
        block = padded[i:i + 16]
        xored = _xor_block(block, prev)
        enc_block = _xor_block(xored, key)
        encrypted.extend(enc_block)
        prev = enc_block
    return base64.b64encode(bytes(encrypted)).decode("ascii")


def simplify_decrypt(cipher_base64: str) -> str:
    """解密（XOR-CBC，兼容小程序 JS），输入 Base64，返回明文"""
    try:
        key = AES_KEY.encode("utf-8")
        iv = AES_IV.encode("utf-8")
        cipher_bytes = base64.b64decode(cipher_base64)
        decrypted = bytearray()
        prev = iv
        for i in range(0, len(cipher_bytes), 16):
            block = cipher_bytes[i:i + 16]
            dec_block = _xor_block(block, key)
            xored = _xor_block(dec_block, prev)
            decrypted.extend(xored)
            prev = block
        unpadded = _pkcs7_unpad(bytes(decrypted))
        return unpadded.decode("utf-8")
    except Exception as e:
        raise ValueError(f"XOR-CBC 解密失败: {e}")


# ===== 标准 AES-CBC（对应 C# 的 ToEncrypt/ToDecrypt）=====

def aes_encrypt(plain_text: str, key: str = None, iv: str = None) -> str:
    """标准 AES-CBC 加密，返回 Base64"""
    from Crypto.Cipher import AES as _AES
    from Crypto.Util.Padding import pad
    key_bytes = (key or AES_KEY).encode("utf-8")[:16]
    iv_bytes = (iv or AES_IV).encode("utf-8")[:16]
    data = plain_text.encode("utf-8")
    cipher = _AES.new(key_bytes, _AES.MODE_CBC, iv_bytes)
    encrypted = cipher.encrypt(pad(data, _AES.block_size))
    return base64.b64encode(encrypted).decode("utf-8")


def aes_decrypt(cipher_text: str, key: str = None, iv: str = None) -> str:
    """标准 AES-CBC 解密，输入 Base64，返回明文"""
    from Crypto.Cipher import AES as _AES
    from Crypto.Util.Padding import unpad
    key_bytes = (key or AES_KEY).encode("utf-8")[:16]
    iv_bytes = (iv or AES_IV).encode("utf-8")[:16]
    encrypted = base64.b64decode(cipher_text)
    cipher = _AES.new(key_bytes, _AES.MODE_CBC, iv_bytes)
    decrypted = unpad(cipher.decrypt(encrypted), _AES.block_size)
    return decrypted.decode("utf-8")


# ===== 入口方法 =====

def decrypt_post_data(post_data: dict) -> dict:
    """
    解密 POST 请求中的 value 字段
    模式: JObject.Parse(AESUtil.ToSimplifyDecrypt(postData.value))
    """
    if not post_data or "value" not in post_data:
        raise ValueError("请求数据中缺少 value 字段")
    decrypted_text = simplify_decrypt(post_data["value"])
    return json.loads(decrypted_text)


def decrypt_and_parse(encrypted_value: str, model_class=None):
    """解密并解析 JSON 为指定模型"""
    json_str = simplify_decrypt(encrypted_value)
    data = json.loads(json_str)
    if model_class:
        return model_class(**data)
    return data
