# gitpersona

We wear many hats from day to day. GitPersona manages them all.

**What?**

This utility allows you to choose which identity you want to use when cloning a new repo to your PC. If you work for multiple organizations, or have personal/organization projects, this should come in handy.

**How?**

We wrap a command around Git. When clone is used, we run our utility first. Then once the repo is clone, these commands are automatically executed:

```bash
git config user.name "One of you identities"
git config user.email "oneemail@identity.example"
```

**What you need?**

Python 3 and the packages

- PyYAML

- PtPython

- GitPython

To install them run:

```bash
 pip3 install gitpython pyyaml ptpython
```

**How to use:**

Clone this repo:

```bash
git clone git@github.com:andersonpem/gitpersona.git $HOME/.gitpersona
```

Run this to add it to your path and have a git wrapper:

```bash
# If you use Bash
echo "source $HOME/.gitpersona/gitwrapper" >> $HOME/.bashrc
# If you use ZSH
echo "source $HOME/.gitpersona/gitwrapper" >> $HOME/.zshrc

# If yo use Windows, you should be ashamed of yourself :P
# Run this to refresh your terminal's rc:
source $HOME/.bashrc # or for ZSH:
source $HOME/.zshrc 
```

**Add your first identity:**

```bash
gitpersona-manager add "Andy" "andy@example.com"
# Gitpersona will return:
Identity 'Andy' added.
```

Now clone a repo and you'll be asked for an identity. The identity selection has autocomplete with tab.
