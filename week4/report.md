# Tutorial 4

## 1. Considerando os seguintes polinómios:

- $x^3 + x + 1$
- $x^4 + x + 1$
- $x^4 + x^3 + x^2 + 1$

### 1.1 Escolher estados iniciais diferentes e testar os períodos. O que se pode concluir dos LFSRs?

#### Para o polinómio $x^3 + x + 1$:

R0 = 001

```
f(R0) = S3 + S1 = 0 + 1 = 1
R1 = 011

f(R1) = 0 + 1 = 1
R2 = 111

f(R2) = 1 + 1 = 0
R3 = 110

f(R3) = 1 + 0 = 1
R4 = 101

f(R4) = 1 + 1 = 0
R5 = 010

f(R5) = 0 + 0 = 0
R6 = 100

f(R6) = 1 + 0 = 1
R7 = 001
```

O LFSR iniciado com R0 = 001 apresenta um período de 7, o que significa que a sequência gerada se repete após 7 shifts. Este valor coincide com o período máximo possível para um LFSR de 3 bits, que é $2^3 - 1 = 7$.

Como o LFSR atinge o período máximo possível, conclui-se que o polinómio $x^3 + x + 1$ é **primitivo**.  
Isto implica que gera a sequência máxima possível para $n = 3$, independentemente do valor inicial escolhido (exceto o estado nulo, que permanece invariante).  
Ou seja, qualquer valor de partida que pertença ao ciclo levará inevitavelmente à mesma sequência periódica, demonstrando que o polinómio gera todas as combinações possíveis de estados antes de se repetir.

#### Para o polinómio $x^4 + x + 1$:

R0 = 0001

```
f(R0) = S4 + S1 = 1
R1 = 0011

f(R1) = 0 + 1 = 1
R2 = 0111

f(R2) = 0 + 1 = 1
R3 = 1111

f(R3) = 1 + 1 = 0
R4 = 1110

f(R4) = 1 + 0 = 1
R5 = 1101

f(R5) = 1 + 1 = 0
R6 = 1010

f(R6) = 1 + 0 = 1
R7 = 0101

f(R7) = 0 + 1 = 1
R8 = 1011

f(R8) = 1 + 1 = 0
R9 = 0110

f(R9) = 0 + 0 = 0
R10 = 1100

f(R10) = 1 + 0 = 1
R11 = 1001

f(R11) = 1 + 1 = 0
R12 = 0010

f(R12) = 0 + 0 = 0
R13 = 0100

f(R13) = 0 + 0 = 0
R14 = 1000

f(R14) = 1 + 0 = 1
R15 = 0001
```

O LFSR iniciado com R0 = 0001 apresenta um período de 15, o que significa que a sequência gerada se repete após 15 shifts.  
Este valor coincide com o período máximo possível para um LFSR de 4 bits, que é $2^4 - 1 = 15$.

Como o LFSR atinge o período máximo, conclui-se que o polinómio $x^4 + x + 1$ é **primitivo**.  
Isto implica que gera a sequência máxima possível para $n = 4$, independentemente do valor inicial escolhido (exceto o estado nulo).  
Ou seja, qualquer valor de partida que pertença ao ciclo levará inevitavelmente à mesma sequência periódica.

#### Para o polinómio $x^4 + x^3 + x^2 + 1$:

R0 = 0001

```
f(R0) = S4 + S3 + S2 = 0 + 0 + 0 = 0
R1 = 0010

f(R1) = 1
R2 = 0101

f(R2) = 1
R3 = 1011

f(R3) = 0
R4 = 0110

f(R4) = 0
R5 = 1100

f(R5) = 0
R6 = 1000

f(R6) = 1
R7 = 0001
```

O LFSR iniciado com R0 = 0001 apresenta um período de 7, o que significa que a sequência gerada se repete após 7 shifts.  
Este valor **não** coincide com o período máximo possível para um LFSR de 4 bits, que é $2^4 - 1 = 15$.

Como o LFSR não atinge o período máximo, conclui-se que o polinómio $x^4 + x^3 + x^2 + 1$ **não é primitivo**.  
Isto implica que a sequência gerada não é a máxima possível para $n = 4$, ou seja, o polinómio não gera todas as combinações possíveis de estados antes de se repetir.

### 1.2 Qual é o melhor polinómio para um LFSR?

O polinómio ideal para um LFSR é **primitivo**, pois garante o **período máximo possível**, $2^n - 1$.  

Tanto $x^3 + x + 1$ como $x^4 + x + 1$ são primitivos, logo produzem sequências de comprimento máximo.  

No entanto, o polinómio $x^4 + x + 1$ é preferível, pois gera uma sequência mais longa (período 15 em vez de 7), oferecendo melhor cobertura de estados e maior complexidade estatística.

O polinómio $x^3 + x + 1$ continua, contudo, a ser útil em contextos de menor escala, onde um período mais curto e uma implementação mais simples são suficientes.

### 1.3 Verificar quais destes polinómios são irredutíveis no Sage. O que isto diz do polinómio ao ser usado num LFSR?

Para verificar os polinómios irredutíveis com o Sage:

```python
F.<x> = GF(2)[]

p1 = x^3 + x + 1
p2 = x^4 + x + 1
p3 = x^4 + x^3 + x^2 + 1

print("p1 é irredutível:", p1.is_irreducible())
print("p2 é irredutível:", p2.is_irreducible())
print("p3 é irredutível:", p3.is_irreducible())
```

**Output:**
```
p1 é irredutível: True
p2 é irredutível: True
p3 é irredutível: False
```

No contexto dos LFSRs, a irredutibilidade é uma condição **necessária**, mas **não suficiente**, para que um polinómio seja primitivo.  
Polinómios irredutíveis têm maior probabilidade de produzir sequências longas e não repetitivas, uma vez que não podem ser decompostos em polinómios de menor grau.

Se um polinómio **não** for irredutível, ele pode ser decomposto em fatores menores, o que faz com que a sequência gerada tenha ciclos curtos e se repita prematuramente.  
Por exemplo, $x^4 + x^3 + x^2 + 1$ não é irredutível e, de facto, não produz o período máximo, como foi verificado experimentalmente.

Assim, todos os polinómios primitivos são necessariamente irredutíveis, mas o inverso **não** é verdadeiro: nem todo o polinómio irredutível é primitivo.  
Esta distinção explica por que razão alguns polinómios irredutíveis não atingem o período máximo num LFSR.

## 2. Usar uma implementação de RC4 para encriptar um ficheiro

Foi adaptada a implementação disponível no repositório [github.com/DavidBuchanan314/rc4](https://github.com/DavidBuchanan314/rc4), cujo código se encontra no ficheiro `2.py`.

```bash
$ python3 2.py -h 

usage: 2.py [-h] {encrypt,decrypt} input output key

RC4 Encryption/Decryption Tool (GitHub version)

positional arguments:
  {encrypt,decrypt}  Mode: encrypt or decrypt
  input              Input file
  output             Output file
  key                Secret key (string)

options:
  -h, --help         show this help message and exit
```

O ficheiro `mensagem.txt` foi encriptado, dando origem ao ficheiro `mensagemout`:

```bash
python3 2.py encrypt mensagem.txt mensagemout dsjkajkdadsadsjkajkdadsa
```

## 3. Verificar compatibilidade com OpenSSL

Pretende-se verificar se o algoritmo utilizado é compatível com o OpenSSL, ou seja, confirmar que:
1. O OpenSSL consegue desencriptar o ficheiro gerado pela implementação em Python.
2. A implementação em Python consegue desencriptar um ficheiro encriptado com o OpenSSL.

### Desencriptação com OpenSSL

Para desencriptar o ficheiro produzido anteriormente (`mensagemout`) utilizando o OpenSSL, é necessário que a chave seja fornecida em formato hexadecimal.  
Assim, converte-se a chave ASCII usada na encriptação para hexadecimal:

```bash
echo -n "dsjkajkdadsaxxxx" | xxd -p -c 256
```

Obtém-se o seguinte output:

```bash
64736a6b616a6b646164736178787878
```

Agora, podemos utilizar esta chave em formato hexadecimal para desencriptar o ficheiro:

```bash
openssl enc -rc4 -d -in mensagemout -out openssl_decrypted.txt -nosalt -K 64736a6b616a6b646164736178787878 -provider legacy
```

O ficheiro desencriptado (`openssl_decrypted.txt`) contém o mesmo conteúdo original de `mensagem.txt`, confirmando que o OpenSSL conseguiu processar corretamente o ficheiro gerado pela implementação Python.

### Encriptação com OpenSSL e desencriptação com Python

Também é possível realizar o processo inverso, encriptar com o OpenSSL e desencriptar com a implementação Python.  
Para isso, utiliza-se o mesmo formato de chave hexadecimal:

```bash
openssl enc -rc4 -in opensslmessage.txt -out openssl_encrypted.rc4 -nosalt -K 64736a6b616a6b646164736178787878 -provider legacy
```

Obtém-se o ficheiro `openssl_encrypted.rc4`.

De seguida, desencripta-se com a implementação em Python:

```bash
python3 2.py decrypt openssl_encrypted.rc4 python_decrypted.txt dsjkajkdadsaxxxx
```

O ficheiro resultante `python_decrypted.txt` corresponde ao conteúdo original de `opensslmessage.txt`.

## 4. Mostrar com OpenSSL que o ChaCha20 produz um ciphertext repetido se encriptar o ficheiro com a mesma chave e nonce. Porque é que isto acontece?

Utilizamos os seguintes valores para a chave e nonce:

```
KEY=000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
NONCE=000102030405060708090a0b0c
```

Primeiro encriptamos o ficheiro `chacha20plaintext.txt`:

```bash
openssl enc -chacha20 -in chacha20plaintext.txt -out encrypted1.bin -K $KEY -iv $NONCE
```

Encriptamos o mesmo ficheiro com os mesmos valores para a chave e o nonce:

```bash
openssl enc -chacha20 -in chacha20plaintext.txt -out encrypted2.bin -K $KEY -iv $NONCE
```

Verificamos que os ficheiros produzidos são idênticos:

```bash
cmp encrypted1.bin encrypted2.bin && echo "MATCH" || echo "DIFFER"
# OUTPUT
MATCH
```

### Explicação

ChaCha20 é uma steam cipher. Para cada par (chave, nonce) gera um keystream pseudo-aleatório que é XOR com o plaintext para obter o ciphertext:

$
\text{ciphertext} = \text{plaintext} \oplus \text{keystream}.
$

Se a chave e o nonce forem iguais, o keystream será idêntico, produzindo o mesmo ciphertext para o mesmo plaintext.

Por isso nunca se deve reutilizar o nonce com a mesma chave, pois permite que padrões entre mensagens cifradas fiquem expostos e compromete a segurança do sistema.

## 5. Comparar o tamanho do plaintext com o tamanho da ciphertext das questões 2 e 4. O que podemos concluir em comparação com os modos AES-CTR e AES-CBC?

Nos exemplos das questões 2 (RC4) e 4 (ChaCha20), verificamos que o tamanho do ciphertext é igual ao tamanho do plaintext.  
Isto acontece porque stream ciphers, como RC4, ChaCha20 e também AES-CTR, geram um keystream do mesmo tamanho do plaintext e não necessitam de padding.

Por outro lado, block ciphers como AES-CBC podem produzir ciphertexts maiores que o plaintext, uma vez que é necessário adicionar padding para completar os blocos da cifra.
