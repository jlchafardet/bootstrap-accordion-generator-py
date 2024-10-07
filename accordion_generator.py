# ============================================================================ 
# Author: José Luis Chafardet G. 
# Email: jose.chafardet@icloud.com 
# Github: https://github.com/jlchafardet 
# 
# File Name: accordion_generator.py 
# Description: A Python script to generate an accordion HTML structure based 
# on user input, including support for multi-line answers and image URLs. 
# Created: 2023-10-01 
# Last Modified: 2023-10-01 
# ============================================================================ 

import re
import uuid  # Import the uuid module for generating unique identifiers
import sys  # Import the sys module to access command-line arguments

def format_answer(answer):
    # Regex to find all URLs in the answer
    url_pattern = r'(https?://[^\s]+)'
    # Replace URLs with img tags
    formatted_answer = re.sub(url_pattern, r'<img src="\1" alt="Image" />', answer)
    return formatted_answer

def get_multiline_input(prompt):
    print(prompt)
    lines = []
    empty_line_count = 0  # Counter for consecutive empty lines

    while True:
        line = input()
        if line == "":
            empty_line_count += 1
            if empty_line_count == 2:  # Check for two consecutive empty lines
                break
        else:
            empty_line_count = 0  # Reset counter if a non-empty line is entered
            lines.append(line)

    return "\n".join(lines)  # Join lines without empty lines

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError("The number must be a positive integer.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def get_non_negative_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError("The number must be a non-negative integer.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def generate_accordion(unique_id, num_items):
    html_content = [f'<div class="accordion" id="accordionParent{unique_id}">\n']
    
    for i in range(num_items):
        while True:
            question = input("Please insert the question: ")
            if question.strip() == "":
                print("The question can't be empty. Please enter a valid question.")
            else:
                break
        
        # Get multi-line input for the answer
        answer = get_multiline_input("Please insert the answer (leave two blank lines to finish): ")
        
        # Process each line in the answer
        processed_lines = []
        in_list = False  # Track if we are currently in a list

        for line in answer.splitlines():
            # Replace Markdown links with HTML links
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
            
            # Replace double asterisks with <strong> tags
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            
            # Check for heading levels based on the number of leading '#' characters
            if line.startswith('###'):
                if in_list:
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                processed_lines.append(f'<h3>{line[3:].strip()}</h3>')  # Strip the '###' characters
            elif line.startswith('##'):
                if in_list:
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                processed_lines.append(f'<h2>{line[2:].strip()}</h2>')  # Strip the '##' characters
            elif line.startswith('#'):
                if in_list:
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                processed_lines.append(f'<h1>{line[1:].strip()}</h1>')  # Strip the '#' character
            elif line.startswith('-'):
                if not in_list:
                    processed_lines.append('<ul>')  # Start a new unordered list
                    in_list = True
                processed_lines.append(f'    <li>{line[1:].strip()}</li>')  # Add list item
            else:
                if in_list:
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                # Add normal lines
                processed_lines.append(line.replace('\n', '<br />\n'))
        
        # Close any open list at the end
        if in_list:
            processed_lines.append('</ul>')

        # Join processed lines with <br /> for normal lines
        answer = '\n'.join(processed_lines)
        
        # Ask if the answer has images
        has_images = input("Does this answer have images? (y/n): ").strip().lower()
        
        if has_images == 'y':
            num_images = get_non_negative_integer("How many images? ")
            for _ in range(num_images):
                image_url = input("Please enter the image full URL: ")
                answer += f'\n<br/><img class="img-thumbnail" src="{image_url}" alt="Image" /><br />\n'  # Append image in proper format
        
        # Generate unique IDs
        heading_id = f"heading{i}"
        target_id = f"collapse{i}"
        
        # Determine the class for the accordion-collapse
        collapse_class = "accordion-collapse collapse show" if i == 0 else "accordion-collapse collapse"
        
        # Append accordion item HTML
        html_content.append(f'''
    <div class="accordion-item">
        <h2 class="accordion-header" id="{heading_id}">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#{target_id}"
                aria-expanded="true" aria-controls="{heading_id}">
                {question}
            </button>
        </h2>
        <div id="{target_id}" class="{collapse_class}" aria-labelledby="{heading_id}"
            data-bs-parent="#accordionParent{unique_id}">
            <div class="accordion-body">
                {answer}
            </div>
        </div>
    </div>
''')
    
    html_content.append('</div>')
    
    return ''.join(html_content)

def main():
    # Check for command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "links":
        # Request multi-line input for links
        links_input = get_multiline_input("Please insert the text with Markdown links (leave two blank lines to finish): ")
        
        # Process the input to convert Markdown links to HTML links
        processed_lines = []
        in_list = False  # Track if we are currently in a list

        for line in links_input.splitlines():
            # Check for lines starting with '-'
            if line.startswith('-'):
                if not in_list:
                    processed_lines.append('<ul>')  # Start a new unordered list
                    in_list = True
                # Convert Markdown link to HTML link
                line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
                processed_lines.append(f'    <li>{line[1:].strip()}</li>')  # Add list item
            else:
                if in_list:
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                # Process non-list lines (convert Markdown links)
                line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
                processed_lines.append(line)  # Add normal line

        # Close any open list at the end
        if in_list:
            processed_lines.append('</ul>')

        # Join processed lines and output to console
        processed_output = '\n'.join(processed_lines)
        print("Processed HTML Links:")
        print(processed_output)
        return  # Exit the function after processing links

    num_items = get_positive_integer("How many items will this accordion have? ")
    unique_id = input("Please enter a unique identifier for the accordion (leave blank for auto-generated): ")
    
    # Generate a 4-character UUID if the unique_id is empty
    if not unique_id.strip():
        unique_id = str(uuid.uuid4())[:4]  # Generate a UUID and take the first 4 characters
    
    accordion_html = generate_accordion(unique_id, num_items)
    
    # Export to file
    file_name = f"accordion_{unique_id}.txt"
    with open(file_name, 'w') as file:
        file.write(accordion_html)
    
    print(f"Accordion HTML has been written to {file_name}")

if __name__ == "__main__":
    main()