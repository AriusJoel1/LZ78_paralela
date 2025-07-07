# Proyecto — Comparación de Algoritmos de Compresión Multilingüe

Este repositorio compara la eficiencia (tiempo y ratio de compresión) de cuatro algoritmos sin pérdida sobre textos en **Quechua, Español, Inglés, Portugués y Ruso**.

| Algoritmo     | Implementación                  | Lenguaje           | Paralelismo          | Notas                                                      |
| ------------- | ------------------------------- | ------------------ | -------------------- | ---------------------------------------------------------- |
| **LZ78_PAR**  | `compresores/lz78_parallel.py`  | Python             | Sí (multiprocessing) | Diccionario independiente por fragmento, sobrecarga alta.  |
| **LZW**       | `compresores/lzw.py`            | Python             | No                   | Basado en diccionario secuencial.                          |
| **Gzip**      | `gzip` (módulo estándar)        | Binding C (`zlib`) | No                   | LZ77 + Huffman (DEFLATE).                                  |
| **Brotli**    | `brotli` (`pip install brotli`) | Binding C++        | No                   | LZ77 + contextos + Huffman, diccionario global optimizado. |


## 1. Instalación 

```
# Clonar el proyecto
git clone https://github.com/AriusJoel1/LZ78_paralela.git
cd LZ78_paralela

# (opcional) crear un entorno virtual
python -m venv venv
venv\Scripts\activate   # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Ejecución

```
python comparador.py
```

## 3. Resultados y analisis

En el idioma español se incluyó una gran cantidad de texto (más de 20 millones de caracteres) para resaltar con mayor claridad las diferencias entre algoritmos de compresión.
Los demas idiomas si tuvieron una cantidad normal de texto.

![Resultados](https://github.com/AriusJoel1/LZ78_paralela/blob/main/img/paralela.jpg?raw=true)

### Interpretación

- **Brotli** logra ratios absurdamente altos porque incluye un **diccionario global de frases comunes** (120 KB) que reconoce palabras y patrones frecuentes, especialmente en textos web o estructuras repetidas.
  
- **Gzip** (implementado en C como parte del estándar `zlib`) combina **LZ77 + codificación Huffman**, lo que le permite comprimir con alta precisión tanto secuencias repetidas como patrones estadísticos.

- **LZ78_PAR**, aunque más lento que Brotli o Gzip, muestra tiempos significativamente menores que su contraparte secuencial (**LZW**), especialmente en textos grandes. Esto demuestra que la **paralelización del algoritmo es efectiva**, incluso estando 100% escrito en Python.

###  ¿Por qué Brotli y Gzip ganaron?

Porque **la diferencia no está en el algoritmo base, sino en cómo están implementados**:

La razón principal por la que Brotli y Gzip logran resultados muy superiores en tiempo y compresión no es porque sus algoritmos sean conceptualmente mejores, sino porque están implementados en lenguajes de bajo nivel como C y C++, con estructuras optimizadas para velocidad y eficiencia en el manejo de memoria. Brotli, por ejemplo, incorpora un diccionario global preentrenado de frases frecuentes en la web. Esto le permite reconocer patrones comunes y reemplazarlos por referencias muy compactas, logrando ratios de compresión extremadamente altos. Gzip, por su parte, combina técnicas como LZ77 y codificación Huffman, lo que le permite comprimir datos de forma efectiva al identificar repeticiones y asignar códigos más cortos a símbolos frecuentes.

###  Si todo fuera en el mismo lenguaje:

- Si **todos los algoritmos se ejecutaran en Python puro**, **LZ78_parallel sería claramente el más rápido**, gracias a su diseño paralelo.  
- Si por el contrario, **todos se reimplementaran en C++ con compresión estadística adicional**, **LZ78 con Huffman y vectorización podría superar considerablemente a Gzip**, pero eso requeriría una implementación de bajo nivel y muchos recursos.

## 4. Conclusion 
Brotli y Gzip no son más inteligentes, solo están mucho mejor implementados. Mientras tanto, **LZ78_parallel** demuestra que incluso en Python puro, un algoritmo bien paralelizado puede ofrecer muy buen rendimiento.




