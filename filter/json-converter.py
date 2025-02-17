import json

# Filenames
universities_file = 'universities.csv'
majors_file = 'majors.csv'
output_file = 'universities.json'

# Read universities from CSV (each line is one university name)
with open(universities_file, 'r', encoding='utf-8') as f:
    university_lines = [line.strip() for line in f if line.strip()]

# Read majors from CSV (each line is one major name)
with open(majors_file, 'r', encoding='utf-8') as f:
    major_lines = [line.strip() for line in f if line.strip()]

# Create a list of major objects (each with a counter initialized to 0)
majors_list = [{"major_name": major, "counter": 0} for major in major_lines]

# Create the JSON data:
# For each university, include its name, counter, and the list of majors.
# (Here every university gets the same full list of majors.)
universities_json = [
    {
        "name": uni,
        "counter": 0,
        "majors": majors_list
    }
    for uni in university_lines
]

# Write the JSON data to the output file with pretty formatting
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(universities_json, f, indent=2, ensure_ascii=False)

print(f"Successfully created {output_file} with {len(universities_json)} university entries.")
