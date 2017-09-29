import unittest
import os
from projects.models import Project
from projects import app


class FairTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        app.config['DATA_FOLDER'] = os.getcwd() + "/tests/data"
        app.config['UPLOAD_FOLDER'] = os.getcwd() + "/tests/images"
        app.config['WTF_CSRF_ENABLED'] = False
        # Override default DB setting -> use a testing db instead of the default
        app.config['DB'] = app.config['DATA_FOLDER'] + "/dataset_test"
        self.app = app.test_client()

    def tearDown(self):
        pass
        # Clean up
        #Project.clear()
        #self.assertTrue(len(Project.get_all()) == 0)




if __name__ == '__main__':
    unittest.main()