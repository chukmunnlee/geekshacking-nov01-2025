# Updated on Fri Oct 31 07:10:44 PM +08 2025

import os, json

class TodoDB:
  def __init__(self, db_file = 'tasks.json'):
    self.db = {}
    self.db_file = db_file

    self.read_db()

  def add(self, filename: str, text: str, line_num: int) -> bool:

    if filename not in self.db:
      self.db[filename] = {}

    todos = self.db[filename]
    todos[f'_{line_num}'] = text

    self.write_db()

    return True

  def get(self, filename: str) -> dict:

    if filename not in self.db:
      return {}

    return self.db[filename]

  def delete_todos(self, filename: str):
    if filename not in self.db:
      return

    self.db.pop(filename)
    self.write_db()

  def get_by_id(self, filename: str, id: int) -> tuple| None:
    if (filename not in self.db) or (id >= len(self.db[filename])):
      return None
    return self.db[filename][f'_{id}']

  def count(self, filename: str) -> int:
    if filename not in self.db:
      return 0
    return len(self.db[filename])

  def get_filenames(self) -> list[str]:
    return [ filename for filename in self.db ]

  def read_db(self):
    if not os.path.isfile(self.db_file):
      self.db = {}
      return

    with open(self.db_file, 'r') as f:
      self.db = json.load(f)

  def write_db(self):
    with open(self.db_file, 'w') as f:
      json.dump(self.db, f, indent=2)

  def sample_data(self):
    filename = 'main.js'
    todos = [ 'abcd', 'efgh', 'ijkl' ]
    line_nums = [ 10, 20, 30 ]

    for i in range(len(todos)):
      self.add(filename, todos[i], line_nums[i])
