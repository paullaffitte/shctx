# shctx

A context manager for your shell

```bash
pip install shctx

# Download example configuration
mkdir -p ~/.shctx
wget https://raw.githubusercontent.com/paullaffitte/shctx/main/config.example.yaml -O ~/.shctx/config.yaml

# Set current context to "work"
shctx --set work
```

## Using shctx as your login shell

To use shctx as your login shell, simply run the following command: `sudo usermod --shell /home/linuxbrew/.linuxbrew/bin/shctx "$USER"`.

shctx is meant to be completely transparent in the usage of your shell. I'm used to close my terminal by closing my shell, usually with `ctrl+D`, sometimes with `exit` command, but running shctx from my login shell forced me to close 2 shells to close my terminal (the original bash, and the bash in an shctx context). Running shctx as my login shell allows me to quit my terminal all at once. Also, switching between contexts replace the bash instance in context `A` with a bash instance in context `B`; it quits the former to start the latter, leaving again only one action to take to close the terminal.

⚠️ Don't use shctx as your login shell for root account! If for any reason shctx can't start, you will not be able to login as root and could be in trouble.
