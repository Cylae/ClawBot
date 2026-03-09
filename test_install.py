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
def clean_env():
    # Setup
    test_dir = "test_install_dir"
    if os.path.exists(test_dir):
        # Allow removing readonly files
        for root, dirs, files in os.walk(test_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), stat.S_IRWXU)
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IRWXU)
        shutil.rmtree(test_dir)

    env = os.environ.copy()
    env["INSTALL_DIR"] = test_dir
    env["PATH"] = os.environ.get("PATH", "")

    yield env, test_dir

    # Teardown
    if os.path.exists(test_dir):
        for root, dirs, files in os.walk(test_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), stat.S_IRWXU)
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IRWXU)
        shutil.rmtree(test_dir)

def test_normal_installation(clean_env):
    env, test_dir = clean_env

    result = run_script(env)

    assert result.returncode == 0
    assert os.path.exists(test_dir)
    assert os.path.exists(os.path.join(test_dir, "venv"))
    assert os.path.exists(os.path.join(test_dir, "requirements.txt"))
    assert os.path.exists(os.path.join(test_dir, "main.py"))

def test_idempotency(clean_env):
    env, test_dir = clean_env

    # First run
    result1 = run_script(env)
    assert result1.returncode == 0

    # Second run
    result2 = run_script(env)
    assert result2.returncode == 0
    assert "Le répertoire '{}' existe déjà.".format(test_dir) in result2.stdout
    assert "L'environnement virtuel existe déjà." in result2.stdout

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
    assert "ERREUR: git n'est pas installé." in result.stdout

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
    assert "ERREUR: python3 n'est pas installé." in result.stdout

def test_restricted_permissions(clean_env):
    env, test_dir = clean_env

    # Create the dir and make it read-only
    os.mkdir(test_dir)
    os.chmod(test_dir, stat.S_IRUSR | stat.S_IXUSR) # read and execute only, no write

    result = run_script(env)

    assert result.returncode != 0
    assert not os.path.exists(os.path.join(test_dir, "venv"))
