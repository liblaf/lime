You are tasked with summarizing code changes into a concise but meaningful commit message. You will be provided with a code diff and optional additional context. Your goal is to analyze the changes and create a clear, informative commit message that accurately represents the modifications made to the code.

First, examine the following code changes provided in git diff format:
<GitDiff>
${GIT_DIFF}
</GitDiff>

Now, if provided, use this context to understand the motivation behind the changes and any relevant background information:
<AdditionalContext>
<RepositoryStructure>
${GIT_FILES}
</RepositoryStructure>
</AdditionalContext>

To create an effective commit message, follow these steps:

1. carefully analyze the diff and context, focusing on:
   - the purpose and rationale of the changes
   - any problems addressed or benefits introduced
   - any significant logic changes or algorithmic improvements
2. ensure the following when composing the commit message:
   - emphasize the "WHY" of the change, its benefits, or the problem it addresses
   - use an informal yet professional tone
   - use a future-oriented manner, third-person singular present tense (e.g., "fixes", "updates", "improves", "adds", "removes")
   - be clear and concise
   - synthesize only meaningful information from the diff and context
   - avoid outputting code, specific code identifiers, names, or file names unless crucial for understanding
   - avoid repeating information, broad generalities, and unnecessary phrases like "this", "this commit", or "this change"
3. summarize the main purpose of the changes in a single, concise sentence, which will be the summary of your commit message
   - start with a third-person singular present tense verb
   - limit to 50 characters if possible
4. if necessary, provide a brief explanation of the changes, which will be the body of your commit message
   - add line breaks for readability and to separate independent ideas
   - focus on the "WHY" rather than the "WHAT" of the changes.
5. if the changes are related to a specific issue or ticket, include the reference (e.g., "fixes #123") at the end of the commit message.

The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

- choose only 1 type from the type-to-description below:
  - feat: introduce new features
  - fix: fix a bug
  - refactor: refactor code that neither fixes a bug nor adds a feature
  - perf: a code change that improves performance
  - style: add or update style files that do not affect the meaning of the code
  - test: adding missing tests or correcting existing tests
  - docs: documentation only changes
  - ci: changes to our CI configuration files and scripts
  - chore: other changes that don't modify src or test file
  - build: make architectural changes
- don't over explain and write your commit message inside <Answer> tags and include no other text
- if the commit involves multiple changes, use markdown unordered list in the commit body to list them clearly
- lines must not be longer than 74 characters

Now, based on the provided code diff and any additional context, create a concise but meaningful commit message following the instructions above.
