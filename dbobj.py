#      -- Database Object Definitions --
# This python file defines certain statements
# that align with the database tables associ-
# -ated with this project. It basically makes
# the most easily templated SQL statements to
# manipulate these tables with relative ease.
# Certain other common statements can not be
# included as they require more complexity and
# therefore do not fit in with the templated
# format these classes take. These classes are
# primarily used in association with the met-
# -hods in the 'database.py' file of this
# project.


class servers:
  sql_create='''CREATE TABLE IF NOT EXISTS servers (
  id integer PRIMARY KEY,
  prefix text);'''
  sql_insert='''INSERT INTO servers(id,prefix)
  VALUES(%s,%s)'''
  sql_update='''UPDATE servers
  SET prefix = %s
  WHERE id = %s'''
  fields = ("id","prefix")
  table_name = "servers"

class accounts:
  sql_create='''CREATE TABLE IF NOT EXISTS accounts (
  id integer PRIMARY KEY,
  value integer);'''
  sql_insert='''INSERT INTO accounts(id,value)
  VALUES(%s,%s)'''
  sql_update='''UPDATE accounts
  SET value = %s
  WHERE id = %s'''
  fields = ("id","value")
  table_name = "accounts"

# Add your other things here with the same data structure to make them work with the built-in
# database system in util_classes.py
