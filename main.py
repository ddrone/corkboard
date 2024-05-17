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

db_insert_script = """
  insert into ideas (idea, count) values (
    ?, 1
  );
"""

def create_idea(conn: sqlite3.Connection, idea: str):
  conn.execute(db_insert_script, [idea])

def db_exists():
  return os.path.exists(db_filename)

def idea_subcommand(args):
  if not db_exists():
    print('Database does not exist, create using \'init\' subcommand first!')
    return

  conn = sqlite3.connect(db_filename)
  create_idea(conn, args.idea)
  conn.commit()
  conn.close()

def serve(_args):
  if not db_exists():
    print('Database does not exist, create using \'init\' subcommand first!')
    return

  # TODO: check the existence of file db_filename
  print('serve: not implemented yet')

def init(_args):
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
  parser.set_defaults(subcommand = 'root')
  subparsers = parser.add_subparsers()
  handlers = {'root': serve}

  def add_subparser(name, handler):
    handlers[name] = handler
    subparser = subparsers.add_parser(name)
    subparser.set_defaults(subcommand = name)
    return subparser

  add_subparser('serve', serve)
  add_subparser('init', init)
  parser_idea = add_subparser('idea', idea_subcommand)
  parser_idea.add_argument('idea')

  return (parser, handlers)

def main():
  (parser, handlers) = setup_argparse()
  args = parser.parse_args()
  handlers[args.subcommand](args)

if __name__ == "__main__":
  main()
