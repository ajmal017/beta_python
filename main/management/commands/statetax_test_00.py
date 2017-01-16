from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        from main import statetax

        import pdb

        tst_tx_cls = statetax.StateTax('CA', 'Single', 100000.)
        tst = tst_tx_cls.get_state_tax()
        pdb.set_trace()
        
        
