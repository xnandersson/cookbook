# Gen generic keys
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:3 -out privkey-A.pem
openssl pkey -in privkey-A.pem -out pubkey-A.pem -pubout

# Sign
openssl dgst -sha1 -sign privkey-A.pem -out signature.bin message.txt
openssl dgst -sha1 -verify pubkey-A.pem -signature signature.bin message.txt

# TODO
# Do dgst in two steps 1. do the hash. 2. encrypt with private key. Should be the same...

# Signature Envelope
openssl smime -sign -in Plaintext.txt -signer alice.crt -inkey alice.pem > Signed-Plaintext.txt
openssl smime -verify -in Signed-Plaintext.txt -signer alice.crt -noverify

# Detached Signature
openssl smime -sign -binary -in Plaintext.txt -signer alice.crt -inkey alice.pem -outform der -out file.p7b
openssl smime -verify -binary -inform der -in file.p7b -content Plaintext.txt -noverify

# Encrypt with smime
openssl smime -encrypt -aes256 -in file.mp4 -binary -outform DER -out file.mp4.dat cert.pem
openssl smime -decrypt -in file.mp4.dat -inform DER -inkey privkey.pem -out file.mp4

# Encrypt std aes-128-cbc
openssl enc -aes-128-cbc -in Plaintext.txt -K ABCDEF12345 -iv ABCDEF > Cipher.txt
openssl enc -d -aes-128-cbc -in Cipher.txt -K ABCDEF12345 -iv ABCDEF

# Detached signature
openssl smime -binary -sign -in Plaintext.txt -signer alice.crt -inkey alice.pem -outform pem -out file.p7b
openssl asn1parse -in file.p7b -dump -i

# This might be wrong. "Signature Envelope" should not have -binary
# Enveloped signature 2
openssl smime -sign -binary -in Plaintext -signer alice.crt -inkey alice.pem -outform der -out file.p7b
openssl smime -verify -binary -inform der -in file.p7b -content Plaintext.txt
openssl smime -verify -binary -inform der -in file.p7b -content Plaintext.txt -noverify

RFC 3370, 3850, 3851, 3852

RFC 5322 (text using electronic mail)

    Enveloped Data

    1. Psedurandom session key
    2. encrypt session key with recipients rsa key
    3. for each recipient, prepare block RecipientInfo that
       contains an identifier of the recipients public-key
       certificate, algorithm identifier to encrypt session
       key and the encrypted session key
    4. encrypt message with session key

    Signed DAta
    1. Select message digest (md5, sha1)
    2. compute the message digest (hash) of the content
    3. encrypt message digest with signers private key
    4. prepare blockl "SignerInfo" that contains signers public
       key certificate, and digest algorithm en the 
       encrypted messaage digest.
Setup
-----

.. code:: bash

  $ for name in alice bob; do openssl req -x509 -newkey rsa:2048 -keyout ${name}.pem -out ${name}.crt -nodes -subj "/C=ES/ST=Andalucia/L=Malaga/O=Openforce AB/OU=Research & Development/CN=${name}"; done


  $ openssl req -x509 -newkey rsa:2048 -keyout alice.pem -out alice.crt -nodes -subj "/C=ES/ST=Andalucia/L=Malaga/O=Openforce AB/OU=Research & Development/CN=alice"
  $ openssl req -x509 -newkey rsa:2048 -keyout bob.pem -out bob.crt -nodes -subj "/C=ES/ST=Andalucia/L=Malaga/O=Openforce AB/OU=Research & Development/CN=bob"
  # Test Message
  $ echo "Hi Alice, this is Bob" > bob2alice.txt

Hash and Encrypt/Decrypt
------------------------

.. code:: bash

  # Hash Text
  $ openssl dgst -sha1 bob2alice.txt
  SHA1(bob2alice.txt)= 3178f625be29524c4c70a4fa39ed8ee9505dce49
  # Hash Binary
  $ openssl dgst -sha1 -out bob2alice.bin -binary bob2alice.txt
  $ stat --format %s bob2alice.bin
  20
  $ xxd -ps bob2alice.bin
  3178f625be29524c4c70a4fa39ed8ee9505dce49

  # Sign
  $ openssl rsautl -encrypt -in bob2alice.bin -out bob2alice.sig -inkey bob.pem
  # This is applicable for later. Create a session key. Encrypt session key.
  $ openssl rsautl -encrypt -in bob2alice.bin -out bob2alice.sig -inkey alice.crt -pubin
  $ stat --format %s bob2alice.sig
  256
  $ openssl rsautl -decrypt -in bob2alice.sig -out bob2alice.unencrypted -inkey alice.pem
  $ stat --format %s bob2alice.unencrypted
  20
  $ diff -u bob2alice.unencrypted bob2alice.bin

Sign a Digest
-------------

.. code:: bash

  # Sign
  $ openssl dgst -sha1 -sign bob.pem -out bob2alice-dgst-sha1.bin bob2alice.bin
  $ stat --format %s bob2alice-dgst-sha1.bin
  256
  # Verify
  $ openssl dgst -sha1 -verify alice.crt -signature bob2alice-dgst-sha1.bin bob2alice.bin
  Verified OK
  # Something similar with encryption.
  $ openssl rsautl -encrypt -in bob2alice.bin -out bob2alice-enc-sha1.bin -inkey alice.pem
  $ stat --format %s bob2alice-enc-sha1.bin

CMS
---

.. code:: bash

  $ openssl cms -in from_bob_to_alice -outform der -encrypt -sign -out from_bob_to_alice -cmsout -inkey bob.pem

S/MIME
------

.. code:: bash

  # This just sign a message.
  $ openssl smime -inkey bob.pem -signer bob.crt -sign -in bob2alice.txt -out bob2alice_1.der -outform der
  $ openssl smime -inkey bob.pem -signer bob.crt -sign -in bob2alice.txt -out bob2alice_1.pem -outform pem 
  $ openssl smime -inkey bob.pem -signer bob.crt -sign -in bob2alice.txt -out bob2alice_1.smime -outform smime
  # This converts smime to pk7. Should in theory look exactly like bob2alice_1.pem, but the very last part of the message differs. Length is the same. Strange.
  $ openssl smime -in bob2alice_1.smime -pk7out

  # Sign + Encrypt
  $ openssl smime -inkey bob.pem -signer bob.crt -sign -in bob2alice.txt -out bob2alice_2.der -outform der -encrypt alice.crt
  $ openssl smime -inkey bob.pem -signer bob.crt -sign -in bob2alice.txt -out bob2alice_2.smime -outform smime -encrypt alice.crt

  $ dumpasn1 from_bob_to_alice.der
  # Decrypt
  $ openssl smime -decrypt -recip alice.pem -in bob2alice_2.smime 
  
