#!/usr/bin/env python3

import argparse
import os
import sqlite3

db_filename = 'ideas.db'

db_init_script = """
  create table ideas(
    id integer primary key autoincrement,
    idea text,
    count integer
  );
"""

def db_exists():
  return os.path.exists(db_filename)

def serve():
  if not db_exists():
    print('Database does not exist, create using \'init\' subcommand first!')
    return

  # TODO: check the existence of file db_filename
  print('serve: not implemented yet')

def init():
  if db_exists():
    print('Database exists already!')
    return

  try:
    conn = sqlite3.connect(db_filename)
    conn.execute(db_init_script)
    conn.close()
  except Exception as e:
    print('Error while creating a database, removing the intermediate result')
    os.remove(db_filename)
    raise e

def setup_argparse():
  parser = argparse.ArgumentParser(
    prog='corkboard',
    description='A scratchpad for project ideas')
  parser.set_defaults(func=serve)

  subparsers = parser.add_subparsers()
  parser_serve = subparsers.add_parser('serve')
  parser_serve.set_defaults(func=serve)

  parser_create = subparsers.add_parser('init')
  parser_create.set_defaults(func=init)

  return parser

def main():
  parser = setup_argparse()
  parser.parse_args().func()

if __name__ == "__main__":
  main()
