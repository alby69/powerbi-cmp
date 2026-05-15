import os
import re

def extract_measures(tmdl_path):
    with open(tmdl_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Split by measure keyword at the start of a line (after a tab or newline)
    # TMDL measures are usually indented once under the table
    parts = re.split(r'\n\tmeasure ', content)

    table_match = re.search(r'table\s+(\S+)', parts[0])
    table_name = table_match.group(1) if table_match else os.path.basename(tmdl_path)

    measures = []

    for part in parts[1:]:
        lines = part.split('\n')
        header = lines[0]

        # Match Name = ...
        name_match = re.match(r"'?([^'=]+)'?\s*=\s*(.*)", header)
        if not name_match:
            continue

        name = name_match.group(1).strip()
        first_line_val = name_match.group(2).strip()

        formula_lines = []
        is_block = False

        if first_line_val == "```":
            is_block = True
            for line in lines[1:]:
                if line.strip() == "```":
                    break
                formula_lines.append(line.strip('\t '))
        elif first_line_val != "":
            formula_lines.append(first_line_val)
        else:
            # Formula starts on next lines
            for line in lines[1:]:
                stripped = line.strip()
                # Check if it's a property
                if not stripped:
                    continue
                if (':' in stripped and not stripped.startswith('//') and not ('"' in stripped and stripped.find(':') > stripped.find('"'))) or stripped.startswith('annotation') or stripped.startswith('changedProperty'):
                    # Likely a property or annotation
                    # TMDL properties are key: value or changedProperty = ...
                    # But we must be careful with DAX formulas containing : (e.g. in strings or some operators?)
                    # Actually TMDL properties are usually at the same indentation level as the formula
                    # but they have a distinct format.

                    # Heuristic: if line has ':', check if it's likely a property
                    if ':' in stripped:
                        key = stripped.split(':')[0]
                        if key in ['formatString', 'displayFolder', 'isHidden', 'lineageTag', 'dataCategory']:
                             break
                    if stripped.startswith('annotation') or stripped.startswith('changedProperty'):
                        break

                formula_lines.append(line.strip('\t '))

        formula = "\n".join(formula_lines).strip()

        # Extract description from annotation PBI_Description
        description = ""
        description_match = re.search(r'annotation PBI_Description = "(.*?)"', part)
        if description_match:
            description = description_match.group(1)

        measures.append({
            "table": table_name,
            "name": name,
            "description": description,
            "formula": formula
        })

    return measures

def main():
    tables_dir = "powerbi/DB_MAGAZZINO_SRC/Model/tables/"
    output_file = "docs/measures_dictionary.md"

    all_measures = []
    if not os.path.exists(tables_dir):
        print(f"Directory {tables_dir} not found.")
        return

    for filename in os.listdir(tables_dir):
        if filename.endswith(".tmdl"):
            measures = extract_measures(os.path.join(tables_dir, filename))
            if measures:
                all_measures.extend(measures)

    # Group by table
    grouped = {}
    for m in all_measures:
        grouped.setdefault(m['table'], []).append(m)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Measures Dictionary\n\n")
        f.write("This document lists all DAX measures defined in the model, organized by table.\n\n")

        for table in sorted(grouped.keys()):
            f.write(f"## {table}\n\n")
            f.write("| Measure Name | Description | Formula |\n")
            f.write("|--------------|-------------|---------|\n")
            for m in grouped[table]:
                # Clean formula for markdown table (replace newlines with <br>, escape |)
                clean_formula = m['formula'].replace('\n', '<br>').replace('|', '\\|')
                f.write(f"| {m['name']} | {m['description']} | `{clean_formula}` |\n")
            f.write("\n")

    print(f"Measures dictionary generated at {output_file}")

if __name__ == "__main__":
    main()
