import gzip
import brotli

def gzip_compress(data: bytes, compresslevel: int = 9) -> bytes:
    return gzip.compress(data, compresslevel)


def brotli_compress(data: bytes, quality: int = 11) -> bytes:
    return brotli.compress(data, quality=quality)
