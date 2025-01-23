import os

def process_tree_string(tree_string):
    """Processes tree string, replacing '|' and '|-' with '#' for levels."""
    lines = tree_string.strip().splitlines()
    processed_lines = []
    for line in lines:
        cleaned_line = line.lstrip()  # Remove leading whitespace

        # Count the number of '|' and '|-' to determine the level
        num_hashes = cleaned_line.count("|") + cleaned_line.count("├──")

        # Remove all | and |-
        cleaned_line = cleaned_line.replace("|", "").replace("├──", "").strip()

        processed_line = "#" * num_hashes + " " + cleaned_line
        processed_lines.append(processed_line)
    return "\n".join(processed_lines)

def generate_summary(processed_markdown):
    """Generates the SUMMARY.md content from processed Markdown."""
    lines = processed_markdown.strip().splitlines()
    summary_lines = []
    for line in lines:
        if line.strip():  # check if line is not empty
            level = line.count("#")
            title = line.lstrip("#").strip()
            filename = title.lower().replace(" ", "-") + ".md"  # Create filename
            summary_lines.append(" " * (level - 1) + "* [" + title + "](" + filename + ")")
    return "\n".join(summary_lines)

def create_content_files(processed_output):
    """Creates content files based on the processed output, 
       creating necessary subfolders within 'your-content'."""
    lines = processed_output.strip().splitlines()
    for line in lines:
        if line.strip():  # check if line is not empty
            level = line.count("#")
            title = line.lstrip("#").strip()
            filename = title.lower().replace(" ", "-") + ".md"  # Create filename

            # Extract directory path (excluding 'your-content')
            subdirectory = os.path.dirname(filename) 

            # Construct full path with 'your-content'
            full_path = os.path.join("your-content", subdirectory, filename) 

            # Create directories if necessary
            directory = os.path.dirname(full_path)
            os.makedirs(directory, exist_ok=True)

            with open(full_path, "w") as f:
                f.write("#" * level + " " + title)

def read_tree_from_log(log_file):
    """Reads the tree structure from the log file."""
    with open(log_file, "r") as f:
        return f.read().strip()

# Read tree data from the log file
log_file = "/home/ubuntu/output.log"
tree_data = read_tree_from_log(log_file)

processed_output = process_tree_string(tree_data)
summary_content = generate_summary(processed_output)

# Write SUMMARY.md
with open("SUMMARY.md", "w") as f:
    f.write("# Summary\n\n" + summary_content)

# Create content files
create_content_files(processed_output)

print("SUMMARY.md and content files generated in your-content directory!")