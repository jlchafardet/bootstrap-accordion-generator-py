# Accordion Generator

## Author

- **Name**: José Luis Chafardet G.
- **Email**: <jose.chafardet@icloud.com>
- **GitHub**: [jlchafardet](https://github.com/jlchafardet)

## Description

The Bootstrap Accordion Generator is a Python script that generates a Bootstrap 5.3 accordion HTML structure based on user input. It supports multi-line answers and image URLs, making it a versatile tool for creating interactive web content.

## Features

- **Dynamic Accordion Generation**: Users can create an accordion structure by providing questions and answers.
- **Multi-line Input Support**: Users can enter multi-line answers, which are formatted correctly in the output.
- **Image URL Handling**: Users can append image URLs to answers, which are converted to `<img>` tags in the HTML output.
- **Markdown Link Conversion**: Users can input text with Markdown links, which are converted to HTML links in the output.
- **Unordered List Support**: Contiguous lines starting with `-` are formatted as an unordered list in the output.
- **Unique Identifier Generation**: If the user does not provide a unique identifier, a 4-character UUID is automatically generated.
- **Input Validation**: The script validates user inputs to ensure that:
  - The number of items is a positive integer.
  - Questions and answers cannot be empty.
  - The number of images is a non-negative integer.
- **Error Handling**: Descriptive error messages guide users in correcting invalid inputs.
- **HTML Output**: The generated accordion HTML is exported to a text file named `accordion_<unique_id>.txt`.

## To-Do

- **Custom Accordion**: Add custom accordion format

## Usage

```bash
python accordion_generator.py
```

To use the Accordion Generator, run the script in a Python environment. Follow the prompts to enter the number of accordion items, unique identifier, questions, answers, and any associated images.

### Special Mode for Links

You can also run the script in a special mode to process Markdown links directly:

```bash
python accordion_generator.py links
```

In this mode, you can input text with Markdown links, and the script will convert them to HTML links, formatting contiguous lines starting with `-` as an unordered list.
