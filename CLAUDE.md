# PROJECT: TAC Knowledge Architecture

## ALWAYS DO FIRST:
1. Read /docs/3_ontology.txt (pillar definitions)
2. Read /data/pillar_7_reference.json (structure template)
3. Read relevant pillar file in /data/ (e.g., pillar1-topicdomain.json, pillar_2.json, etc.)

## FILE STRUCTURE:
- Individual pillar files: pillar1-topicdomain.json, pillar_2.json through pillar_8.json
- Reference template: pillar_7_reference.json
- This isolates each pillar to prevent cross-contamination during development

## RULES:
- Never generate content for a pillar without stating its boundaries first
- One pillar per session
- Generate one layer at a time (Sub-Pillars → Branches → Topic Domains)
- Always validate before committing
- Match the scale and structure of Pillar 7 reference

## OUTPUT FORMAT:
- All architecture work outputs as JSON matching pillar_7_reference.json structure
- Commit messages format: "Pillar X: [action] - Y Sub-Pillars, Z Branches, N Topic Domains"
