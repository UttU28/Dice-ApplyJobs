# Input list of dictionaries
data = [
    {'id': 'c6393e4b-9de1-4829-9746-2165579c70ab', 'email': 'aluhar@gmail.com', 'selectedResume': 'Python_Utsav_Chaudhary_Resume.pdf', 'timeOfArrival': '1723366049'},
    {'id': '27345a04-0bfa-4221-aa99-4a12b5a95454', 'email': 'utsavmaan28@gmail.com', 'selectedResume': 'Utsav_Chaudhary_Resume.pdf', 'timeOfArrival': '1723366111'},
    {'id': '41a7047e-307c-471b-bba0-9cd2f17853fd', 'email': 'utsavmaan28@gmail.com', 'selectedResume': 'Python Utsav Chaudhary Resume.pdf', 'timeOfArrival': '1723372910'},
    {'id': '34a591bb-0497-49c2-b7ac-9742b73fd39b', 'email': 'aluhar@gmail.com', 'selectedResume': 'Utsav_Chaudhary_Resume.pdf', 'timeOfArrival': '1723372913'}
]

# Initialize an empty dictionary to store the results
result = {}

# Process each entry in the input data
for entry in data:
    email = entry['email']
    job_id = entry['id']
    resume = entry['selectedResume']
    
    # Create a new entry if the email is not already in the result
    if email not in result:
        result[email] = []
    
    # Append the [job_id, resume] pair to the list for the email
    result[email].append([job_id, resume])

# Print the result
print(result)
