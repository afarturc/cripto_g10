# Tutorial 3

## 1. Usar Python para encriptar e desencriptar o ficheiro em modo AES-CBC

O código foi guardado em `aes_cbc.py`.

```bash
$ python3 aes_cbc.py -h

usage: aes_cbc.py [-h] [-o OUTPUT] [-k KEY] {encrypt,decrypt} input

Encrypt or decrypt text files using AES CBC

positional arguments:
  {encrypt,decrypt}    Operation mode
  input                Input file

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output file (default: input + .enc or .dec)
  -k, --key KEY        Key file (default: random key, saved to key.bin)

Examples:
  python aes_cbc.py encrypt input.txt -o encrypted.bin -k mykey.bin
  python aes_cbc.py decrypt encrypted.bin -o output.txt -k mykey.bin
```

Foram gerados os ficheiros `enc_file_python.py`, `dec_file_python.py` e `key.bin`.

## 2. Repetir o processo com OpenSSL

Para encriptar:

```bash
openssl enc -aes-256-cbc -e -in file.txt -out enc_file_cbc.bin -pass pass:password -pbkdf2
```

Para desencriptar:

```bash
openssl enc -aes-256-cbc -d -in enc_file_cbc.bin -out dec_file_cbc.txt -pass pass:password -pbkdf2
```

## 3. Após encriptação, editar o ficheiro para alterar o valor de um byte e desencriptar novamente

### 3.1. O que aconteceu? Quanto do ficheiro foi corrompido?

A desencriptação está correta exceto numa pequena parte a meio do texto.

No modo CBC, cada Pₙ depende apenas de Cₙ e Cₙ₋₁:

```
Pₙ = D(K, Cₙ) ⊕ Cₙ₋₁
```

Apenas dois blocos são afetados, o bloco alterado e o seguinte. Todo o texto anterior e posterior a estes dois blocos é recuperável.

### 3.2. É possível recuperar um ficheiro encriptado com CBC se o IV e o primeiro bloco do ciphertext forem corrompidos?

Sim, parcialmente. Todos os blocos a partir de P₂ são recuperáveis.

- P₀ é irrecuperável: `P₀ = D(K, C₀) ⊕ IV` → faltam IV e C₀
- P₁ é irrecuperável: `P₁ = D(K, C₁) ⊕ C₀` → falta C₀
- P₂ é recuperável: `P₂ = D(K, C₂) ⊕ C₁` → C₁ e C₂ existem
- Pₙ (n > 2) é recuperável pela mesma razão

### 3.3. É possível recuperar o ficheiro se durante uma transmissão satélite o primeiro bit do ciphertext não for entregue?

Seja Cₘ o bloco ao qual pertence o bit perdido.

**Se soubermos qual é Cₘ:**
- Blocos anteriores a Cₘ: recuperáveis
- Pₘ e Pₘ₊₁: irrecuperáveis
- Blocos posteriores a Pₘ₊₁: recuperáveis

**Se não soubermos qual é Cₘ:**
- A perda de um bit causa desalinhamento em cascata
- Blocos até Cₘ₋₁: recuperáveis
- Blocos de Cₘ até ao fim: irrecuperáveis

### 3.4. Encriptaste uma mensagem muito grande com AES-CBC e descobres que o primeiro byte estava errado ("hello" em vez de "Hello"). Podes modificar o ciphertext existente ou tens de re-encriptar tudo?

Não é necessário re-encriptar tudo. Apenas os blocos a partir do bloco modificado (inclusive) precisam de ser re-encriptados.

No CBC, `Cₙ = E(K, Pₙ ⊕ Cₙ₋₁)`. Alterar Pₘ implica alterar Cₘ, que por sua vez afeta Cₘ₊₁, e assim sucessivamente até ao fim. Os blocos anteriores a Cₘ não são afetados.

## 4. Repetir o exercício com modo CTR. Quais são as diferenças?

Para encriptar e desencriptar:

```bash
openssl enc -aes-256-ctr -e -in file.txt -out enc_file_ctr.bin -pass pass:password -pbkdf2
openssl enc -aes-256-ctr -d -in enc_file_ctr.bin -out dec_file_ctr.txt -pass pass:password -pbkdf2
```

### 4.1. O que aconteceu? Quanto do ficheiro foi corrompido?

A desencriptação está correta exceto no bloco que contém o byte alterado.

No modo CTR, cada bloco é independente: `Pₙ = Cₙ ⊕ E(K, Counter + n)`

Apenas um bloco é afetado. Todo o resto do ficheiro é recuperável.

### 4.2. É possível recuperar um ficheiro encriptado com CTR se o primeiro bloco do ciphertext for corrompido?

Sim, parcialmente. Todos os blocos exceto P₀ são recuperáveis, devido à independência dos blocos no modo CTR.

O modo CTR não utiliza IV da mesma forma que o CBC.

### 4.3. É possível recuperar o ficheiro se durante uma transmissão satélite o primeiro bit do ciphertext não for entregue?

Seja Cₘ o bloco ao qual pertence o bit perdido.

**Se soubermos qual é Cₘ:** Todos os blocos exceto Pₘ são recuperáveis.

**Se não soubermos qual é Cₘ:** Tal como no CBC, o desalinhamento propaga-se. Blocos até Cₘ₋₁ são recuperáveis, de Cₘ até ao fim são irrecuperáveis.

### 4.4. É possível modificar o ciphertext existente ao alterar um byte do plaintext, ou é necessário re-encriptar tudo?

Apenas o bloco que contém o byte modificado precisa de ser re-encriptado.

No CTR, `Cₙ = Pₙ ⊕ E(K, Counter + n)`. Como os blocos são independentes, alterar Pₘ apenas afeta Cₘ. Nenhum dos outros blocos precisa de ser re-encriptado.

## CBC vs CTR

A principal diferença entre CBC e CTR é que no CBC os blocos dependem uns dos outros, enquanto no CTR os blocos são independentes. Isto torna o CTR paralelizável e com propagação mínima de erros.
