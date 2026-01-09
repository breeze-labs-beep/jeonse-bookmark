import json
import os
import urllib.parse

files_dir = "files"
output_file = "files.json"

def update_files_json():
    if not os.path.exists(files_dir):
        print(f"Directory '{files_dir}' not found.")
        return

    files_data = []
    
    # List files in the directory
    for filename in os.listdir(files_dir):
        if filename.startswith('.'): # Skip hidden files like .DS_Store
            continue
            
        # Construct URL with encoding
        # We need to encode the filename part
        encoded_filename = urllib.parse.quote(filename)
        url = f"./{files_dir}/{encoded_filename}"
        
        # Create file entry (no description)
        entry = {
            "name": filename,
            "url": url
        }
        files_data.append(entry)
    
    # Sort by name for consistency
    files_data.sort(key=lambda x: x["name"])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(files_data, f, ensure_ascii=False, indent=2)
        
    print(f"Updated {output_file} with {len(files_data)} files.")

if __name__ == "__main__":
    update_files_json()
