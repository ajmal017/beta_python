import os
import os.path

from django.test import TestCase
from onboarding.interactive_brokers.compression import zip_file, unzip_file
from onboarding.tests.factories import IndividualFactory,PhoneInfoFactory
import shutil

path_temp = './onboarding/tests/test_files/temp/'
path_test_dir = './onboarding/tests/test_files/test_dir/'
path_test_zip = './onboarding/tests/test_files/test.zip'
class BaseTest(TestCase):
    def setUp(self):
        self.individual_acc = IndividualFactory()
        #phoneInfo = PhoneInfoFactory._create()
        #self.individual_acc.Phones.Phone.
        if not os.path.exists(path_temp):
            os.makedirs(path_temp)

    def test_serializer(self):
        xml = self.individual_acc
        print(xml)
        self.assertTrue(xml!="")

    def test_zip(self):
        zip_file(path_test_dir,path_temp+"test.zip")
        self.assertTrue(os.path.exists(path_temp+"test.zip"))

    def test_unzip(self):

        unzip_file(path_test_zip,  path_temp)
        self.assertTrue(os.path.exists(path_test_dir))
        self.assertTrue(os.path.exists(path_temp+"test_dir/testfile1"))

    def tearDown(self):
        shutil.rmtree(path_temp)

