import testinfra


def test_os_release(host):
    """test host release for good measure"""

    assert host.file("/etc/os-release").contains("Ubuntu")


def test_ssh_running(host):
    """test that the ssh service is running"""

    assert host.service("ssh").is_running


def test_ssh_certs_created(host):
    """test that the ssh certificates are created"""

    for crypto in ["rsa", "ecdsa", "ed25519"]:
        assert host.file(f"/etc/ssh/ssh_host_{crypto}_key-cert.pub")


def test_auth_principals_created(host):
    """test that the auth principals are added correctly"""

    with host.sudo():
        assert host.file("/etc/ssh/auth_principals/ansible")
        assert host.file("/etc/ssh/auth_principals/ansible").contains("testing")


def test_sshd_config_file_created(host):
    """test that the sshd_config_file is generated in the correct spot"""

    with host.sudo():
        assert host.file("/etc/ssh/ssh_config.d/10-sshd_config")


def test_validate_hostkeys_script_exists(host):
    """test that the validate_hostkeys script is present"""

    with host.sudo():
        assert host.file("/usr/local/bin/validate_hostkeys")


def test_validate_hostkey_timer_runner(host):
    """test that the validate_hostkeys timer is running"""

    with host.sudo():
        assert host.service("validate_hostkeys.timer").is_running
