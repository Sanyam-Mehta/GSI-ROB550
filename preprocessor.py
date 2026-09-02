import csv

'''
Look at "ROB550 W25 Intro Survey (Responses) - Sorted.csv" to see how to format the CSV. It must have some survey fields, along with calculated programming and mechanical aptitude columns.

The csv must also have a "Require Team Size 4" column. If a student is likely to drop, put a "1" in the row to signify they must be put in a team of size 4.
'''

def get_students_armlab(filename, section):
    assert section in ('AM', 'PM')
    
    section_findtext = 'Section 1' if section=='AM' else 'Section 2'
    
    with open(filename) as f:
        data = csv.DictReader(f)

        students = []

        for i, row in enumerate(data):
            if section_findtext in row['Section']:
                student = dict(
                    id=i,
                    email=row['Email Address'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    preferred_name=row['First Name'] if row['Preferred Name'] == 'Please use my first name (above)' else row['Preferred Name'],
                    programming=float(row['Programming Aptitude']),
                    mechanical=float(row['Mechanical Aptitude']),
                    degree=row['Degree'],
                    require_4=bool(row['Require Team Size 4']) and int(row['Require Team Size 4'])
                )
                students.append(student)

    return students


def get_students_botlab(intro_filename, peer_eval_filename, section):
    assert section in ('AM', 'PM')
    
    students_armlab = get_students_armlab(intro_filename, section)
    students_armlab_dict = {
        student['email']:student for student in students_armlab
    }
    
    # After getting the data from the intro survey, use the peer evaluation survey to overwrite some fields
    with open(peer_eval_filename) as f:
        data = csv.DictReader(f)

        students = []

        for i, row in enumerate(data):
            email = row['Email Address']
            if email in students_armlab_dict:
                student = students_armlab_dict[email]
                student['programming'] = float(row["Now that you've seen the intensity of the programming requirements for this course, how would you rate your coding abilities? This will NOT be used toward your grade at all, but is to help the instructors understand student progress through ROB550."])
                student['require_4'] = False
                student['prev_team'] = int(row['Your team number'].split()[-1])
                
                students.append(student)
                
        # add back any students who did not fill out the peer eval survey
        existing_emails = set([student['email'] for student in students])
        print(existing_emails)
        for student in students_armlab:
            if student['email'] not in existing_emails:
                students.append(student)
                student['prev_team'] = -1

    return students


if __name__ == '__main__':
    # For debug runs, you can change this field
    filename =  '/Users/sanyam/Projects/UMich/GSI-ROB550-Everything/GSI-ROB550/ROB550 F25 Intro Survey (Responses) - Sorted - dropping likelihood threshold 4.csv'
    students_am = get_students_armlab(filename, 'AM')
    students_pm = get_students_armlab(filename, 'PM')
    
    for student in students_am: print(student)
    print('\n' + '='*150 + '\n')
    for student in students_pm: print(student)