#
# 10-interactive.fish — interactive-shell settings, greeting, prompt/colour pointers
#

# set -gx TERM xterm-256color   # off by default — let the terminal set its own TERM (kitty/alacritty/foot need theirs); uncomment to force
set -g theme_nerd_fonts yes   # tell prompts/themes that Nerd Font glyphs are available

# Keep full (unshortened) directory names in the prompt.
set -g fish_prompt_pwd_dir_length 0

# Colours and key bindings for fzf (fuzzy finder).
set -gx FZF_DEFAULT_OPTS "--color=16,header:13,info:5,pointer:3,marker:9,spinner:1,prompt:5,fg:7,hl:14,fg+:3,hl+:9 --inline-info --tiebreak=end,length --bind=shift-tab:toggle-down,tab:toggle-up"

# No greeting on launch — keep the terminal quiet (this also suppresses fish's
# default welcome). To show a fastfetch system summary instead, uncomment below
# or add it to your own ~/.config/fish/config.fish.
set -g fish_greeting
# if type -q fastfetch
#     function fish_greeting
#         fastfetch
#     end
# end

# Prompt and colours are intentionally NOT set in this payload — theming lives in
# one place, the Fish Tweak Tool / fish's own config:
#   • prompt  -> fish_config prompt choose <name>; and fish_config prompt save
#   • colours -> fish_config theme  choose <name>; and fish_config theme  save
