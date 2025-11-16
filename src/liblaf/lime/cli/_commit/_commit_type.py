import attrs


@attrs.define
class CommitType:
    type: str
    desc: str = ""


# ref: <https://github.com/conventional-changelog/commitlint/blob/master/%40commitlint/config-conventional/src/index.ts>
# ref: <https://github.com/lobehub/lobe-cli-toolbox/blob/master/packages/lobe-commit/src/constants/gitmojis.ts>
COMMIT_TYPES_LIST: list[CommitType] = [
    CommitType("feat", "A new feature"),
    CommitType("fix", "A bug fix"),
    CommitType("docs", "Documentation only changes"),
    CommitType(
        "style",
        "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
    ),
    CommitType("refactor", "A code change that neither fixes a bug nor adds a feature"),
    CommitType("perf", "A code change that improves performance"),
    CommitType("test", "Adding missing tests or correcting existing tests"),
    CommitType(
        "build", "Changes that affect the build system or external dependencies"
    ),
    CommitType("ci", "Changes to our CI configuration files and scripts"),
    CommitType("chore", "Other changes that don't modify src or test files"),
]


COMMIT_TYPES: dict[str, CommitType] = {ct.type: ct for ct in COMMIT_TYPES_LIST}
