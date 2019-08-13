.. code:: bash

  $ openssl req -x509 -newkey rsa:2048 -keyout key.pem -out mycert.crt -nodes -config req.cnf
  $ openssl x509 -in mycert.crt -out mycert.des -outform des
