from django.core.management.base import NoArgsCommand
import pdb

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        '''
        lists all private keys on private keyring and all public keys on
        public keyring
        '''

        from onboarding.interactive_brokers import encryption as encr
        from onboarding.interactive_brokers import onboarding as onboard
        import gnupg

        gpg = gnupg.GPG(gnupghome=onboard.PATH_TO_FILES + onboard.KEYS[:-1], verbose=True)
        
        private_keys = encr.list_keys(gpg, True)
        public_keys = encr.list_keys(gpg, False)

        print('PRIVATE---------------------------------------')
        print(str(private_keys))
        print('# of PRIVATE keys:' + str(len(private_keys)))
        print('PUBLIC---------------------------------------')
        print(str(public_keys))
        print('# of PUBLIC keys:' + str(len(public_keys)))
        print('---------------------------------------')
       

        

        
        
