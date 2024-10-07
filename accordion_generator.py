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

import re  # Import regular expressions for text processing
import uuid  # Import the uuid module for generating unique identifiers
import sys  # Import the sys module to access command-line arguments

def format_answer(answer):
    """
    Replace URLs in the answer with HTML <img> tags.

    Args:
        answer (str): The input string containing URLs.

    Returns:
        str: The formatted answer with URLs replaced by <img> tags.
    """
    # Regex to find all URLs in the answer
    url_pattern = r'(https?://[^\s]+)'
    # Replace URLs with img tags
    formatted_answer = re.sub(url_pattern, r'<img src="\1" alt="Image" />', answer)
    return formatted_answer

def get_multiline_input(prompt):
    """
    Get multi-line input from the user until two consecutive empty lines are entered.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The concatenated multi-line input.
    """
    print(prompt)  # Display the prompt to the user
    lines = []  # Initialize a list to store the lines of input
    empty_line_count = 0  # Counter for consecutive empty lines

    while True:
        line = input()  # Read a line of input from the user
        if line == "":
            empty_line_count += 1  # Increment the empty line counter
            if empty_line_count == 2:  # Check for two consecutive empty lines
                break  # Exit the loop if two empty lines are entered
        else:
            empty_line_count = 0  # Reset counter if a non-empty line is entered
            lines.append(line)  # Add the non-empty line to the list

    return "\n".join(lines)  # Join lines without empty lines and return

def get_positive_integer(prompt):
    """
    Prompt the user for a positive integer input.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        int: The positive integer input by the user.
    """
    while True:  # Loop until a valid input is received
        try:
            value = int(input(prompt))  # Convert user input to an integer
            if value <= 0:  # Check if the value is not positive
                raise ValueError("The number must be a positive integer.")
            return value  # Return the valid positive integer
        except ValueError as e:  # Handle invalid input
            print(f"Invalid input: {e}. Please try again.")  # Inform the user of the error

def get_non_negative_integer(prompt):
    """
    Prompt the user for a non-negative integer input.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        int: The non-negative integer input by the user.
    """
    while True:  # Loop until a valid input is received
        try:
            value = int(input(prompt))  # Convert user input to an integer
            if value < 0:  # Check if the value is negative
                raise ValueError("The number must be a non-negative integer.")
            return value  # Return the valid non-negative integer
        except ValueError as e:  # Handle invalid input
            print(f"Invalid input: {e}. Please try again.")  # Inform the user of the error

def generate_accordion(unique_id, num_items):
    """
    Generate the HTML for an accordion based on user input.

    Args:
        unique_id (str): A unique identifier for the accordion.
        num_items (int): The number of items in the accordion.

    Returns:
        str: The generated HTML content for the accordion.
    """
    # Start the HTML structure for the accordion
    html_content = [f'<div class="accordion" id="accordionParent{unique_id}">\n']
    
    for i in range(num_items):  # Loop through the number of items specified by the user
        while True:  # Loop until a valid question is received
            question = input("Please insert the question: ")  # Prompt for the question
            if question.strip() == "":  # Check if the question is empty
                print("The question can't be empty. Please enter a valid question.")  # Inform the user
            else:
                break  # Exit the loop if a valid question is provided
        
        # Get multi-line input for the answer
        answer = get_multiline_input("Please insert the answer (leave two blank lines to finish): ")
        
        # Process each line in the answer
        processed_lines = []  # Initialize a list to store processed lines of the answer
        in_list = False  # Track if we are currently in a list

        for line in answer.splitlines():  # Split the answer into individual lines
            # Replace Markdown links with HTML links
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
            
            # Replace double asterisks with <strong> tags for bold text
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            
            # Check for heading levels based on the number of leading '#' characters
            if line.startswith('###'):  # Check for level 3 heading
                if in_list:  # If we were in a list, close it
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                processed_lines.append(f'<h3>{line[3:].strip()}</h3>')  # Strip the '###' characters and add heading
            elif line.startswith('##'):  # Check for level 2 heading
                if in_list:  # If we were in a list, close it
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                processed_lines.append(f'<h2>{line[2:].strip()}</h2>')  # Strip the '##' characters and add heading
            elif line.startswith('#'):  # Check for level 1 heading
                if in_list:  # If we were in a list, close it
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                processed_lines.append(f'<h1>{line[1:].strip()}</h1>')  # Strip the '#' character and add heading
            elif line.startswith('-'):  # Check for list items
                if not in_list:  # If we are not already in a list
                    processed_lines.append('<ul>')  # Start a new unordered list
                    in_list = True
                processed_lines.append(f'    <li>{line[1:].strip()}</li>')  # Add list item, stripping the leading '-'
            else:  # For normal lines of text
                if in_list:  # If we were in a list, close it
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                # Add normal lines, replacing newlines with <br /> for HTML formatting
                processed_lines.append(line.replace('\n', '<br />\n'))
        
        # Close any open list at the end
        if in_list:
            processed_lines.append('</ul>')  # Close the unordered list if it was open

        # Join processed lines with <br /> for normal lines
        answer = '\n'.join(processed_lines)
        
        # Ask if the answer has images
        has_images = input("Does this answer have images? (y/n): ").strip().lower()
        
        if has_images == 'y':  # If the user indicates there are images
            num_images = get_non_negative_integer("How many images? ")  # Prompt for the number of images
            for _ in range(num_images):  # Loop through the number of images
                image_url = input("Please enter the image full URL: ")  # Prompt for the image URL
                # Append image in proper format to the answer
                answer += f'\n<br/><img class="img-thumbnail" src="{image_url}" alt="Image" /><br />\n'  
        
        # Generate unique IDs for the accordion items
        heading_id = f"heading{i}"  # Unique ID for the heading
        target_id = f"collapse{i}"  # Unique ID for the collapse section
        
        # Determine the class for the accordion-collapse
        collapse_class = "accordion-collapse collapse show" if i == 0 else "accordion-collapse collapse"
        
        # Append accordion item HTML to the content
        html_content.append(f'''
    <div class="accordion-item">
        <h2 class="accordion-header" id="{heading_id}">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#{target_id}"
                aria-expanded="true" aria-controls="{heading_id}">
                {question}  # Display the question in the button
            </button>
        </h2>
        <div id="{target_id}" class="{collapse_class}" aria-labelledby="{heading_id}"
            data-bs-parent="#accordionParent{unique_id}">
            <div class="accordion-body">
                {answer}  # Display the processed answer in the accordion body
            </div>
        </div>
    </div>
''')
    
    html_content.append('</div>')  # Close the main accordion div
    
    return ''.join(html_content)  # Return the complete HTML content as a string

def main():
    """
    Main function to execute the accordion generator script.

    It checks for command-line arguments to determine if the script should run
    in normal mode or link processing mode.
    """
    # Check for command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "links":  # If the user wants to process links
        # Request multi-line input for links
        links_input = get_multiline_input("Please insert the text with Markdown links (leave two blank lines to finish): ")
        
        # Process the input to convert Markdown links to HTML links
        processed_lines = []  # Initialize a list to store processed lines
        in_list = False  # Track if we are currently in a list

        for line in links_input.splitlines():  # Split the input into lines
            # Check for lines starting with '-'
            if line.startswith('-'):
                if not in_list:  # If we are not already in a list
                    processed_lines.append('<ul>')  # Start a new unordered list
                    in_list = True
                # Convert Markdown link to HTML link
                line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
                processed_lines.append(f'    <li>{line[1:].strip()}</li>')  # Add list item
            else:
                if in_list:  # If we were in a list, close it
                    processed_lines.append('</ul>')  # Close the unordered list if we were in one
                    in_list = False
                # Process non-list lines (convert Markdown links)
                line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
                processed_lines.append(line)  # Add normal line

        # Close any open list at the end
        if in_list:
            processed_lines.append('</ul>')  # Close the unordered list if it was open

        # Join processed lines and output to console
        processed_output = '\n'.join(processed_lines)  # Join the processed lines into a single string
        print("Processed HTML Links:")  # Inform the user about the output
        print(processed_output)  # Print the processed HTML links
        return  # Exit the function after processing links

    # Prompt for the number of items in the accordion
    num_items = get_positive_integer("How many items will this accordion have? ")
    unique_id = input("Please enter a unique identifier for the accordion (leave blank for auto-generated): ")
    
    # Generate a 4-character UUID if the unique_id is empty
    if not unique_id.strip():  # If the user did not provide a unique ID
        unique_id = str(uuid.uuid4())[:4]  # Generate a UUID and take the first 4 characters
    
    accordion_html = generate_accordion(unique_id, num_items)  # Generate the accordion HTML
    
    # Export to file
    file_name = f"accordion_{unique_id}.txt"  # Create a filename based on the unique ID
    with open(file_name, 'w') as file:  # Open the file for writing
        file.write(accordion_html)  # Write the generated HTML to the file
    
    print(f"Accordion HTML has been written to {file_name}")  # Inform the user about the output file

if __name__ == "__main__":  # Check if the script is being run directly
    main()  # Call the main function to execute the script