import os
from blog_reader import *

# runs only when the script is executed, not when it's imported
if __name__ == "__main__":
    base_path = './'
    output_file = "blog.md"

# write to output file
with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write('# Blogs\n\n')

        entries = os.listdir(base_path)
        directories = [entry for entry in entries if os.path.isdir(os.path.join(base_path, entry))]
        directories.sort(reverse=True) # sort years from newest to oldest

        for year in directories:
            f.write(f'## {year}\n')

            year_path = f'{base_path}/{year}'
            entries = os.listdir(year_path)

            f.write(gen_grid(year_path))
            f.write('\n<br><br>\n\n')
