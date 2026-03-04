# -*- coding: utf-8 -*-
"""
AES 加解密工具
替代原 AESUtil.cs，使用标准 AES-CBC-PKCS7
"""
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from config import settings


def aes_encrypt(plain_text: str, key: str = None, iv: str = None) -> str:
    """
    AES-CBC 加密，返回 Base64 字符串
    """
    key = (key or settings.AES_KEY).encode("utf-8")[:16]
    iv = (iv or settings.AES_IV).encode("utf-8")[:16]
    data = plain_text.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(encrypted).decode("utf-8")


def aes_decrypt(cipher_text: str, key: str = None, iv: str = None) -> str:
    """
    AES-CBC 解密，输入 Base64 字符串，返回明文
    """
    key = (key or settings.AES_KEY).encode("utf-8")[:16]
    iv = (iv or settings.AES_IV).encode("utf-8")[:16]
    encrypted = base64.b64decode(cipher_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode("utf-8")


def decrypt_and_parse(encrypted_value: str, model_class=None):
    """
    解密并解析 JSON 为指定模型
    替代原控制器中的: JsonConvert.DeserializeObject<T>(AESUtil.ToSimplifyDecrypt(postData.value))
    """
    json_str = aes_decrypt(encrypted_value)
    data = json.loads(json_str)
    if model_class:
        return model_class(**data)
    return data
