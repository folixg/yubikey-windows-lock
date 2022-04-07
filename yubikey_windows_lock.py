""" Yubikey Windows Lock
Script to automatically lock your windows machine when yubikey gets removed

usage: yubikey_windows_lock.py [-h] [-s SERIAL] [-w WAIT]

options:
  -h, --help            show this help message and exit
  -s SERIAL, --serial SERIAL
                        Limit to yubikey with this serial number
  -w WAIT, --wait WAIT  The time (in s) between two checks (default: 2)


If imported this file will prvovide the class YubikeyWindowsLock.
"""
from argparse import ArgumentParser
from ctypes import windll
from time import sleep
from ykman.device import list_all_devices, scan_devices


class YubikeyWindowsLock:
    """
    Class that bundles everything needed to monitor connection of yubikey(s)

    Methods:
    --------
    monitor_system(self, wait_time=None, serial=None)
        Monitor the system in an endless loop and lock the screen if
        Yubikey is removed
    """

    _state = None
    _keys = []

    def __init__(self) -> None:
        _, self._state = scan_devices()
        self._keys = []

    def _serial_sanity_check(self, serial: int) -> None:
        if not serial:
            return
        if not str(serial).isdecimal():
            raise ValueError("serial number contains illegal character")
        if len(str(serial)) != 8:
            raise ValueError("serial number must consist of 8 digits")

    def _state_changed(self) -> bool:
        _, new_state = scan_devices()
        if new_state != self._state:
            self._state = new_state
            return True
        return False

    def _update_list_of_yubikeys(self) -> None:
        self._keys = [info.serial for _, info in list_all_devices()]

    def _key_is_present(self, serial: int) -> bool:
        if serial:
            self._serial_sanity_check(serial)
            return serial in self._keys
        return len(self._keys) > 0

    def monitor_system(self, wait_time: float = 2, serial: int = None) -> None:
        """
        Monitor the system in an endless loop and lock the screen if
        Yubikey is removed

        Parameters
        ----------
        wait_time : float, optional
            Time (in s) between two checks for status change (default: 2)
        serial : int, optional
            Only monitor the Yubikey matching this serial number (default:
            don't limit to specific key)
        """
        while True:
            if self._state_changed():
                self._update_list_of_yubikeys()
                if not self._key_is_present(serial):
                    windll.user32.LockWorkStation()
            sleep(wait_time)


if __name__ == "__main__":
    parser = ArgumentParser(description="Lock Windows when Yubikey is removed")
    parser.add_argument(
        "-s",
        "--serial",
        type=int,
        default=None,
        help="Limit to yubikey with this serial number",
    )
    parser.add_argument(
        "-w",
        "--wait",
        type=float,
        default=2,
        help="The time (in s) between two checks (default: 2)",
    )
    args = parser.parse_args()
    YubikeyWindowsLock().monitor_system(wait_time=args.wait, serial=args.serial)
