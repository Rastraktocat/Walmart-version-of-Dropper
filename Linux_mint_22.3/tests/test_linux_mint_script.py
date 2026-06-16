import pytest
from itertools import product
import linux_mint_script

def test_main():

def test_xor_file():

def test_base64_file():

def test_encode_read():

def test_log_file():

def test_parse_args():


@pytest.mark.parametrize("file_path, file_exe_path, configuration_bool, x64_bool, test_output", products(
def test_mingw_run(monkeypatch):
	mingw_run_file_path = []
	mingw_run_file_exe_path = []
	mingw_run_configuration_bool_list = [True, False]
	mingw_run_x64_bool_list = [86, 64]
	mingw_run_test_output_list = [True, False]

