import subprocess
import os
import shutil
import stat
import pytest

SCRIPT_PATH = "./install_clawdbot.sh"

def run_script(env=None):
    if env is None:
        env = os.environ.copy()

    result = subprocess.run(
        ["bash", SCRIPT_PATH],
        env=env,
        capture_output=True,
        text=True
    )
    return result

@pytest.fixture
def clean_env(tmp_path):
    test_dir = str(tmp_path / "test_install_dir")
    env = os.environ.copy()
    env["INSTALL_DIR"] = test_dir
    env["PATH"] = os.environ.get("PATH", "")

    yield env, test_dir

def test_normal_installation(clean_env):
    env, test_dir = clean_env

    result = run_script(env)

    assert result.returncode == 0
    assert os.path.exists(test_dir)
    assert os.path.exists(os.path.join(test_dir, "venv"))
    assert os.path.exists(os.path.join(test_dir, "requirements.txt"))
    assert os.path.exists(os.path.join(test_dir, "main.py"))
    assert os.path.exists(os.path.join(test_dir, "venv", ".installed"))

def test_idempotency(clean_env):
    env, test_dir = clean_env

    # First run
    result1 = run_script(env)
    assert result1.returncode == 0

    # Second run
    result2 = run_script(env)
    assert result2.returncode == 0
    assert f"The directory '{test_dir}' already exists." in result2.stdout
    assert "The virtual environment already exists." in result2.stdout
    assert "Dependencies are already up-to-date." in result2.stdout

def test_missing_git(clean_env, tmp_path):
    env, test_dir = clean_env

    # Create a fake bin dir without git
    fake_bin = tmp_path / "fake_bin"
    fake_bin.mkdir()
    os.symlink(shutil.which("python3"), fake_bin / "python3")
    os.symlink(shutil.which("bash"), fake_bin / "bash")
    os.symlink(shutil.which("mkdir"), fake_bin / "mkdir")
    os.symlink(shutil.which("echo"), fake_bin / "echo")
    os.symlink(shutil.which("rm"), fake_bin / "rm")

    env["PATH"] = str(fake_bin)

    result = run_script(env)

    assert result.returncode != 0
    assert "ERROR: git is not installed." in result.stdout

def test_missing_python3(clean_env, tmp_path):
    env, test_dir = clean_env

    # Create a fake bin dir without python3
    fake_bin = tmp_path / "fake_bin"
    fake_bin.mkdir()
    os.symlink(shutil.which("git"), fake_bin / "git")
    os.symlink(shutil.which("bash"), fake_bin / "bash")
    os.symlink(shutil.which("mkdir"), fake_bin / "mkdir")
    os.symlink(shutil.which("echo"), fake_bin / "echo")
    os.symlink(shutil.which("rm"), fake_bin / "rm")

    env["PATH"] = str(fake_bin)

    result = run_script(env)

    assert result.returncode != 0
    assert "ERROR: python3 is not installed." in result.stdout

def test_restricted_permissions(clean_env):
    env, test_dir = clean_env

    # Create the dir and make it read-only
    os.mkdir(test_dir)
    os.chmod(test_dir, stat.S_IRUSR | stat.S_IXUSR) # read and execute only, no write

    result = run_script(env)

    assert result.returncode != 0
    assert not os.path.exists(os.path.join(test_dir, "venv"))
