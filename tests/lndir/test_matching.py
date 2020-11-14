import os

import pytest
from src.lndir.lndir import lndir

@pytest.fixture
def test_directory(tmpdir):
    tmpdir.mkdir('S01')
    for i in range(6):
        f = tmpdir / 'Episode.Title.S01.E0{}.mkv'.format(i)
        f.write('text')
    return tmpdir

def test_dry_run(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
          'to_dir': test_directory / 'output', 'to_structure': 'Episode.Title.S$1E$2.mkv',
           'dry': True})
    
def test_symlink(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
          'to_dir': test_directory / 'output', 'to_structure': 'Episode.Title.S$1E$2.mkv',
           'symlink':True})
    for f in os.listdir(test_directory / 'output'):
        if not os.path.islink(test_directory / 'output' / f):
            raise AssertionError('{} is not a symlink'.format(f))

def test_file(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
          'to_dir': test_directory / 'output', 'to_structure': 'Episode.Title.S$1E$2.mkv'})
    for f in os.listdir(test_directory / 'output'):
        if not os.path.isfile(test_directory / 'output' / f):
            raise AssertionError('{} is not a symlink'.format(f))

def test_amount(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
          'to_dir': test_directory / 'output', 'to_structure': 'Episode.Title.S$1E$2.mkv',
           'symlink': True})
    length = len(os.listdir(test_directory / 'output'))
    if length != 6:
        raise AssertionError('Incorrect amount of files, expected 6, {} created'.format(length))