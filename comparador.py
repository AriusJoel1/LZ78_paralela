import os
import time
import csv


from compresores.lz78_parallel import lz78_parallel_compress
from compresores.lzw import lzw_compress
from compresores.gzip_brotli import gzip_compress, brotli_compress

TEXT_DIR = 'textos'
RESULT_CSV = 'resultados.csv'

ALGORITHMS = [
    ('LZ78_PAR', lambda text: lz78_parallel_compress(text)),
    ('LZW', lambda text: lzw_compress(text)),
    ('GZIP', lambda text: gzip_compress(text.encode('utf-8'))),
    ('BROTLI', lambda text: brotli_compress(text.encode('utf-8'))),
]


def measure(text: str, func):
    t0 = time.perf_counter()
    compressed = func(text)
    t1 = time.perf_counter()
    # Estimate compressed size: list of ints or tuples assume 2 bytes per code
    if isinstance(compressed, list):
        comp_size = len(compressed) * 2
    else:
        comp_size = len(compressed)
    return t1 - t0, comp_size


def main():
    results = []
    for fname in os.listdir(TEXT_DIR):
        if not fname.endswith('.txt'): continue
        lang = os.path.splitext(fname)[0]
        path = os.path.join(TEXT_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        orig_size = len(text.encode('utf-8'))
        for name, func in ALGORITHMS:
            elapsed, comp_size = measure(text, func)
            ratio = orig_size / comp_size if comp_size else 0
            results.append((lang, name, f'{elapsed:.6f}', orig_size, comp_size, f'{ratio:.2f}'))
    # Write CSV
    with open(RESULT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Idioma', 'Algoritmo', 'Tiempo_s', 'Tamaño_orig', 'Tamaño_comp', 'Ratio'])
        writer.writerows(results)

    print("{:<10} | {:<10} | {:<9} | {:<13} | {:<13} | {:<5}".format(
        "Idioma", "Algoritmo", "Tiempo_s", "Tamaño_orig", "Tamaño_comp", "Ratio"))
    print("-" * 70)
    for row in results:
        print("{:<10} | {:<10} | {:<9} | {:<13} | {:<13} | {:<5}".format(*row))

if __name__ == '__main__':
    main()
