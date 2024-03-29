def render_paper_contents(final_contents):
    """
    Input: list of (section, content) pieces
    """
    rendered_sections = ""
    for section, content in final_contents:
        rendered_sections += f"Title: {section}\n"
        rendered_sections += f"{content}\n\n"
    return rendered_sections