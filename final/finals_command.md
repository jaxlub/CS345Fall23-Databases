# Asymetric
```
openssl genrsa -out private.key 3072   

openssl rsa -text -in private.key | less

openssl rsa -in private.key -pubout -out public_key.key

openssl pkeyutl -encrypt -pubin -inkey public_key.key -in m.txt -out m_encrypted.bin

openssl base64 -in m_encrypted.bin -out m_encrypted.txt  

->

openssl base64 -d -in m_encrypted.txt -out temp.bin

openssl pkeyutl -decrypt -inkey private.key -in temp.bin -out decoded.txt
```
## SSH KeyGen
```
ssh-keygen -C jalubk
ssh -i gcp jalubk@34.122.67.118
sudo apt install postgresql-client
```

## SHA256
```
select sha256('hello'); # secure hash algo
select encode(sha256('hello'), 'base64'); # base 64 hash
openssl dgst -sha256 mobydick.txt # secure hash with openssl
```

## Sign

openssl dgst -binary -sha256 mobydick.txt > **mobydick.hash**

openssl pkeyutl **-sign** -in mobydick.hash -inkey pub_priv.key -pkeyopt digest:sha256 -keyform PEM -out mobydick.txt.sign

->

openssl pkeyutl **-verify** -in mobydick.hash -sigfile mobydick.txt.sign -pubin -inkey public_key.key -pkeyopt digest:sha256 -keyform PEM




## Symmetric 
```
openssl enc -aes-256-ctr -pass file:password.txt -pbkdf2 -e -base64 -in mobydick.txt -out encrypted_mobydick.txt

openssl enc -aes-256-ctr -pass file:password.txt -pbkdf2 -d -base64 -in encrypted_mobydick.txt -out decrypted_mobydick.txt
```