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
          'to_structure': str(test_directory / 'output' / 'Episode.Title.S{^1}E{^2}.mkv'),
           'dry': True})
    
def test_symlink(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
          'to_structure': str(test_directory / 'output' / 'Episode.Title.S{^1}E{^2}.mkv'),
           'symlink': True})
    for f in os.listdir(test_directory / 'output'):
        if not os.path.islink(test_directory / 'output' / f):
            raise AssertionError('{} is not a symlink'.format(f))

def test_hardlink(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
           'to_structure': str(test_directory / 'output' / 'Episode.Title.S{^1}E{^2}.mkv'),
           'hardlink': True})
    for f in os.listdir(test_directory / 'output'):
        if not os.stat(test_directory / 'output' / f).st_nlink > 1:
            raise AssertionError('{} is not a hardlink'.format(f))

def test_file(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
           'to_structure': str(test_directory / 'output' / 'Episode.Title.S{^1}E{^2}.mkv')})
    for f in os.listdir(test_directory / 'output'):
        if not os.path.isfile(test_directory / 'output' / f):
            raise AssertionError('{} is not a symlink'.format(f))

def test_amount(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
           'to_structure': str(test_directory / 'output' / 'Episode.Title.S{^1}E{^2}.mkv'),
           'symlink': True})
    length = len(os.listdir(test_directory / 'output'))
    if length != 6:
        raise AssertionError('Incorrect amount of files, expected 6, {} created'.format(length))

def test_directory_create(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
           'to_structure': str(test_directory / 'output' / 'S{^1}/Episode.Title.S{^1}E{^2}.mkv'),
           'symlink': True})
    length = len(os.listdir(test_directory / 'output/S01'))
    if length != 6:
        raise AssertionError('Did not copy files correctly to {}'.format(test_directory / 'output/S01'))

def test_file_from_directory(test_directory):
    pass

def test_relative_path(test_directory):
    lndir({'from_dir': test_directory, 'from_structure': 'Episode.Title.S(\\d+).E(\\d+)(.*)',
           'to_structure': str('output/S{^1}/Episode.Title.S{^1}E{^2}.mkv')})
    for f in os.listdir(test_directory / 'output' / 'S01'):
        if not os.path.isfile(test_directory / 'output' / 'S01' / f):
            raise AssertionError('{} is not a file'.format(f))