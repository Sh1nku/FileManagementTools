#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import re
import argparse
import pathlib
from shutil import copyfile

def dir_exists(dir):
    if not os.path.isdir(os.path.abspath(dir)):
        raise argparse.ArgumentTypeError("{} is an invalid directory".format(dir))
    return os.path.abspath(dir)

def create_file_path_from_args(string, args, relative_path):
    for index, value in enumerate(args):
        string = string.replace('{^'+str(index+1)+'}', value)
    if os.path.isabs(string):
        return string
    else:
        return str(relative_path / string)

def lndir(args):
    files = {}
    for f in os.listdir(args['from_dir']):
        file = re.search(args['from_structure'], f)
        if file:
            arguments = []
            for group in file.groups():
                arguments.append(group)
            files[file.string] = arguments
    if len(files.keys()) > 0:
        if args.get('dry'):
            for key, value in files.items():
                print('{} -> {}'.format(args['from_dir'] / key, create_file_path_from_args(args['to_structure'], value, args['from_dir'])))
        else:
            for key, value in files.items():
                output_file = create_file_path_from_args(args['to_structure'], value, args['from_dir'])
                pathlib.Path(os.path.split(output_file)[0]).mkdir(parents=True, exist_ok=True)
                if args.get('symlink'):
                    os.symlink(args['from_dir'] / key, output_file)
                elif args.get('copy'):
                    copyfile(args['from_dir'] / key, output_file)
                else:
                    os.link(args['from_dir'] / key, output_file)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch copy, hardlink or symlink files using regex')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--symlink', action='store_true', help='Create symlinks instead of hardlinks')
    group.add_argument('-c', '--copy', action='store_true', help='Copy files instead of symlink')
    group.add_argument('-d', '--dry', action='store_true', help='List the files that would be created')
    parser.add_argument('from_dir', help='The dir to copy from', type=dir_exists)
    parser.add_argument('from_structure', help='Regex expression describing the structure of the files')
    parser.add_argument('to_structure', help='Expression with {^N} describing the inputs')
    args = vars(parser.parse_args())
    args['from_dir'] = pathlib.Path(args['from_dir'])
    lndir(args)


