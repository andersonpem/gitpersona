#!/usr/bin/env python3
import argparse
import os
import signal
import sys

import yaml
from git import Repo
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import signal
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
IDENTITY_FILE = os.path.join(script_dir, 'identities.yaml')


# Define the signal handler function
def signal_handler(sig, frame):
    print('\nExiting gracefully...')
    sys.exit(0)


# Set the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Set the signal handler for SIGTERM
signal.signal(signal.SIGTERM, signal_handler)


def load_identities():
    if os.path.exists(IDENTITY_FILE):
        with open(IDENTITY_FILE, 'r') as file:
            return yaml.safe_load(file) or {}
    return {}


def save_identities(identities):
    with open(IDENTITY_FILE, 'w') as file:
        yaml.safe_dump(identities, file)


def add_identity(args):
    identities = load_identities()
    identity = f"{args.name}: {args.email}"
    if identity in identities:
        print(f"Identity '{identity}' already exists.")
    else:
        identities[identity] = args.email
        save_identities(identities)
        print(f"Identity '{identity}' added.")


def remove_identity(args):
    identities = load_identities()
    identity = f"{args.name}: {args.email}"
    if identity in identities:
        del identities[identity]
        save_identities(identities)
        print(f"Identity '{identity}' removed.")
    else:
        print(f"No identity found for '{identity}'.")


def edit_identity(args):
    identities = load_identities()
    identity_completer = WordCompleter(list(identities.keys()))
    identity = prompt("Choose an identity to edit [You can use tab to autocomplete]: ", completer=identity_completer)

    while identity not in identities.keys():
        print("Invalid identity. Please try again.")
    identity = prompt("Choose an identity: ", completer=identity_completer)

    old_name, old_email = identity.split(": ")
    edit_choice = input("Do you want to edit the name, email, or both? (Enter 'name', 'email', or 'both'): ")

    new_name = old_name
    new_email = old_email

    if edit_choice in ['name', 'both']:
        new_name = input("Enter the new name: ")
        del identities[old_name]  # Remove the old identity
    if edit_choice in ['email', 'both']:
        new_email = input("Enter the new email: ")

    identities[new_name] = new_email  # Add the updated identity
    save_identities(identities)
    print(f"Identity '{old_name}: {old_email}' edited to '{new_name}: {new_email}'.")


def list_identities(args):
    identities = load_identities()
    if not identities:
        print("No identities found.")
    else:
        for identity in identities.keys():
            name, email = identity.split(": ")
            print(name)


def clone_repository(args):
    identities = load_identities()
    identity_completer = WordCompleter(list(identities.keys()))
    print("Cloning repo, but first...")
    identity = prompt("Choose an identity for commits [you can use tab to autocomplete]: ", completer=identity_completer)

    while identity not in identities.keys():
        print("Invalid identity. Please try again.")
        identity = prompt("Choose an identity: ", completer=identity_completer)

    name, email = identity.split(": ")
    repo_name = args.directory or args.url.split('/')[-1].replace('.git', '')
    Repo.clone_from(args.url, repo_name)
    repo = Repo(repo_name)
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", name)
        git_config.set_value("user", "email", email)
    print(f"Repository '{repo_name}' cloned with identity '{name}'.")

    if not os.path.exists(repo_name):
        print(f"Directory '{repo_name}' does not exist. Please check the repository cloning process.")
        return

    os.chdir(repo_name)


def switch_identity(args):
    repo_path = args.repo_path or '.'
    os.chdir(repo_path)
    repo = Repo('.')
    if not repo.bare:
        identities = load_identities()
        identity_completer = WordCompleter(list(identities.keys()))
        print("Switching identity in the current project.")
        identity = prompt("Choose an identity [you can use tab to autocomplete]: ", completer=identity_completer)

        while identity not in identities.keys():
            print("Invalid identity. Please try again.")
            identity = prompt("Choose an identity: ", completer=identity_completer)

        name, email = identity.split(": ")
        with repo.config_writer() as git_config:
            git_config.set_value("user", "name", name)
            git_config.set_value("user", "email", email)
        print(f"Identity switched to '{name}'.")
    else:
        print("Not a Git repository.")


def main():
    parser = argparse.ArgumentParser(description="Git Identity Manager")
    subparsers = parser.add_subparsers(help="commands")

    # Add identity command
    parser_add = subparsers.add_parser('add', help='Add a new identity')
    parser_add.add_argument('name', help='Identity name')
    parser_add.add_argument('email', help='Email address')
    parser_add.set_defaults(func=add_identity)

    # Remove identity command
    parser_remove = subparsers.add_parser('remove', help='Remove an existing identity')
    parser_remove.add_argument('name', help='Identity name')
    parser_remove.add_argument('email', help='Email address')
    parser_remove.set_defaults(func=remove_identity)

    # List identities command
    parser_list = subparsers.add_parser('list', help='List all identities')
    parser_list.set_defaults(func=list_identities)

    # Clone repository command
    parser_clone = subparsers.add_parser('clone', help='Clone a repository with a specified identity')
    parser_clone.add_argument('url', help='Repository URL')
    parser_clone.add_argument('directory', nargs='?', default=None, help='Directory to clone the repository into')
    parser_clone.set_defaults(func=clone_repository)

    # Switch identity command
    parser_switch = subparsers.add_parser('switch', help='Switch identity in an existing project')
    parser_switch.add_argument('repo_path', help='Path to the Git repository')
    parser_switch.set_defaults(func=switch_identity)

    # Edit identity command
    parser_edit = subparsers.add_parser('edit', help='Edit an existing identity')
    parser_edit.set_defaults(func=edit_identity)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted by user')
        try:
            sys.exit(0)
        except SystemExit:
            sys.exit(0)