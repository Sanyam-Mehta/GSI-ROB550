import random
import math
import csv
from collections import defaultdict
import itertools
from preprocessor import get_students_armlab, get_students_botlab
from tabulate import tabulate

# ===== MODIFY THIS SECTION =====

# Whether to generate Armlab teams or Botlab teams
project_type = 'Botlab' # Must be 'Armlab' or 'Botlab', capitalized

# Whether to generate teams for the AM or PM section
section = 'PM'

# Configure botlab-specific settings
# use_mech = project_type == 'Armlab'
use_mech = project_type == 'Botlab'

# The filenames to get the data from
intro_filename = '/Users/sanyam/Projects/UMich/GSI-ROB550-Everything/GSI-ROB550/ROB550 W26 Intro Survey (Responses) - Dropping Likelihood 3.csv'
peer_eval_filename = '/Users/sanyam/Projects/UMich/GSI-ROB550-Everything/GSI-ROB550/ROB550 - Armlab Peer Evaluation (W26) (Responses) - Form Responses.csv' #'./ROB550 W25 - Armlab Peer Evaluation (Responses) - Sorted.csv' # This can be blank for armlab teams


# The team sizes to use for both AM and PM
team_sizes_am = [3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4] # am group has 29 responses; groups of 5 groups of 3 and 2 groups of 4 = 5*3 + 2*4 = 15 + 8 = 23. 2 are likely to drop, so it's ok
team_sizes_pm = [3, 3, 3, 3, 3, 3, 3, 3, 3] # pm groups has 27 respones, 5 have a likelihood of dropping above 3. Let's 

# Which people aren't allowed to be with each other. Use this if people have requested to not work with others. Use emails.
# Format like this: disallowed_groups = [('example@umich.edu', 'someone@umich.edu')]
disallowed_groups = [
    ("yuchiel@umich.edu", "mrmcmah@umich.edu")
    ] #[("akvenky@umich.edu", "tzuchieh@umich.edu"), ("arattan@umich.edu", "tzuchieh@umich.edu"),
                     # ("ryantsai@umich.edu", "chaojw@umich.edu"), ()] 
# ===============================


# Some asserts
assert project_type in ('Armlab', 'Botlab')
assert section in ('AM', 'PM')

if project_type == 'Botlab':
    assert peer_eval_filename

class Student:
    def __init__(self, id, programming, mechanical, degree, require_4, email, first_name, last_name, preferred_name):
        self.id = id
        self.programming = programming
        self.mechanical = mechanical
        self.degree = degree
        self.require_4 = require_4 # This student must be in a team of 4 students
        
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_name = preferred_name
    
    def to_csv_row(self, use_mech=True):
        value = {
            'Email': self.email,
            'First Name':self.first_name,
            'Last Name': self.last_name,
            'Preferred Name': self.preferred_name,
            'Degree': self.degree,
            'Prog': self.programming,
        }
        if use_mech: value['Mech'] = self.mechanical
        return value
    
# Calculate the total aptitude of a team
def team_aptitude(team):
    avg_programming = sum(student.programming for student in team) / len(team)
    avg_mechanical = sum(student.mechanical for student in team) / len(team)
    return avg_programming, avg_mechanical

# Calculate the balance score for a team assignment
def calculate_balance_score(teams, use_mech=True):
    balance_score = 0
    total_programming = sum(student.programming for team in teams for student in team)
    total_mechanical = sum(student.mechanical for team in teams for student in team)
    total_students = sum(1 for team in teams for student in team)
    
    # Calculate ideal averages
    ideal_programming = total_programming / total_students
    ideal_mechanical = total_mechanical / total_students
    
    for team in teams:
        team_programming, team_mechanical = team_aptitude(team)
        balance_score += abs(team_programming - ideal_programming)
        if use_mech: balance_score += abs(team_mechanical - ideal_mechanical)
    
    return balance_score

# Check if the PhD constraint is violated
def check_phd_constraint(teams):
    for team in teams:
        phd_count = sum(student.degree == 'PhD' for student in team)
        if phd_count > 1:
            return False
    return True

# Check if the disallowed pairs constraint is violated
def check_disallowed_pairs(teams):
    # Look through every team
    for team in teams:
        # Try every combination of students and see if the disallowed pairs constraint is violated
        for student1, student2 in itertools.combinations(team, 2):
            # We only need to check one way because it is symmetric, so no need to do "if student1 in not_allowed_with[student2]"
            if student2.email in not_allowed_with[student1.email]:
                print(f"Disallowed pair found: {student1.email} and {student2.email} are in the same team.")
                return False
            
    return True

# Simulated Annealing Algorithm
def simulated_annealing(students, team_sizes, use_mech=True):
    # Pick out students that require 4
    require_4_students = list(filter(lambda st: st.require_4, students))
    # import pdb; pdb.set_trace()
    
    regular_students = list(filter(lambda st: not st.require_4, students))
    
    BASE_SIZE = 3
    
    # Initial random team assignment
    random.shuffle(regular_students)
    random.shuffle(require_4_students)
    teams = []
    idx = 0
    for _ in range(len(team_sizes)):
        teams.append(regular_students[idx:idx+BASE_SIZE])
        idx += BASE_SIZE

    # Handle students that must be in a team of 4, they are put as the last member of a team
    require_4_students.extend(regular_students[idx:])
    for i, size in enumerate(team_sizes):
        if size == 4:
            teams[i].append(require_4_students.pop())
    
    assert len(require_4_students) == 0
    assert sum(team_sizes) == sum(len(team) for team in teams)

    # Initial temperature and cooling rate
    temperature = 100
    cooling_rate = 0.98
    max_iterations = 9000
    
    current_score = calculate_balance_score(teams, use_mech)
    
    # Main annealing loop
    for iteration in range(max_iterations):
        if temperature < 1e-3:
            break

        # Randomly select two teams and swap members
        team_a, team_b = random.sample(range(len(teams)), 2)
        if teams[team_a][-1].require_4:
            student_a = teams[team_a][random.randint(0,2)]
        else:
            student_a = random.choice(teams[team_a])
        
        if teams[team_b][-1].require_4:
            student_b = teams[team_b][random.randint(0,2)]
        else:
            student_b = random.choice(teams[team_b])
        
        # Create new team configurations by swapping
        new_teams = [team[:] for team in teams]
        new_teams[team_a].remove(student_a)
        new_teams[team_b].remove(student_b)
        new_teams[team_a].insert(0, student_b)
        new_teams[team_b].insert(0, student_a)
        
        # Check the PhD constraint
        if not check_phd_constraint(new_teams):
            continue
        
        # Check the disallowed pair constraint
        if not check_disallowed_pairs(new_teams):
            continue
        
        # Calculate new balance score
        new_score = calculate_balance_score(new_teams)
        
        # Decide whether to accept the new configuration
        if new_score < current_score or random.random() < math.exp((current_score - new_score) / temperature):
            teams = new_teams
            current_score = new_score

        # Decrease the temperature
        temperature *= cooling_rate
    
    print(f'Found teams in {iteration} iterations')
    print('PhD constaint satisfied:', check_phd_constraint(teams))
    print('Disallowed pairs satisfied:', check_disallowed_pairs(teams))

    return teams, current_score


if project_type == 'Armlab':
    students_dict = get_students_armlab(intro_filename, section)
else:
    students_dict = get_students_botlab(intro_filename, peer_eval_filename, section)
students = [
    Student(st['id'], st['programming'], st['mechanical'], st['degree'], st['require_4'], st['email'], st['first_name'], st['last_name'], st['preferred_name'])
    for st in students_dict
]

# print student names
i = 0
for student in students:
    print(i, student.first_name, student.last_name)
    i+=1
    



# For botlab, make previous students not share the same team
if project_type == 'Botlab':
    # import pdb; pdb.set_trace()
    team_count = max(students_dict, key=lambda st: st['prev_team'])['prev_team']
    prev_team_emails = [[] for _ in range(team_count)]
    
    for student in students_dict:
        prev_team_emails[student['prev_team']-1].append(student['email'])
        
    disallowed_groups.extend(prev_team_emails)

# Preprocess disallowed groups
not_allowed_with = defaultdict(list) # For each student, which students aren't allowed with them
for mutually_exclusive in disallowed_groups:
    for student in mutually_exclusive:
        not_allowed_with[student].extend(mutually_exclusive)
# After this, students end up in the "not allowed group" with themselves, which doesn't make sense, so we take that out
for student in not_allowed_with:
    while student in not_allowed_with[student]:
        not_allowed_with[student].remove(student)

# Define team size
team_sizes = team_sizes_am if section == 'AM' else team_sizes_pm


print("Team sizes:", team_sizes)

print(students[0].__dict__)


assert sum(team_sizes) == len(students), print("Team Sizes:", team_sizes, sum(team_sizes), "Total students:", len(students))

# Run Simulated Annealing
optimized_teams, final_score = simulated_annealing(students, team_sizes)

print('Final score: %.3f' % final_score)
print()

# Calculate average aptitudes and format results for display
table = []
for team_id, members in enumerate(optimized_teams):
    if members:
        programming_avg = sum(student.programming for student in members) / len(members)
        
        row = [
            team_id + 1,  # Team number (1-indexed)
            ", ".join(f"{student.id}" for student in members),  # Team members
            round(programming_avg, 2),  # Average programming aptitude
        ]
        if use_mech:
            mechanical_avg = sum(student.mechanical for student in members) / len(members)
            row.append(round(mechanical_avg, 2)) # Average mechanical aptitude
        
        table.append(row)

# Print the results as a table
table_headers = ["Team #", "Team Members", "Prog Apt"]
if use_mech: table_headers.append('Mech Apt')
print(tabulate(table, headers=table_headers, tablefmt="grid"))

# Write to csv
with open(f'ROB550_Teams_{project_type}_{section}.csv', 'w', newline='') as f:
    if use_mech:
        csv_fieldnames = ['Team', 'Email', 'Preferred Name', 'First Name', 'Last Name', 'Degree', 'Prog', 'Mech', 'Team Prog', 'Team Mech']
    else:
        csv_fieldnames = ['Team', 'Email', 'Preferred Name', 'First Name', 'Last Name', 'Degree', 'Prog', 'Team Prog']
        
    writer = csv.DictWriter(f, fieldnames=csv_fieldnames)
    
    writer.writeheader()
    for team_id, members in enumerate(optimized_teams):
        if members:
            programming_avg = round(sum(student.programming for student in members) / len(members), 2)
            
            # Format first student differently to display team stats
            first_team_row = members[0].to_csv_row(use_mech)
            first_team_row.update({
                'Team': team_id+1,
                'Team Prog': programming_avg,
            })
            
            if use_mech:
                mechanical_avg = round(sum(student.mechanical for student in members) / len(members), 2)
                first_team_row['Team Mech'] = mechanical_avg
            
            writer.writerow(first_team_row)
            
            # Format other members
            for member in members[1:]:
                member_row = member.to_csv_row(use_mech)
                member_row['Team'] = team_id+1
                writer.writerow(member_row)