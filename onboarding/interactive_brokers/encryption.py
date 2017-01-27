import gnupg

def encrypt(self, files):
    gpg = gnupg.GPG(gnupghome='\onboarding\interactive_brokers\Files\IBKR_CI.PubKey.asc')
    encrypted = gpg.encrypt_file(files, recipients='mail@mail.com', passphrase='secret')
    f = tempfile.NamedTemporaryFile(delete=False)
    name = f.name
    f.write(encrypted.data)
    f.close()
    return open(name, 'r+b')

def decrypt(self, files):
    gpg = gnupg.GPG(gnupghome='/home/XXXX/.gnupg')
    result = gpg.decrypt(files.content).data
    return result