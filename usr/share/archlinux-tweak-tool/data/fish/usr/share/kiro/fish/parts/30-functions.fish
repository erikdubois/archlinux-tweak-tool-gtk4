#
# 30-functions.fish — shell helper functions
#

# Restart fish to reload its configuration after editing.
function reload --description 'Restart fish to reload config'
    exec fish
end

# Command history with timestamps, oldest first.
function history --description 'History with timestamps'
    builtin history --show-time='%F %T ' | sort
end

# Quick backup: backup <file> -> <file>.bak
function backup --argument filename --description 'Copy a file to <file>.bak'
    cp $filename $filename.bak
end

# Copy — recursive when the source is a directory (adapted from CachyOS, using
# fish's native string builtin instead of a trim-right helper).
function copy --description 'cp, recursive when copying a directory'
    if test (count $argv) = 2; and test -d "$argv[1]"
        command cp -r (string trim --right --chars=/ -- $argv[1]) $argv[2]
    else
        command cp $argv
    end
end

# List the last n (default 100) installed packages.
function ripp --argument length --description 'List the last n (100) packages installed'
    if test -z $length
        set length 100
    end
    expac --timefmt='%Y-%m-%d %T' '%l\t%n' | sort | tail -n $length | nl
end

# Browse the git log interactively with fzf (preview a commit with Enter).
function gl --description 'Interactive git log via fzf'
    git log --graph --color=always --format="%C(auto)%h%d %s %C(black)%C(bold)%cr" $argv | fzf --ansi --no-sort --reverse --tiebreak=index --toggle-sort=\` --bind "ctrl-m:execute: echo '{}' | grep -o '[a-f0-9]\{7\}' | head -1 | xargs -I % sh -c 'git show --color=always % | less -R'"
end

# Extract most bundled & compressed file types: ex <archive>
function ex --description "Extract bundled & compressed files"
    if test -f "$argv[1]"
        switch $argv[1]
            case '*.tar.bz2'
                tar xjf $argv[1]
            case '*.tar.gz'
                tar xzf $argv[1]
            case '*.bz2'
                bunzip2 $argv[1]
            case '*.rar'
                unrar x $argv[1]
            case '*.gz'
                gunzip $argv[1]
            case '*.tar'
                tar xf $argv[1]
            case '*.tbz2'
                tar xjf $argv[1]
            case '*.tgz'
                tar xzf $argv[1]
            case '*.zip'
                unzip $argv[1]
            case '*.Z'
                uncompress $argv[1]
            case '*.7z'
                7z $argv[1]
            case '*.deb'
                ar x $argv[1]
            case '*.tar.xz'
                tar xf $argv[1]
            case '*.tar.zst'
                tar xf $argv[1]
            case '*'
                echo "'$argv[1]' cannot be extracted via ex"
        end
    else
        echo "'$argv[1]' is not a valid file"
    end
end

# Always page less with raw control chars (colours survive).
function less
    command less -R $argv
end

# cd that lists the directory it lands in.
function cd
    builtin cd $argv; and ls
end

# Show which installed packages require the given package: depends <pkg>
function function_depends
    set search $argv[1]
    sudo pacman -Sii $search | grep "Required" | sed -e "s/Required By     : //g" | sed -e "s/  /\n/g"
end

# Edit /etc/hblock/allow.list, creating the dir/file if missing.
function nhblockallow --description "Edit /etc/hblock/allow.list, creating dir/file if missing"
    if not test -f /etc/hblock/allow.list
        sudo mkdir -p /etc/hblock
        sudo touch /etc/hblock/allow.list
    end
    sudo nano /etc/hblock/allow.list
end

# Remove orphaned packages — no-op (and no error) when there are none.
function cleanup --description 'Remove orphaned packages'
    set -l orphans (pacman -Qtdq)
    if test -n "$orphans"
        sudo pacman -Rns $orphans
    else
        echo "No orphaned packages to remove."
    end
end

# Categorised overview of everything this Kiro fish config ships — helper
# functions, aliases (grouped by their section dividers), and keybindings.
# Parses the live parts/*.fish so it never drifts from what is actually loaded.
function fish-help --description 'Overview of Kiro fish functions, aliases & keybindings'
    set -l parts /usr/share/kiro/fish/parts
    if not test -d $parts
        echo "fish-help: parts not found at $parts (package not installed?)" >&2
        return 1
    end

    set -l hdr ''; set -l rst ''
    if isatty stdout
        set hdr (set_color -o cyan); set rst (set_color normal)
    end

    echo $hdr"Kiro fish config — overview"$rst
    echo "Source: $parts/*.fish   ·   live lookups: functions NAME · type NAME · alias"
    echo

    # ── Functions ─────────────────────────────────────────────────────────────
    echo $hdr"FUNCTIONS"$rst" (30-functions.fish)"
    for line in (cat $parts/30-functions.fish)
        string match -qr '^function ' -- $line; or continue
        set -l name (string replace -r '^function ([^ ]+).*' '$1' -- $line)
        set -l desc (string replace -r ".*--description ['\"]([^'\"]+)['\"].*" '$1' -- $line)
        test "$desc" = "$line"; and set desc ''
        printf "  %-18s %s\n" $name $desc
    end
    echo

    # ── Aliases (grouped by their section dividers) ───────────────────────────
    # The header is held in $pending and only printed once an alias appears under
    # it, so empty sections (e.g. the commented-out personal block) are dropped.
    echo $hdr"ALIASES"$rst" (40-aliases.fish)"
    set -l pending ''
    for line in (cat $parts/40-aliases.fish)
        if string match -qr '^#\s*──' -- $line
            set pending (string replace -r '^#\s*──\s*(.*?)\s*─.*$' '$1' -- $line)
        else if string match -qr '^\s*alias ' -- $line
            if test -n "$pending"
                printf "\n  %s%s%s\n" $hdr $pending $rst
                set pending ''
            end
            set -l name (string replace -r '^\s*alias ([A-Za-z0-9_.+-]+)=.*' '$1' -- $line)
            set -l cmt ''
            string match -qr '#' -- $line; and set cmt (string replace -r '^[^#]*#\s*' '' -- $line)
            printf "    %-22s %s\n" $name $cmt
        end
    end
    echo

    # ── Keybindings ───────────────────────────────────────────────────────────
    echo $hdr"KEYBINDINGS"$rst" (20-keybindings.fish)"
    printf "    %-22s %s\n" "!" "expand to the previous command"
    printf "    %-22s %s\n" '!$' "expand to the last argument of the previous command"
end
