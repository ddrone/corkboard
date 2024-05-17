#!/usr/bin/env python3

import subprocess
import sys

def changed_files():
  result = subprocess.run('git diff --cached --name-only'.split(), capture_output=True)
  return result.stdout.decode().splitlines()

threshold = 100

def main():
  offenders = []
  for name in changed_files():
    with open(name) as f:
      if f.read().count('\n') > threshold:
        offenders.append(name)

  if len(offenders) > 0:
    print('Found long files:\n')
    for name in offenders:
      print(f'\t{name}')
    sys.exit(1)

if __name__ == "__main__":
  main()
