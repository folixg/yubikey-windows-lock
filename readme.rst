####################
Yubikey Windows Lock
####################

A script to lock your Windows machine once a formerly connected Yubikey
is removed.

Requirements
============
Needs a Python installation and yubikey-manager which can be installed with

.. code-block:: shell

    pip install --user yubikey-manager

Usage
=====

Command Line Options
--------------------

.. code-block::

    usage: yubikey-windows-lock.py [-h] [-w WAIT] [serial]

    Lock Windows when Yubikey is removed

    positional arguments:
    serial                Limit to yubikey with this serial number

    options:
    -h, --help            show this help message and exit
    -w WAIT, --wait WAIT  The time (in s) between two checks (default: 5)

Start at Windows login
----------------------
An easy way to automatically launch the script on Windows login is to use Windows Task Scheduler.
Create a basic task that is executed on logon and as action starts a program.
In the ``Program/Script`` field provide the path to ``pythonw.exe`` of your Python installation.
Typically that is

.. code-block::

    C:\Users\<your_username>\AppData\Local\Programs\Python\<your_python_version>\pythonw.exe

In the ``Add arguments`` field you provide the path to ``yubikey-windows-lock.py`` and optionally the
arguments you want to provide to the script.
So it should look something like

.. code-block::

    C:\Users\<your_username>\<path_to_this_repo>\yubikey-windows-lock.py -w 3 12345678