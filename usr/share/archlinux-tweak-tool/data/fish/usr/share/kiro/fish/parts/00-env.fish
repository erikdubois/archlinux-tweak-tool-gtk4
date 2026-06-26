#
# 00-env.fish — core environment for ALL shells (sourced before the interactive guard)
#

# Prepend user-local bin dirs so non-interactive scripts inherit them too.
for dir in $HOME/.local/bin $HOME/.bin
    if test -d $dir; and not contains $dir $PATH
        set -gx PATH $dir $PATH
    end
end

# Default editor used by the shell and many CLI tools.
set -gx EDITOR nano   # command-line editor
set -gx VISUAL nano   # full-screen editor (same as EDITOR here)

# Render man pages through bat (colour + paging) when bat is installed.
if type -q bat
    set -gx MANPAGER "sh -c 'col -bx | bat -l man -p'"
    set -gx MANROFFOPT -c
end
