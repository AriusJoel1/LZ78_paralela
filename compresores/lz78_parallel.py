from multiprocessing import Pool, cpu_count

def lz78_compress(data: str):
    dict_size = 1
    dictionary = {"": 0}
    w = ""
    output = []
    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            output.append((dictionary[w], c))
            dictionary[wc] = dict_size
            dict_size += 1
            w = ""
    if w:
        output.append((dictionary[w], ''))
    return output

def compress_chunk(chunk):
    return lz78_compress(chunk)

def lz78_parallel_compress(data: str, processes: int = None):
    # Split data into roughly equal chunks
    nprocs = processes or cpu_count()
    size = len(data)
    chunk_size = size // nprocs
    chunks = [data[i * chunk_size : (i + 1) * chunk_size] for i in range(nprocs)]
    # Last chunk includes the remainder
    if size % nprocs:
        chunks[-1] += data[nprocs * chunk_size:]
    with Pool(nprocs) as pool:
        results = pool.map(compress_chunk, chunks)
    # Flatten results
    flat = [item for sublist in results for item in sublist]
    return flat