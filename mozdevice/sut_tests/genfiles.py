# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from random import randint
from zipfile import ZipFile
import os
import shutil


def gen_binary_file(path, size):
    with open(path, 'wb') as f:
        for i in xrange(size):
            byte = '%c' % randint(0, 255)
            f.write(byte)


def gen_zip(path, files, stripped_prefix=''):
    with ZipFile(path, 'w') as z:
        for f in files:
            new_name = f.replace(stripped_prefix, '')
            z.write(f, new_name)


def mkdir(path, *args):
    try:
        os.mkdir(path, *args)
    except OSError:
        pass


def gen_folder_structure():
    root = 'test-files/'
    prefix = root + 'push2/'
    mkdir(prefix)

    gen_binary_file(prefix + 'file4.bin', 59036)
    mkdir(prefix + 'sub1')
    shutil.copyfile(root + 'mytext.txt', prefix + 'sub1/file1.txt')
    mkdir(prefix + 'sub1/sub1.1')
    shutil.copyfile(root + 'mytext.txt', prefix + 'sub1/sub1.1/file2.txt')
    mkdir(prefix + 'sub2')
    shutil.copyfile(root + 'mytext.txt', prefix + 'sub2/file3.txt')


def gen_test_files():
    gen_folder_structure()
    flist = [
                'test-files/push2',
                'test-files/push2/file4.bin',
                'test-files/push2/sub1',
                'test-files/push2/sub1/file1.txt',
                'test-files/push2/sub1/sub1.1',
                'test-files/push2/sub1/sub1.1/file2.txt',
                'test-files/push2/sub2',
                'test-files/push2/sub2/file3.txt'
            ]
    gen_zip('test-files/mybinary.zip', flist, stripped_prefix='test-files/')
    gen_zip('test-files/mytext.zip', ['test-files/mytext.txt'])


def clean_test_files():
    dirs = ['test-files/push1', 'test-files/push2']
    for d in dirs:
        try:
            shutil.rmtree(d)
        except OSError:
            pass

    files = ['test-files/mybinary.zip', 'test-files/mytext.zip']
    for f in files:
        try:
            os.remove(f)
        except OSError:
            pass


if __name__ == '__main__':
    gen_test_files()
