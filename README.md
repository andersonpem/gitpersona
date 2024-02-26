# gitpersona

We wear many hats from day to day. GitPersona manages them all.

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
```
