import pytest

from pxpilot.notifications import NotificationManager


class MockNotifier:
    def __init__(self, config):
        self.config = config

    def create_message(self):
        return MockMessage()


class MockMessage:
    def add_header(self, start_time):
        self.start_time = start_time


NOTIFIER_TYPES = {
    'email': MockNotifier,
    'sms': MockNotifier
}


@pytest.fixture
def notifier_config(request):
    tg = {"token": "token_value", "chat_id": "chan_id_value"}
    mail = {
        "smtp_server": "",
        "smtp_port": "",
        "smtp_user": "",
        "smtp_password": "",
        "from_email": "",
        "to_email": ""
    }

    if request.param == "disabled":
        mail["disabled"] = True

    config = [
        {"telegram": tg},
        {"email": mail}
    ]
    return config


@pytest.fixture
def notification_manager(notifier_config):
    return NotificationManager(notifier_config, {"telegram": MockNotifier, "email": MockNotifier})


@pytest.fixture
def notification_manager_one(notifier_config):
    return NotificationManager(notifier_config, {"telegram": MockNotifier})


@pytest.mark.parametrize("notifier_config", [""], indirect=True)
def test_init(notification_manager, notifier_config):
    assert len(notification_manager._notifiers) == 2
    assert len(notification_manager._message_to_notifier_map) == 2


@pytest.mark.parametrize("notifier_config", ["disabled"], indirect=True)
def test_init_disabled(notification_manager, notifier_config):
    assert len(notification_manager._notifiers) == 1
    assert len(notification_manager._message_to_notifier_map) == 1


@pytest.mark.parametrize("notifier_config", [""], indirect=True)
def test_asa(notification_manager_one, notifier_config):
    assert len(notification_manager_one._notifiers) == 1
    assert len(notification_manager_one._message_to_notifier_map) == 1
