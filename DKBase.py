# DeeKie Base Manager (Data base manager)
# - Started 28 October 2023
# -------------------------------------------
import os

os.chdir('D:\\Desktop\\python_folder\\Year 13 - NEA stuff\\database_manager\\databases')


class DKBase:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_exists = True

        try:
            with open(self.file_name, 'r') as f:  # Checks if file already exists
                pass
        except FileNotFoundError:
            self.file_exists = False

    # ---------------------------------------------------- # USED WITHIN OTHER FUNCTIONS
    def find_index_positions(self, first_line):

        index_counter = -1
        character_count = 0
        positions = []  # Function to find the index positions of '|'

        for char in first_line:
            index_counter += 1
            if char == '|':
                character_count += 1
                positions.append(index_counter)

        return positions

    # ------------------------------------------------------- # USED WITHIN OTHER FUNCTIONS
    def get_field_lengths(self, index_positions_list):
        lengths_list = []
        index_counter = -1

        for num in index_positions_list:
            index_counter += 1

            if index_counter == 0:
                lengths_list.append(num)  # Gets first field length
            else:
                length = num - index_positions_list[index_counter - 1]  # Gets remaining field lengths
                lengths_list.append(length - 1)

        return lengths_list

    # --------------------------------------------------- # USE THIS FUNCTION ONLY TO READ AND GET DATA
    def open(self):
        if self.file_exists:
            pass
        else:
            error_message = "ERROR: file '{}' does not exist.".format(self.file_name)  # Error checking
            raise Exception(error_message)                                             # Checks if file even exists

    # ----------------------------------------------------
    def create(self, fields):  # fields MUST BE A DICTIONARY
        if self.file_exists:
            error_message = "ERROR: file '{}' already exists.".format(self.file_name)  # Error checking
            raise Exception(error_message)                                             # Checks if file already exists
        else:                                                                          # Prevents overwriting
            pass

        try:
            for i in fields.values():                                # Error checking
                int(i)                                               # Checks if value in dict is a string
        except ValueError:
            raise Exception("ERROR: invalid type for key values")

        headings_row = ""
        heading_string = ""

        for field_title in fields:  # Formatting field titles to be written onto txt files
            field_title_length = len(field_title)
            field_length = fields[field_title]

            if field_title_length >= field_length:
                heading_string = field_title + "|"

            elif field_title_length < field_length:
                string = field_title.center(field_length)  # Sets and formats field length to correct length.
                heading_string = string + "|"  # Puts field title in middle, between whitespace.

            headings_row = headings_row + heading_string

        print(headings_row)

        with open(self.file_name, 'w') as file:
            formatted_headings_row = headings_row + '\n'
            file.write(formatted_headings_row)
            print("File created successfully")

    # ------------------------------------------------------
    def add_records(self, *records):  # records MUST BE A TUPLE

        if not isinstance(records, tuple):  # Error checking
            raise Exception("ERROR: invalid records argument given. Must be a tuple.")  # Checks if records is a tuple.

        with open(self.file_name, 'r') as file:  # Gets headings row of DB for format checks e.g. fields given.
            lines = file.readlines()
            first_line = lines[0]

        number_of_fields = first_line.count('|')

        for record in records:  # Error checking
            if not isinstance(record, tuple):  # Checks if record is a tuple
                raise Exception("ERROR: invalid records argument given. Must be a tuple.")

        for record in records:  # Error checking
            if len(record) != number_of_fields:  # Checks if record has correct amount of fields.
                raise Exception("ERROR: one or more records have an invalid length.")

        index_positions_list = self.find_index_positions(first_line)
        field_lengths_list = self.get_field_lengths(index_positions_list)

        for record in records:
            index_counter = -1  # Error checking
            for data in record:  # Checks if each data given exceeds their respective field length.
                index_counter += 1
                if len(str(data)) > field_lengths_list[index_counter]:
                    raise Exception("ERROR: one or more given fields have exceeded the field length")

        for record in records:
            record_string = ""
            index_counter = -1  # Formatting the records to be written into the txt file.
            for data in record:
                index_counter += 1
                data_string = str(data).center(field_lengths_list[index_counter])
                data_string = data_string + '|'
                record_string += data_string

            print("Record string: ", record_string)

            with open(self.file_name, 'a') as file:
                formatted_record_string = record_string + "\n"
                file.write(formatted_record_string)

    def del_records(self, conditions):  # conditions MUST BE A DICTIONARY


        condition_fields = list(conditions)
        #print(condition_fields)

        if not isinstance(conditions, dict):                                                    # Error checking
            raise Exception("ERROR: invalid conditions argument given. Must be a dictionary.")  # Checks if its a dict

        with open(self.file_name, 'r') as file:  # Gets headings row of DB for format checks e.g. fields given.
            file_lines = file.readlines()
            headings_row = file_lines[0]

        for field in condition_fields:
            if field not in headings_row:                                                # Error checking
                raise Exception("ERROR: Fields given do not exist in the database.")     # Checks if fields exist in DB

        index_positions = [0]
        for pos in self.find_index_positions(headings_row):    # Gets list of index positions of '|', inserting 0 at the start.
            index_positions.append(pos)

        field_counter = -1
        lines_to_be_removed = []
        for field in condition_fields:
            field_counter += 1
            field_index_pos = headings_row.index(field)

            if field_index_pos == 0:
                column_start_pos = 0                   # Gets index positions of '|' for the first column/field
                column_end_pos = index_positions[1]
            else:                                       # VVV   SEE NOTES FOR VISUAL AND BETTER EXPLANATION   VVV
                index_positions_for_search = []
                for i in index_positions:               # Makes temporary list of index positions to insert the index
                    index_positions_for_search.append(i)  # pos of the field.

                index_positions_for_search.append(field_index_pos)  # Sorts it, putting field pos between the index
                index_positions_for_search.sort()  # positions of the starting '|' and the ending '|'.

                field_index_pos_for_search = index_positions_for_search.index(field_index_pos)

                column_start_pos = index_positions[field_index_pos_for_search-1]  # Gives us index positions of '|'
                column_end_pos = index_positions[field_index_pos_for_search]  # for the field/column

            #print("Start pos:", column_start_pos)
            #print("End pos:", column_end_pos)
            #print(" ")

            line_index_counter = -1
            for line in file_lines:
                line_index_counter += 1
                data = line[column_start_pos:column_end_pos]
                current_field = condition_fields[field_counter]
                condition = str(conditions[current_field])
                #print("Condition:", condition)

                if column_start_pos == 0:
                    stripped_data = data.strip()
                else:                                         # Gets data from text file, removes whitespace.
                    data = data[1:]                           # Just gets the data
                    stripped_data = data.strip()

                #print("Stripped data:", stripped_data)

                if condition == stripped_data:
                    lines_to_be_removed.append(line_index_counter)
                    #print(line)

        #print("Lines to be removed:", lines_to_be_removed)
        lines_to_be_removed = list(set(lines_to_be_removed))  # Removes any duplicates from list
        #print("Lines to be removed:", lines_to_be_removed)

        shift_counter = -1
        for num in lines_to_be_removed:
            shift_counter += 1                                # Removes line from list of file lines.
            removed_line = num - shift_counter                # Shift counter used as index positions change when a line
            file_lines.pop(removed_line)                      # is removed. Shift counter remembers what line to remove.

        with open(self.file_name, 'w') as file:
            for line in file_lines:                           # Overwrites file with the changes made.
                file.write(line)







    # ------------------------------------------------------------------------
    def get(self, fields, conditions=None):
        headings_row = ""
        select_all = False

        with open(self.file_name, 'r') as file:  # Gets headings row of DB for format checks e.g. fields given.
            file_lines = file.readlines()
            headings_row = file_lines[0]


        # ERROR CHECKING - fields - MUST BE A TUPLE, EVEN A SINGLE ITEM TUPLE
        if not isinstance(fields, tuple):
            raise Exception("ERROR: Given fields must be a tuple")  # Checks if fields is the correct data type

        if len(fields) == 1 and fields[0] == '*':         # '*' Selects the whole record, just like SQL
            select_all = True
            pass

        else:
            for field in fields:                          # Checks if a given field exists in the database
                if field not in headings_row:
                    raise Exception("ERROR: fields parameter - Given field does not exist in database")


        # ERROR CHECKING - conditions
        condition_fields = []
        if conditions != None:                  # Checks if user has given conditions
            condition_fields = list(conditions)

            if not isinstance(conditions, dict):                                                    # Error checking
                raise Exception("ERROR: invalid conditions parameter given. Must be a dictionary.")  # Checks if its a dict

            for field in condition_fields:
                if field not in headings_row:                             # Error checking   # Checks if fields exist in DB
                    raise Exception("ERROR: conditions parameter - Fields given do not exist in the database.")






        # ---STARTING SEARCH FOR TARGET RECORDS
        index_positions = [0]
        for pos in self.find_index_positions(
                headings_row):  # Gets list of index positions of '|', inserting 0 at the start.
            index_positions.append(pos)

        field_counter = -1
        lines_to_be_read = []

        for field in condition_fields:
            field_counter += 1
            field_index_pos = headings_row.index(field)

            if field_index_pos == 0:
                column_start_pos = 0  # Gets index positions of '|' for the first column/field
                column_end_pos = index_positions[1]
            else:  # VVV   SEE NOTES FOR VISUAL AND BETTER EXPLANATION   VVV
                index_positions_for_search = []
                for i in index_positions:  # Makes temporary list of index positions to insert the index
                    index_positions_for_search.append(i)  # pos of the field.

                index_positions_for_search.append(field_index_pos)  # Sorts it, putting field pos between the index
                index_positions_for_search.sort()  # positions of the starting '|' and the ending '|'.

                field_index_pos_for_search = index_positions_for_search.index(field_index_pos)

                column_start_pos = index_positions[field_index_pos_for_search - 1]  # Gives us index positions of '|'
                column_end_pos = index_positions[field_index_pos_for_search]  # for the field/column

            # print("Start pos:", column_start_pos)
            # print("End pos:", column_end_pos)
            # print(" ")

            line_index_counter = -1
            for line in file_lines:
                line_index_counter += 1
                data = line[column_start_pos:column_end_pos]
                current_field = condition_fields[field_counter]
                condition = str(conditions[current_field])
                # print("Condition:", condition)

                if column_start_pos == 0:
                    stripped_data = data.strip()
                else:  # Gets data from text file, removes whitespace.
                    data = data[1:]  # Just gets the data
                    stripped_data = data.strip()

                # print("Stripped data:", stripped_data)

                if condition == stripped_data:
                    lines_to_be_read.append(line_index_counter)
                    # print(line)

        lines_to_be_read = list(set(lines_to_be_read))  # Removes any duplicates from list
        #print("target record indexes:", lines_to_be_read)

        target_records = []                       # List containing the whole target records, not the index

        if conditions == None:  # Includes all records if user has not given any conditions
            target_records = file_lines[1:]
        else:
            for line_index in lines_to_be_read:
                target_records.append(file_lines[line_index])
                #print(file_lines[line_index])



        no_of_records = len(target_records)
        records_table = []                        # Creates a table. Each row is a record that meets the condition.

        for i in range(0, no_of_records):         # Each row will contain the target data that the user wanted.
            records_table.append([])











        # --- GETTING INDIVIDUAL DATA
        field_counter = -1

        if select_all:                         # If user wanted the whole record/ all data

            headings_list = []
            count = -1
                                                         #THIS PART ONLY GETS THE FIELD TITLES
            for pos in index_positions:                  #CAN BE MADE INTO A FUNCTION?
                if pos != index_positions[len(index_positions)-1]:
                    count += 1
                    forward_count = count + 1

                    start_pos = index_positions[count]
                    end_pos = index_positions[forward_count]

                    heading = headings_row[start_pos:end_pos]

                    if start_pos == 0:
                        stripped_heading = heading.strip()
                    else:  # Gets heading from text file, removes whitespace.
                        heading = heading[1:]  # Just gets the heading
                        stripped_heading = heading.strip()

                    #print(stripped_heading)
                    headings_list.append(stripped_heading)

            #print(headings_list)




            for field in headings_list: #HEADINGS ROW IS THE WHOLE RECORD, NOT A LIST OF HEADING TITLES
                field_counter += 1
                field_index_pos = headings_row.index(field)

                if field_index_pos == 0:
                    column_start_pos = 0  # Gets index positions of '|' for the first column/field
                    column_end_pos = index_positions[1]
                else:  # VVV   SEE NOTES FOR VISUAL AND BETTER EXPLANATION   VVV
                    index_positions_for_search = []
                    for i in index_positions:  # Makes temporary list of index positions to insert the index
                        index_positions_for_search.append(i)  # pos of the field.

                    index_positions_for_search.append(field_index_pos)  # Sorts it, putting field pos between the index
                    index_positions_for_search.sort()  # positions of the starting '|' and the ending '|'.

                    field_index_pos_for_search = index_positions_for_search.index(field_index_pos)

                    column_start_pos = index_positions[field_index_pos_for_search - 1]  # Gives us index positions of '|'
                    column_end_pos = index_positions[field_index_pos_for_search]  # for the field/column

                #print("Start pos:", column_start_pos)
                #print("End pos:", column_end_pos)
                #print("---------------- ")

                record_index_count = -1  # Tracks index of what record data should be added to.
                for line in target_records:
                    record_index_count += 1
                    data = line[column_start_pos:column_end_pos]
                    #print("data: ", data)

                    if column_start_pos == 0:
                        stripped_data = data.strip()
                    else:  # Gets data from text file, removes whitespace.
                        data = data[1:]  # Just gets the data
                        stripped_data = data.strip()

                    # print(stripped_data)
                    records_table[record_index_count].append(stripped_data)

                    if record_index_count == no_of_records - 1:
                        record_index_count = -1

                # print("---------------- ")



        else:                                   # Doesnt get whole record. Only gets what user asks for
            for field in fields:
                field_counter += 1
                field_index_pos = headings_row.index(field)

                if field_index_pos == 0:
                    column_start_pos = 0  # Gets index positions of '|' for the first column/field
                    column_end_pos = index_positions[1]
                else:  # VVV   SEE NOTES FOR VISUAL AND BETTER EXPLANATION   VVV
                    index_positions_for_search = []
                    for i in index_positions:  # Makes temporary list of index positions to insert the index
                        index_positions_for_search.append(i)  # pos of the field.

                    index_positions_for_search.append(field_index_pos)  # Sorts it, putting field pos between the index
                    index_positions_for_search.sort()  # positions of the starting '|' and the ending '|'.

                    field_index_pos_for_search = index_positions_for_search.index(field_index_pos)

                    column_start_pos = index_positions[field_index_pos_for_search - 1]  # Gives us index positions of '|'
                    column_end_pos = index_positions[field_index_pos_for_search]  # for the field/column


                #print("Start pos:", column_start_pos)
                #print("End pos:", column_end_pos)
                #print("---------------- ")



                record_index_count = -1                  # Tracks index of what record data should be added to.
                for line in target_records:
                    record_index_count += 1
                    data = line[column_start_pos:column_end_pos]
                    #print("data: ", data)

                    if column_start_pos == 0:
                        stripped_data = data.strip()
                    else:                                         # Gets data from text file, removes whitespace.
                        data = data[1:]                           # Just gets the data
                        stripped_data = data.strip()

                    #print(stripped_data)
                    records_table[record_index_count].append(stripped_data)

                    if record_index_count == no_of_records - 1:
                        record_index_count = -1

                #print("---------------- ")


        for record in records_table:
            print(record)











    # ------------------------------------------------------------------------
    def update(self, fields, conditions):
        headings_row = ""

        with open(self.file_name, 'r') as file:  # Gets headings row of DB for format checks e.g. fields given.
            file_lines = file.readlines()
            headings_row = file_lines[0]


        # ERROR CHECKING - fields - MUST BE A DICTIONARY
        if not isinstance(fields, dict):
            raise Exception("ERROR: fields parameter must be a dictionary")  # Checks if fields is the correct data type

        else:
            for field in fields:                          # Checks if a given field exists in the database
                if field not in headings_row:
                    raise Exception("ERROR: fields parameter - Given field does not exist in database")


        # ERROR CHECKING - conditions
        condition_fields = []
        condition_fields = list(conditions)
        if not isinstance(conditions, dict):
            raise Exception("ERROR: invalid conditions parameter given. Must be a dictionary.")  # Checks if its a dict

        if len(conditions) < 1:    # Checks only one condition given
            raise Exception("ERROR: conditions parameter - No condition given. Function requires one condition.")
        elif len(conditions) > 1:
            raise Exception("ERROR: conditions parameter - More than one condition given. Function requires one condition.")

        for field in condition_fields:
            if field not in headings_row:
                raise Exception("ERROR: conditions parameter - Fields given do not exist in the database.")



        # ---STARTING SEARCH FOR TARGET RECORDS
        index_positions = [0]
        for pos in self.find_index_positions(
                headings_row):  # Gets list of index positions of '|', inserting 0 at the start.
            index_positions.append(pos)

        field_counter = -1
        lines_to_be_read = []
        
        for field in condition_fields:
            field_counter += 1
            field_index_pos = headings_row.index(field)

            if field_index_pos == 0:
                column_start_pos = 0  # Gets index positions of '|' for the first column/field
                column_end_pos = index_positions[1]
            else:  # VVV   SEE NOTES FOR VISUAL AND BETTER EXPLANATION   VVV
                index_positions_for_search = []
                for i in index_positions:  # Makes temporary list of index positions to insert the index
                    index_positions_for_search.append(i)  # pos of the field.

                index_positions_for_search.append(field_index_pos)  # Sorts it, putting field pos between the index
                index_positions_for_search.sort()  # positions of the starting '|' and the ending '|'.

                field_index_pos_for_search = index_positions_for_search.index(field_index_pos)

                column_start_pos = index_positions[field_index_pos_for_search - 1]  # Gives us index positions of '|'
                column_end_pos = index_positions[field_index_pos_for_search]  # for the field/column

            # print("Start pos:", column_start_pos)
            # print("End pos:", column_end_pos)
            # print(" ")

            line_index_counter = -1
            for line in file_lines:
                line_index_counter += 1
                data = line[column_start_pos:column_end_pos]
                current_field = condition_fields[field_counter]
                condition = str(conditions[current_field])
                #print("Condition:", condition)

                if column_start_pos == 0:
                    stripped_data = data.strip()
                else:  # Gets data from text file, removes whitespace.
                    data = data[1:]  # Just gets the data
                    stripped_data = data.strip()

                #print("Stripped data:", stripped_data)

                if condition == stripped_data:
                    lines_to_be_read.append(line_index_counter)
                    # print(line)

        lines_to_be_read = list(set(lines_to_be_read))  # Removes any duplicates from list
        target_record_indexes = lines_to_be_read        
        #print("target record indexes:", lines_to_be_read)

        target_records = []  # List containing the whole target records, not the index

        for line_index in lines_to_be_read:
            target_records.append(file_lines[line_index])
            #print(file_lines[line_index])





        # ---UPDATING DATABASE
        fields_list = list(fields)

        #print(fields_list)
        #print(index_positions)
        #print("-------------------")

        field_counter = -1
        index_change_counter = -1

        for record in target_records:  # Iterates through records that need updating
            #print("OLD record:", record)
            new_record = record
            index_change_counter += 1

            for field in fields_list:
                new_data = fields[field]
                #print("new_data:", new_data)

                field_counter += 1
                field_index_pos = headings_row.index(field)

                if field_index_pos == 0:
                    column_start_pos = 0  # Gets index positions of '|' for the first column/field
                    column_end_pos = index_positions[1]
                else:  # VVV   SEE NOTES FOR VISUAL AND BETTER EXPLANATION   VVV
                    index_positions_for_search = []
                    for i in index_positions:  # Makes temporary list of index positions to insert the index
                        index_positions_for_search.append(i)  # pos of the field.

                    index_positions_for_search.append(field_index_pos)  # Sorts it, putting field pos between the index
                    index_positions_for_search.sort()  # positions of the starting '|' and the ending '|'.

                    field_index_pos_for_search = index_positions_for_search.index(field_index_pos)

                    column_start_pos = index_positions[field_index_pos_for_search - 1]  # Gives us index positions of '|'
                    column_end_pos = index_positions[field_index_pos_for_search]  # for the field/column

                #print("Start pos:", column_start_pos)
                #print("End pos:", column_end_pos)
                #print(" ")




                # UPDATED DATA ERROR CHECKING - CHECK IF IT EXCEEDS LENGTH
                field_length = column_end_pos - column_start_pos - 1   # -1 needs testing. test max of field length?
                #print("Field length:", field_length)

                if len(new_data) > field_length:
                    raise Exception("ERROR: fields parameter - One or more New values exceeds field length")

                # +1 doesnt include/replace line separator
                formatted_new_data = new_data.center(field_length)
                #print("formatted new data:", formatted_new_data)
                #print("replacing >>:", new_record[column_start_pos+1:column_end_pos])
                new_record = new_record.replace(record[column_start_pos+1:column_end_pos], formatted_new_data, 1) # Replaces only first occurence.
                #print(new_record)                                                                         # useful when there is duplicates in multiple fields e.g  x |     x  |x|x|       x        |

            #print("NEW record:", new_record)
            #print("-------------------")

            #print("target_record_indexes: ", target_record_indexes)
            #print("index change counter:", index_change_counter)
            current_index_to_change = target_record_indexes[index_change_counter]
            file_lines[current_index_to_change] = new_record
            # Gets file_lines list, replaces old records with new records.

        #for line in file_lines:
            #print(line)

        with open(self.file_name, 'w') as file:
            for line in file_lines:                           # Overwrites file with the changes made.
                file.write(line)






# TESTS --------------------------------

database = DKBase('bookings - Copy (4).txt')
database.open()

database.update(
    {'Occasion': 'Celebration'},
    {'Name': 'Philip'}
)


# Requirements/Limitations: fields and conditions dictionary is mandatory. Conditions dictionary MUST only have one
#                           key/value pair.

# TESTS --------------------------------
