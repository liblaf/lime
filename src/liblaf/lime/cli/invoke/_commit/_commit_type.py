import attrs


@attrs.define
class CommitType:
    type: str
    desc: str = ""


# ref: <https://github.com/lobehub/lobe-cli-toolbox/blob/master/packages/lobe-commit/src/constants/gitmojis.ts>
COMMIT_TYPES_LIST: list[CommitType] = [
    CommitType("feat", "Introduce new features"),
    CommitType("fix", "Fix a bug"),
    CommitType("refactor", "Refactor code that neither fixes a bug nor adds a feature"),
    CommitType("perf", "A code change that improves performance"),
    CommitType(
        "style", "Add or update style files that do not affect the meaning of the code"
    ),
    CommitType("test", "Adding missing tests or correcting existing tests"),
    CommitType("docs", "Documentation only changes"),
    CommitType("ci", "Changes to our CI configuration files and scripts"),
    CommitType("chore", "Other changes that dont modify src or test file"),
    CommitType("build", "Make architectural changes"),
]


COMMIT_TYPES: dict[str, CommitType] = {ct.type: ct for ct in COMMIT_TYPES_LIST}
