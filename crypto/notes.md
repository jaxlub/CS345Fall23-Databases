# Notes and Commands from Key Crypto Class
great practice is posting your key generation and private keys on github :)
```
# make private key
openssl genrsa -out pub_priv.key 3072   

# view private key
openssl rsa -text -in pub_priv.key | less

# make public key
penssl rsa -in pub_priv.key -pubout -out public_key.key

# encrypt message using public key
openssl pkeyutl -encrypt -pubin -inkey public_key.key -in m.txt -out m_encrypted.bin

# put in base64 text file from binary to send over email
openssl base64 -in m_encrypted.bin -out m_encrypted.txt  
# now message is encrypted and can be sent

# convert back to bin for decryption
openssl base64 -d -in m_encrypted.txt -out temp.bin

# decrypt from bin to message
openssl pkeyutl -decrypt -inkey pub_priv.key -in temp.bin -out decoded.txt
```

Connecting to remote VM
```
ssh-keygen -C jalubk
ssh -i gcp jalubk@34.122.67.118
sudo apt install postgresql-client
```
Connecting to remote postgres
```
psql -U postgres -h 34.118.200.180
```
Then create user role with db creation allowed and role generation blocked
```
create role jalubk login password 'cs345-jalubk!' createdb nocreaterole;
create database jalubk;
select rolname,rolpassword from pg_authid; # view passwords
select sha256('hello'); # secure hash algo
select encode(sha256('hello'), 'base64'); # base 64 hash
openssl dgst -sha256 mobydick.txt # secure hash with openssl
```

```
# Signing
openssl dgst -binary -sha256 mobydick.txt > mobydick.hash # binary output
openssl pkeyutl -sign -in mobydick.hash -inkey pub_priv.key -pkeyopt digest:sha256 -keyform PEM -out mobydick.txt.sign
# Then send file and signature to someone 
# to verify Signature
openssl pkeyutl -verify -in mobydick.hash -sigfile mobydick.txt.sign -pubin -inkey public_key.key -pkeyopt digest:sha256 -keyform PEM
```

```
# Get IP Address of Machine
curl http://checkip.amazonaws.com
```

Symmetric Encrypting/decrypting of Mobydick
```
openssl enc -aes-256-ctr -pass file:password.txt -pbkdf2 -e -base64 -in mobydick.txt -out encrypted_mobydick.txt

openssl enc -aes-256-ctr -pass file:password.txt -pbkdf2 -d -base64 -in encrypted_mobydick.txt -out decrypted_mobydick.txt
```