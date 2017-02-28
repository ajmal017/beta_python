from django.core.management.base import NoArgsCommand
from main import constants
from main import abstract
import pandas as pd
import os
import pdb

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        '''
        recursively deletes uncompressed, zipped and encrypted directories
        used during creatiion of a file for IB onboarding
        '''

        from onboarding.interactive_brokers import onboarding as onboard

        import shutil

        dirs = [onboard.PATH_TO_FILES + onboard.UNCOMPRESSED,
                onboard.PATH_TO_FILES + onboard.ZIPPED,
                onboard.PATH_TO_FILES + onboard.ENCRYPTED]

        for d in dirs:
            if os.path.exists(d):
                shutil.rmtree(d)
