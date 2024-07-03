# Abyss
Abyss is a chat application that uses RSA and Fernet encryptions to protect your data.

# How does it work?
Your login, password and host info are stored in a fernet-encrypted config file, so it will be way harder to steal them, even if someone has direct access to your file system.
When client connects to server, they send each other RSA public keys to estabilish secure data transfer. There are used unique encryption keys for each client. And every time client or server restarts, it generates new RSA keys. So, even if clients or servers keys get cracked(which is very unlikely), it will not lead to serious data leaks.

# Why to use Abyss?
Almost every popular messenger belongs to a commercial corporation, and its servers(and clients, likely) are NOT open-source. Why is it bad? It means, that they likely will collect your personal info and sell it to third-parties and governments. While all Abyss software is completely free and open-source, so you can setup your own servers for you and your friends/family/colleagues.

# Server
Server-side software needs python to be installed in your system.
  1. To install server, download and run server-setup.py.
  2. To run it, run ```python3 server.py```.
  3. To manually add user to database, run ```python3 reg_user.py```.

# Client
Client-side software need python too.
  1. To install client, simply run client-setup.py and follow the steps.
  2. Before connecting to server, you'll need to edit client configuration. Do it with ```python3 config.py```.
  3. If you haven't yet registered on the server, run ```python3 client.py register registration_key```(replace "registration_key" with servers registration key). Where to get registration key? You may ask server administrator or the person who invited you for it.
  4. To start normal session(no registration, just login), run ```python3 client.py```.

# Feedback
Please, comment, ask your questions and suggest edits! ;)
