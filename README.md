# DKBase - txt file database manager README <<
### Last updated: 09/02/2024

## OVERVIEW 
DKBase is a database manager revolving around text files.
It can be used to handle multiple databases and is designed 
to be used in python programs.

## CURRENT FEATURES:

-Create a new database
-Add records
-Delete a record

## Setting up
Before making any changes to a database, you must correctly setup a database.
When setting up a database you can either setup to create a new database or
setup to view or edit a database.

## Creating a new database
db_variable = DKBase('file_name.txt')

db_variable.create(
	fields={'IDfield': IDlength, 'field1': length2, ...}
	)


Create a variable to refer to a database (db_variable).
Use .create() function to setup the fields and field lengths of the database.
.create() only accepts'fields' as an argument.
'fields' must be a dictionary.
Within the dictionary, the key is the name of the field while the value is 
its field length. 
field length must be an integer.


## Opening an existing database
db_variable = DKBase('file_name.txt')

db_variable.open()



Before making changes to a database e.g. inserting/deleting a record, you must use the .open() function.
