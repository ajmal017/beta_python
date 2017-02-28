from django.core.management.base import NoArgsCommand
from main import constants
import pdb

class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        '''
        for given xml file, prints all elements of xml tree preceded by indices to showing nesting level
        '''

        from onboarding.interactive_brokers import onboarding as onb
        from onboarding.interactive_brokers import onboarding_helpers as onb_help
        import xml.etree.ElementTree as ET
        
        tree = ET.parse(onb.PATH_TO_FILES + onb.DOCUMENTS + 'Testers_20160310_121317.xml')
        root = tree.getroot()
        onb_help.show_tree(root) 
        
       

        

        
        
