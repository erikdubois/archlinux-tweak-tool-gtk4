#
# 50-integrations.fish — optional tool integrations (all guarded) and plugin config
#

# fzf key bindings (Ctrl-T directory search) when fzf + the fzf.fish plugin exist.
if command -sq fzf; and type -q fzf_configure_bindings
    fzf_configure_bindings --directory=\ct
end

# direnv per-directory environments.
if type -q direnv
    direnv hook fish | source
end

# tree-based quick directory listings (depth 1/2/3).
if type -q tree
    function l1;  tree --dirsfirst -ChFL 1 $argv; end
    function l2;  tree --dirsfirst -ChFL 2 $argv; end
    function l3;  tree --dirsfirst -ChFL 3 $argv; end
    function ll1; tree --dirsfirst -ChFupDaL 1 $argv; end
    function ll2; tree --dirsfirst -ChFupDaL 2 $argv; end
    function ll3; tree --dirsfirst -ChFupDaL 3 $argv; end
end

# `done` plugin — desktop notification when a long command finishes in an
# unfocused window. The plugin itself is installed via fisher / the Fish Tweak
# Tool, not bundled here; these just tune it when it is present. Use -g, never
# -U: a system payload must not mutate the user's universal variables.
set -g __done_min_cmd_duration 10000          # only notify for commands longer than 10s
set -g __done_notification_urgency_level low   # send the notification at low urgency

# zoxide (smarter cd): install with `pacman -S zoxide`, then enable it in your
# own ~/.config/fish/config.fish with:  zoxide init fish | source
