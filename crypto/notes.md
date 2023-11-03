# Notes and Commands from Key Crypto Class
great practice is posting your key generation on github :)
```
# make private key
openssl genrsa -out pub_priv.key 3072   

# view private key
openssl rsa -text -in pub_priv.key | less

# make public key
penssl rsa -in pub_priv.key -pubout -out public_key.key

# encrypt message using public key
openssl pkeyutl -encrypt -pubin -inkey public_key.key -in m.txt -out m_encrypted.bin
```