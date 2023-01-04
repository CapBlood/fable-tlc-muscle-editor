#!/usr/bin/env python

from PyInstaller.__main__ import run as pyinstall_run

pyinstall_run([
    'body_changer/ui/main_window.py',
    '--windowed',
    '--noconfirm',
    '--clean',
    '--add-data',
    'body_changer/muscle.lark:.',
    '-n',
    'Body Changer'
])
