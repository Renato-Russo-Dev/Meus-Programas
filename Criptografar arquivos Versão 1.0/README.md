 <h2 align="center">Um programa que criptografa e descriptografa de arquivos .txt usando Python, com uma interface gráfica em Tkinter.</h2>

O processo é feito com hash SHA-256 para garantir uma chave de 256 bits, que é usada junto com o algoritmo AES.

A criptografia é realizada usando o algoritmo AES em modo GCM, com uma chave que é derivada do próprio arquivo. 

Fiz esse programa para inicialmente criptografar um arquivo de texto comum do bloco de notas (.txt) e penso futuramente em extender as opções pra que eu possa conseguir criptografar outros tipos de arquivos e de diversos tamanhos.

Para funcionar é necessário que você tenha esse pacote instalado no seu Pyhton.

    pip install cryptography
