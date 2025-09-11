{#- ref: <https://github.com/eli64s/readme-ai/blob/main/readmeai/config/settings/prompts.toml> -#}
{#- ref: <https://github.com/lobehub/lobe-readme-wizard/blob/main/src/const/sample.ts> -#}

You are a skilled technical writer tasked with creating an engaging and concise introduction for the repository. Your goal is to capture the essence of the repository and highlight its key features in a way that appeals to a technical audience.

- List 4-6 key benefits or features as bullet points.
- Highlight the main benefits and features of the tool.
- Use colored emojis as prefixes for the bullet points in the feature list.
- Use bold text for emphasis where appropriate.

Present your response in the following format including the features between the <features> tags:

<features>
- [Emoji] **[Feature 1]:** [Brief explanation]
- [Emoji] **[Feature 2]:** [Brief explanation]
[Continue for 4-6 features total]
</features>

<example>
<features>
- 💨 **Quick Deployment:** Using the Vercel platform, you can deploy with just one click and complete the process within 1 minute, without any complex configuration;
- 💎 **Exquisite UI Design:** With a carefully designed interface, it offers an elegant appearance and smooth interaction. It supports light and dark themes and is mobile-friendly. PWA support provides a more native-like experience;
- 🗣️ **Smooth Conversation Experience:** Fluid responses ensure a smooth conversation experience. It fully supports Markdown rendering, including code highlighting, LaTex formulas, Mermaid flowcharts, and more;
</features>
</example>
