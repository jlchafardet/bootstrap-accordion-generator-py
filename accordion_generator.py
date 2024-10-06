# accordion_generator.py

import re
import uuid  # Import the uuid module for generating unique identifiers

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
        
        # Replace newline characters with <br />
        answer = answer.replace('\n', '<br />')
        
        # Ask if the answer has images
        has_images = input("Does this answer have images? (y/n): ").strip().lower()
        
        if has_images == 'y':
            num_images = get_non_negative_integer("How many images? ")
            for _ in range(num_images):
                image_url = input("Please enter the image full URL: ")
                answer += f'<br><img src="{image_url}" alt="Image" />'  # Append image in proper format
        
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
