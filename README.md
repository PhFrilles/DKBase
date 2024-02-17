# DKBase - txt file database manager README <<
### Last updated: 17/02/2024

## OVERVIEW 
DKBase is a database manager revolving around text files.
It can be used to handle multiple databases and is designed 
to be used in python programs.

## CURRENT FEATURES:

Create a new database, Add records, Delete records, Selecting data

## SETTING UP
Before making any changes to a database, you must correctly setup a database.
When setting up a database you can either setup to create a new database or
setup to view or edit a database.

## CREATING A NEW DATABASE
>db_variable = DKBase('file_name.txt')
>
>db_variable.create(
	fields={'IDfield': IDlength, 'field1': length2, ...}
	)


_Create a variable to refer to a database (db_variable).
Use .create() function to setup the fields and field lengths of the database.
.create() only accepts'fields' as an argument.
'fields' must be a dictionary.
Within the dictionary, the key is the name of the field while the value is 
its field length. 
field length must be an integer._


## OPENING AN EXISTING DATABASE
>db_variable = DKBase('file_name.txt')
>
>db_variable.open()


_Before making changes to a database e.g. inserting/deleting a record, you must use the .open() function._

## ADDING RECORDS
>db_variable.add_records(
>	(ID, field1, field2, ...),
>	(ID, field1, field2, ...)
>		)

_add_records() will take a single record or a list of records containing information about a specifc entry.
Records must be a tuple.
A record must have the same amount of fields the database has.
For each record, fields must be entered with the correct datatype.
Fields must be entered in the same order as how the database has ordered fields._

## DELETING RECORDS
>db_variable.del_records(
>	{field: data},
>	{field: data}
>		)

_del_records() will take a single dictionary only.
The dictionary will take a fieldname and then an item of data.
There can be many key/value pairs (or conditions) to check for.
The function will search through the field column and compare with the given data.
it will then delete the record if the data matches._

## SELECTING DATA
>db_variable.get(
>	(fields,),
>	{field: data, ...}
>		)

_.get() takes two parameters: fields and condition.
fields must be a tuple. It takes the field names that the user wants. Fields must exist in database.
fields can also take '*' as a single item tuple. Like SQL, this will select all fields.
Within condition dictionary, field is the field that the user wants to compare against.
Data is an item of data that will be compared to all items within the given field.
condition dictionary is optional and not needed.
Only use condition dictionary if looking for a record with specific data_

## UPDATING DATA
>db_variable.update(
>	{field: data, ...},
>	{field: condition}
>		)

_.update() function takes two parameters: 'Fields' and 'Condition'.
'Fields' must be a dictionary. It contains the field that the user would like to change - the key - and the new data that replaces it - the value.
given fields must exist in the database. 'Fields' can contain multiple key/value pairs.
'Condition' must be a dictionary. It contains the field that the user wants to compare against - the key - and the condition/data that will be compared to all items within the given field - the value.
'Condition' can only have one condition or key/value pair.
LIMITATIONS: Field headings of the database can be changed. This is a vulnerability that can be exploited to prevent a database from being used._
