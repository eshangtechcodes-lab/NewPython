"""
DES 加解密工具 — 平移自 C# RealEstate_System.cs
算法: DES CBC 模式 (PKCS5 填充)
密钥/IV: !(&*)@@$ (8字节 ASCII)
编码: GBK (对应 C# Encoding.Default 在中文 Windows 上的行为)
加密输出: 十六进制大写字符串
"""
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# C# 源码中的 DES 密钥（与 IV 相同）
_DES_KEY = b'!(&*)@@$'
_DES_IV = b'!(&*)@@$'
# C# Encoding.Default 在中文 Windows 上对应 GBK
_ENCODING = 'gbk'


def des_encrypt(plain_text: str) -> str:
    """
    DES 加密 — 对齐 C# ToEncrypt()
    输入明文字符串，返回十六进制大写字符串
    """
    if not plain_text:
        return plain_text or ""
    # C#: Encoding.Default.GetBytes(value)
    data = plain_text.encode(_ENCODING)
    cipher = DES.new(_DES_KEY, DES.MODE_CBC, _DES_IV)
    encrypted = cipher.encrypt(pad(data, DES.block_size))
    # C#: foreach (byte b) { AppendFormat("{0:X2}", b) }
    return encrypted.hex().upper()


def des_decrypt(cipher_text: str) -> str:
    """
    DES 解密 — 对齐 C# ToDecrypt()
    输入十六进制字符串，返回解密后的明文
    """
    if not cipher_text:
        return cipher_text or ""
    # C#: hex string → byte array
    data = bytes.fromhex(cipher_text)
    cipher = DES.new(_DES_KEY, DES.MODE_CBC, _DES_IV)
    decrypted = unpad(cipher.decrypt(data), DES.block_size)
    # C#: Encoding.Default.GetString(ms.ToArray())
    return decrypted.decode(_ENCODING)


def des_encrypt_id(merchant_id) -> str:
    """
    加密 MERCHANTS_ID — 将数字ID转为字符串再加密
    对齐 C# value.ToEncrypt() 其中 value 为 object → value.ToString().ToEncrypt()
    MERCHANTS_ID 存储为负数（如 -2846），C# 转字符串后为 "-2846"
    """
    if merchant_id is None:
        return None
    return des_encrypt(str(int(merchant_id)))
