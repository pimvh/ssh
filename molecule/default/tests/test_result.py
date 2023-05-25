import testinfra


def test_os_release(host):
    """test host release for good measure"""

    assert host.file("/etc/os-release").contains("Ubuntu")


def test_ssh_running(host):
    """test that the fail2ban service is running"""

    assert host.service("ssh").is_running


def test_ssh_certs_created(host):
    """test that the fail2ban jail.local file is created"""

    for crypto in ["rsa", "ecdsa", "ed25519"]:
        assert host.file(f"/etc/ssh/ssh_host_{crypto}_key-cert.pub")


def test_valid_validity_hostkey(host):
    """test that the validate_hostkeys timer is running"""

    assert host.service("validate_hostkeys").is_valid


def test_validity_hostkey(host):
    """test that the validate_hostkeys timer is running"""

    assert host.service("validate_hostkeys.timer").is_running
