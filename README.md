# tmux-screnum

tmux-screnum is a port of the [py-screnum][alexras-py-screnum] script for renumbering windows in [tmux][tmux] sessions. Its goal is to remove any gaps in window numbering that inevitably show up when you're opening and closing a lot of windows in a screen session. It also sorts the windows by name.

**Note** that the script might behave strangely if you don't have automatic window renaming turned off. You can turn off automatic window renaming by adding the following to your `.tmux.conf`:

```
set-window-option -g automatic-rename off
```

[alexras-py-screnum]:https://www.github.com/alexras/py-screnum/
[tmux]: http://tmux.sourceforge.net/
