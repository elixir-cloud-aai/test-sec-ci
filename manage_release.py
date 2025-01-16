"""Create changelog and manage releases."""

import argparse
import subprocess
from datetime import datetime
from pathlib import Path


class DockerImageRelease:
    """Class to bump image version.

    Arguments:
        image_type: Image to release, jupyterhub or notebook.

    Attributes:
        image_type: Image to release, jupyterhub or notebook.
        version_file: Path of the version file for the image.
        changelog_file: Path of the changelog file.
    """

    def __init__(self, image_type: str):
        """Class init."""
        self.image_type = image_type
        self.version_file = Path(f"jupyterhub/{image_type}/VERSION")
        self.changelog_file = Path(f"CHANGELOG.{image_type}.md")

    def get_current_version(self) -> str:
        """Get the current version of the images.

        Read the version mentioned in the `VERSION` file
        of the selected image and return.

        Returns:
            str: Version of the image.
        """
        if self.version_file.exists():
            return self.version_file.read_text().strip()
        return "0.0.0"

    def bump_version(self, bump_type="patch"):
        """Bump the version of the image.

        Arguments:
            bump_type: `patch`, `minor` or `major`.
        """
        current = self.get_current_version()
        major, minor, patch = map(int, current.split("."))

        if bump_type == "major":
            major += 1
            minor = patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        else:
            patch += 1

        new_version = f"{major}.{minor}.{patch}"
        self.version_file.write_text(new_version)
        return new_version

    def update_changelog(self, version, changes):
        """Updates the change log.

        Arguments:
            version: New version image is getting updated to.
            changes: Message to add to changelog.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        new_entry = f"""
## [{version}] - {today}

### {self.image_type.capitalize()} Image
{changes}
"""
        current_changelog = (
            self.changelog_file.read_text()
            if self.changelog_file.exists()
            else "# Changelog\n"
        )
        unreleased_pos = current_changelog.find("## [Unreleased]")

        if unreleased_pos == -1:
            updated_changelog = current_changelog + new_entry
        else:
            updated_changelog = (
                current_changelog[:unreleased_pos]
                + "## [Unreleased]\n\n"
                + new_entry
                + current_changelog[unreleased_pos:].split("## [")[1:]
            )  # type: ignore

        self.changelog_file.write_text(updated_changelog)

    def create_git_tag(self, version):
        """Create a git tag for the image with version."""
        tag = f"{self.image_type}-v{version}"
        subprocess.run(["git", "tag", tag], check=False)
        subprocess.run(["git", "push", "origin", tag], check=False)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(description="Manage Docker image releases")
    parser.add_argument(
        "image_type", choices=["hub", "notebook"], help="Type of image to release"
    )
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        default="patch",
        help="Version bump type",
    )
    parser.add_argument("--changes", type=str, help="Changelog entry content")

    args = parser.parse_args()

    release = DockerImageRelease(args.image_type)
    new_version = release.bump_version(args.bump)

    if args.changes:
        release.update_changelog(new_version, args.changes)

    # Commit changes
    subprocess.run(
        ["git", "add", f"{args.image_type}/VERSION", "CHANGELOG.md"], check=False
    )
    subprocess.run(
        ["git", "commit", "-m", f"chore(release): {args.image_type} v{new_version}"],
        check=False,
    )

    # Create and push tag
    release.create_git_tag(new_version)

    print(f"Released {args.image_type} v{new_version}")


if __name__ == "__main__":
    main()
