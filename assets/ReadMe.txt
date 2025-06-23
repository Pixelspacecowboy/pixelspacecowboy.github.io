# Load and update the README with normalized schema and enhancements
readme_path = "/mnt/data/ReadMe.txt"

with open(readme_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Create updated README content
updated_readme = []
skip_schema_section = False

for line in lines:
    if "## 🚀 Features" in line:
        updated_readme.append(line)
        updated_readme.extend([
            "\n### 🔁 Major Enhancements (Relational Redesign & Reports)\n",
            "- 📘 **Normalized Schema**: Introduced an `authors` table and linked it to `books` via a foreign key.\n",
            "- 🧠 **JOIN Queries**: All view and search operations now use SQL `JOIN` to combine author and book data.\n",
            "- 📊 **Genre Report**: Added a grouped count function using SQL `GROUP BY` to show book totals by genre.\n",
            "- 🗄️ **Relational Integrity**: Author names are now stored once and reused via foreign key relationships.\n",
        ])
    elif "## 🗃️ Database Schema" in line:
        updated_readme.append(line)
        updated_readme.append("\nThe database now includes two normalized tables:\n")
        updated_readme.append("\n### `authors` Table\n")
        updated_readme.append("| Column | Type    | Description         |\n")
        updated_readme.append("|--------|---------|---------------------|\n")
        updated_readme.append("| id     | INTEGER | Primary key (auto)  |\n")
        updated_readme.append("| name   | TEXT    | Author name (unique) |\n")

        updated_readme.append("\n### `books` Table\n")
        updated_readme.append("| Column    | Type    | Description                        |\n")
        updated_readme.append("|-----------|---------|------------------------------------|\n")
        updated_readme.append("| id        | INTEGER | Primary key (auto)                 |\n")
        updated_readme.append("| title     | TEXT    | Title of the book (required)       |\n")
        updated_readme.append("| author_id | INTEGER | Foreign key to `authors(id)`       |\n")
        updated_readme.append("| genre     | TEXT    | Genre/category                     |\n")
        updated_readme.append("| year      | INTEGER | Year of publication                |\n")
        skip_schema_section = True  # Skip old schema
    elif skip_schema_section:
        if line.strip() == "---":
            skip_schema_section = False
            updated_readme.append("\n---\n")
        continue
    else:
        updated_readme.append(line)

# Save updated README
updated_readme_path = "/mnt/data/ReadMe_UPDATED.txt"
with open(updated_readme_path, "w", encoding="utf-8") as f:
    f.writelines(updated_readme)

updated_readme_path
