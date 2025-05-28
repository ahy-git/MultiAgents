import os

AGENT_DIR = "."  # Root path of your MultiAgents repo
README_PATH = "README.md"
START_MARKER = "<!-- AGENTS_START -->"
END_MARKER = "<!-- AGENTS_END -->"

# Directories to ignore
EXCLUDE = {
    ".git", "__pycache__", "venv",
    ".idea", ".vscode", ".DS_Store",
    "requirements.txt", "README.md", ".envGIT", ".gitignore",
    "crew_profile_generator.py", "agents.yaml", "tasks.yaml"
}
EXCLUDE_PREFIXES = ["AHYPRJ"]

def get_agent_directories(path):
    return sorted([
        name for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
        and name not in EXCLUDE
        and not name.startswith("__")
        and not any(name.startswith(prefix) for prefix in EXCLUDE_PREFIXES)
    ])

def get_description(agent_dir):
    desc_path = os.path.join(agent_dir, "description.md")
    if os.path.isfile(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            return f.read().strip().replace("\n", " ")
    return "No description available."


def generate_agent_list(agent_dirs):
    markdown = "| Directory | Description (Optional) |\n|-----------|------------------------|\n"
    for agent in agent_dirs:
        desc = get_description(agent)
        markdown += f"| `{agent}` | {desc} |\n"
    return markdown

def update_readme(agent_section):
    if not os.path.exists(README_PATH):
        print("README.md not found. Creating new one.")
        with open(README_PATH, "w") as f:
            f.write("# MultiAgents\n\n" + START_MARKER + "\n" + agent_section + "\n" + END_MARKER)
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER in content and END_MARKER in content:
        before = content.split(START_MARKER)[0]
        after = content.split(END_MARKER)[1]
        new_content = before + START_MARKER + "\n" + agent_section + "\n" + END_MARKER + after
    else:
        new_content = content + "\n\n" + START_MARKER + "\n" + agent_section + "\n" + END_MARKER

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    dirs = get_agent_directories(AGENT_DIR)
    agent_md = generate_agent_list(dirs)
    update_readme(agent_md)
    print("✅ README.md updated with current agent directories.")
