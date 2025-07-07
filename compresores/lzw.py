
def lzw_compress(uncompressed: str):
    # Build the dictionary from unique characters to handle any Unicode
    unique_chars = sorted(set(uncompressed))
    dict_size = len(unique_chars)
    dictionary = {ch: i for i, ch in enumerate(unique_chars)}
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            # Output code for w
            if w:
                result.append(dictionary[w])
            # Add wc to the dictionary
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    # Output code for last w
    if w:
        result.append(dictionary[w])
    return result
