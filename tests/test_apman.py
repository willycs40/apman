import pytest
import os
from apman.packagemanager import PackageManager
from apman.utilities import cd


here = os.path.dirname(os.path.abspath(__file__))

# content of test_class.py
class TestClass:

#    def test_utilities_cd(self):
#        os.getcwd()

    def test_missing_package_configs(self):

        config_path = os.path.join(here,'test_configs','missing_parameters','config')

        with pytest.raises(Exception) as excinfo:
            package = PackageManager(config_path)
        
        assert 'missing from package' in str(excinfo.value)

    def test_package_timeout(self):

        config_path = os.path.join(here,'test_configs','timeout','config')
        package = PackageManager(config_path)
        package.run_package(log_run_to_db = False, send_notification_emails = False, print_notification = False)

        assert package._script_thread.script_timed_out == True

    def test_package_error(self):

        config_path = os.path.join(here,'test_configs','error','config')
        package = PackageManager(config_path)
        package.run_package(log_run_to_db = False, send_notification_emails = False, print_notification = False)

        assert package._script_thread.script_exceptioned == True

    def test_package_success(self):

        config_path = os.path.join(here,'test_configs','success','config')
        package = PackageManager(config_path)
        package.run_package(log_run_to_db = False, send_notification_emails = False, print_notification = False)

        assert package._script_thread.script_exceptioned == False
        assert package._script_thread.script_timed_out == False

