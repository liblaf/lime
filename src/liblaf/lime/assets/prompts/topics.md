Generate relevant topics for a GitHub repository.

# Steps

1. **Analyze the Codebase**: Review the merged representation of the entire codebase, focusing on the metadata, repository structure, and individual file contents.
2. **Identify Key Elements**: Determine the primary purpose, subject area, and programming language used in the project.
3. **Highlight Unique Features**: Note any unique or standout features of the project that could attract contributors.
4. **Generate Topics**: Create a list of up to 20 topics that reflect the analysis. Ensure each topic is concise, lowercase, and uses hyphens if necessary.

# Output Format

Output the list of topics as a single line of text, with each topic separated by a space. Each topic should be in lowercase and use hyphens if necessary.

<Answer>
topic1 topic2 topic3 ...
</Answer>

# Examples

<Example>
<Input>
(codebase of tqdm ...)
</Input>
<Answer>
python cli console gui time terminal telegram utilities jupyter progress discord progress-bar parallel keras meter progressbar pandas progressmeter rate closember
</Answer>
</Example>

# Notes

- Ensure that the topics are relevant to the repository's content and purpose.
- Each topic should be concise and descriptive, with no more than 50 characters.
- Use hyphens to separate words within a topic if necessary.
