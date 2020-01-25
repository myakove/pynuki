# coding: utf-8

from . import constants as const
from .utils import logger


class NukiDevice(object):
    def __init__(self, bridge, json):
        self._bridge = bridge
        self._json = json

    @property
    def name(self):
        return self._json.get("name")

    @property
    def nuki_id(self):
        return self._json.get("nukiId")

    @property
    def battery_critical(self):
        return self._json.get("batteryCritical")

    @property
    def firmware_version(self):
        return self._json.get("firmwareVersion")

    @property
    def state(self):
        return self._json.get("state")

    @property
    def state_name(self):
        return self._json.get("stateName")

    @property
    def device_type(self):
        dev = self._json.get("deviceType")

    @property
    def device_type_str(self):
        dev = self.device_type
        if dev == const.DEVICE_TYPE_LOCK:
            return "lock"
        elif dev == const.DEVICE_TYPE_OPENER:
            return "opener"
        logger.error("Unknown device type: {dev}")
        return "UNKNOWN"

    def update(self, aggressive=False):
        """
        Update the state of the Nuki device
        :param aggressive: Whether to aggressively poll the Bridge. If set to
        True, this will actively query the Lock, thus using more battery.
        :type aggressive: bool
        """
        if aggressive:
            data = self._bridge.lock_state(self.nuki_id)
            if not data["success"]:
                logger.warning(
                    f"Failed to update the state of device {self.nuki_id}"
                )
            self._json = {k: v for k, v in data.items() if k != "success"}
        else:
            data = [
                l
                for l in self._bridge._get_devices(self.device_type)
                if l.nuki_id == self.nuki_id
            ]
            assert data, (
                "Failed to update data for lock. "
                f"Nuki ID {self.nuki_id} volatized."
            )
            self._json = data[0]._json

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._json}>"
