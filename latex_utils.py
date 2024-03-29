import re

def extract_sections(tex_content):
    """
    Extracts sections and their titles from LaTeX content.
    """
    section_pattern = r'\\section\{(.*?)\}((?:[^\\]|\\(?!section))+)'
    sections = re.findall(section_pattern, tex_content, re.DOTALL)
    return sections

def remove_latex_commands(text):
    """
    Removes LaTeX commands from the text, leaving plain content.
    """
    no_commands = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]+\])?\{[^}]+\}', '', text)
    no_commands = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]+\])?', '', no_commands)
    return no_commands.strip()

def get_main_contents(tex_file_path):
    """
    Generates a summary for the LaTeX document.
    """
    with open(tex_file_path, 'r', encoding='utf-8') as file:
        tex_content = file.read()
    
    sections = extract_sections(tex_content)
    main_contents = []

    for title, content in sections:
        plain_content = remove_latex_commands(content)
        main_contents.append((title, plain_content, len(plain_content.split())))

    return main_contents

# Example usage
# summary = generate_summary('path_to_your_file.tex')
# print(summary)
