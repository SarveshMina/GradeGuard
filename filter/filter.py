# import csv

# input_file = 'world-universities.csv'
# output_file = 'universities.csv'

# with open(input_file, newline='', encoding='utf-8') as csv_in, \
#      open(output_file, 'w', newline='', encoding='utf-8') as csv_out:
    
#     reader = csv.reader(csv_in)
#     writer = csv.writer(csv_out)
    
#     # Optionally, write a header. Uncomment the next line if needed.
#     # writer.writerow(["University Name"])
    
#     for row in reader:
#         if len(row) > 1:
#             writer.writerow([row[1]])

# print(f"Created '{output_file}' with university names only.")
# import csv

# input_file = 'majors-list.csv'
# output_file = 'majors.csv'

# with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
#      open(output_file, 'w', newline='', encoding='utf-8') as outfile:
#     reader = csv.DictReader(infile)
#     # Create a simple CSV writer for the output
#     writer = csv.writer(outfile)
    
#     # Write a header row if desired
#     writer.writerow(['Major'])
    
#     # Iterate through each row in the input CSV
#     for row in reader:
#         # Write only the Major column to the output
#         writer.writerow([row['Major']])

import csv

input_file = 'world-universities.csv'
output_file = 'universities.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Only proceed if the row isn't empty and the first column is US or GB
        if row and row[0] in ['US', 'GB']:
            # Write just the second column (the university name)
            writer.writerow([row[1]])

print(f"Filtered universities saved to {output_file}.")

