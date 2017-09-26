#!/usr/bin/env python
# derivered from unihandecode setup.py

import os
from setuptools import setup
from distutils.command.build import build

import pykakasi.genkanwadict as genkanwadict


README = open('README.rst').read()


def gen_dict(src_f, pkl_f):
    kanwa = genkanwadict.mkkanwa()
    src = os.path.join('pykakasi', 'data', src_f)
    dst = os.path.join('pykakasi', pkl_f)
    try:
        os.unlink(dst)
    except:
        pass
    kanwa.mkdict(src, dst)


def gen_kanwa(src, dst):
    try:
        os.unlink(dst+'.db')
    except:
        pass
    kanwa = genkanwadict.mkkanwa()
    kanwa.run(src, dst)


def _pre_build():
    DICTS = [
        ('itaijidict.utf8', 'itaijidict2.pickle'),
        ('hepburndict.utf8', 'hepburndict2.pickle'),
        ('kunreidict.utf8', 'kunreidict2.pickle'),
        ('passportdict.utf8', 'passportdict2.pickle'),
        ('hepburnhira.utf8', 'hepburnhira2.pickle'),
        ('kunreihira.utf8', 'kunreihira2.pickle'),
        ('passporthira.utf8', 'passporthira2.pickle')
    ]
    for (s, p) in DICTS:
        gen_dict(s, p)

    # build kakasi dict
    src = os.path.join('pykakasi', 'data', 'kakasidict.utf8')
    dst = os.path.join('pykakasi', 'kanwadict2.db')
    gen_kanwa(src, dst)


class my_build(build):
    def run(self):
        self.execute(_pre_build, (), msg="Running pre build task")
        build.run(self)


tests_require = ['nose', 'coverage', 'mock']
setup(name='pykakasi',
      version='0.24',
      description='Python implementation of kakasi - kana kanji simple inversion library',  # NOQA
      url='http://github.com/miurahr/pykakasi',
      license='GPLv3',
      long_description=README,
      author='Hioshi Miura',
      author_email='miurahr@linux.com',
      packages=['pykakasi',
                'pykakasi.genkanwadict'],
      provides=['pykakasi'],
      scripts=["kakasi"],
      include_package_data=True,
      package_data={
        'pykakasi': ['*.pickle', 'kanwadict2.*']},
      test_suite='nose.collector',
      tests_require=tests_require,
      cmdclass={'build': my_build},
      zip_safe=False,
)
