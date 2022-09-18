import os
import pytest
import dotenv


# dotenv.load_dotenv(os.path.join("tests", "test.env"))
# dotenv.
@pytest.fixture
def custom_env(request):
    env: dict[str] = request.param
    old_env = {}
    for key, val in env.items():
        old_env[key] = os.environ[key]
        if val == None:
            del os.environ[key]
        else:
            os.environ[key] = val
    yield
    for key, val in env.items():
        os.environ[key] = old_env[key]
