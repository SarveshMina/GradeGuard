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

# Create the JSON data with the new analytics fields
universities_json = []
for uni in university_lines:
    # Create university object with all required fields
    university_obj = {
        "id": uni,  # Use university name as ID
        "name": uni,
        "counter": 0,
        "majors": majors_list.copy(),  # Use copy to avoid reference issues
        "degrees": {}  # Empty degrees structure, will be populated when modules are added
    }
    
    universities_json.append(university_obj)

# Write the JSON data to the output file with pretty formatting
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(universities_json, f, indent=2, ensure_ascii=False)

print(f"Successfully created {output_file} with {len(universities_json)} university entries.")
print("Each university now includes empty degrees field for module analytics.")