from argparse import ArgumentParser
from ctypes import windll
from ykman.device import list_all_devices, scan_devices
from time import sleep

class YubikeyWindowsLock:
    _state = None
    _keys = []
    _serial = None
    _wait_time = 2

    def __init__(self, serial = None, wait_time = 2) -> None:
        _, self._state = scan_devices()
        self._keys = []
        self._set_serial(serial)
        self._set_wait_time(wait_time)

    def _serial_sanity_check(self, serial) -> None:
        if not serial:
            return
        if not str(serial).isdecimal():
            raise ValueError(f"serial number contains illegal character")
        if len(str(serial)) != 8:
            raise ValueError(f"serial number must consist of 8 digits")

    def _set_serial(self, serial) -> None:
        self._serial_sanity_check(serial)
        self._serial = serial

    def _set_wait_time(self, wait_time) -> None:
        if wait_time < 1:
            raise ValueError(f"Value {wait_time} not allowed for wait_time, needs to be at least 1")
        self._wait_time = wait_time

    def _state_changed(self) -> bool:
        _, new_state = scan_devices()
        if new_state != self._state:
            self._state = new_state
            return True
        return False

    def _update_list_of_yubikeys(self) -> None:
        self._keys = [info.serial for _, info in list_all_devices()]

    def _key_is_present(self) -> bool:
        if self._serial:
            return self._serial in self._keys
        return len(self._keys) > 0

    def _lock_screen(self) -> None:
        windll.user32.LockWorkStation()

    def _wait(self) -> None:
        sleep(self._wait_time)

    def monitor_system(self, wait_time=None, serial=None) -> None:
        if wait_time:
            self._set_wait_time(wait_time)
        if serial:
            self._set_serial(serial)
        while True:
            if self._state_changed():
                self._update_list_of_yubikeys()
                if not self._key_is_present():
                    self._lock_screen()
            self._wait()

if __name__ == '__main__':
    parser = ArgumentParser(description='Lock Windows when Yubikey is removed')
    parser.add_argument('-s', '--serial', type=int, default=None, help='Limit to yubikey with this serial number')
    parser.add_argument('-w', '--wait', type=float, default=5, help='The time (in s) between two checks (default: 5)')
    args = parser.parse_args()
    YubikeyWindowsLock().monitor_system(wait_time=args.wait, serial=args.serial)
