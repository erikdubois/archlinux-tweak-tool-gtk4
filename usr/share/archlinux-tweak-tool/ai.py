import functions as fn
from gi.repository import GLib


def on_click_ai_ollama(self, _widget):
    try:
        if fn.path.exists("/usr/bin/ollama"):
            fn.log_subsection("Removing ollama...")
            process = fn.launch_pacman_remove_in_terminal("ollama")
            def wait_removal():
                process.wait()
                GLib.idle_add(self.lbl_ai_ollama.set_markup, "Ollama - Local LLM runner")
                GLib.idle_add(self.btn_ai_ollama.set_label, "Install")
                GLib.idle_add(fn.show_in_app_notification, self, "ollama removal complete")
            fn.threading.Thread(target=wait_removal, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "ollama removal started")
        else:
            has_nvidia = fn.path.exists("/dev/nvidia0")
            pkgs = "ollama ollama-cuda" if has_nvidia else "ollama"
            fn.log_subsection(f"Installing {pkgs}...")
            fn.debug_print(f"NVIDIA GPU detected: {has_nvidia}")
            process = fn.launch_pacman_install_in_terminal(pkgs)
            def wait_install():
                try:
                    stdout_data, stderr_data = process.communicate()
                    stdout_str = stdout_data.decode() if stdout_data else ""
                    stderr_str = stderr_data.decode() if stderr_data else ""
                    error_output = stderr_str + stdout_str
                    if fn.path.exists("/usr/bin/ollama"):
                        fn.log_success("ollama installed successfully")
                        GLib.idle_add(self.lbl_ai_ollama.set_markup, "Ollama - Local LLM runner <b>installed</b>")
                        GLib.idle_add(self.btn_ai_ollama.set_label, "Remove")
                        GLib.idle_add(fn.show_in_app_notification, self, "ollama installation complete")
                    else:
                        fn.log_warn("ollama binary NOT found, installation may have failed")
                        fn.check_missing_repo_error(self, error_output, "ollama")
                except Exception as e:
                    fn.log_error(f"Error during ollama installation: {e}")
            fn.threading.Thread(target=wait_install, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "ollama installation started")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_ai_webui(self, _widget):
    try:
        if fn.path.exists("/usr/bin/open-webui"):
            fn.log_subsection("Removing open-webui...")
            process = fn.launch_pacman_remove_in_terminal("open-webui")
            def wait_removal():
                process.wait()
                GLib.idle_add(self.lbl_ai_webui.set_markup, "Open WebUI - Browser UI for Ollama")
                GLib.idle_add(self.btn_ai_webui.set_label, "Install")
                GLib.idle_add(fn.show_in_app_notification, self, "open-webui removal complete")
            fn.threading.Thread(target=wait_removal, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "open-webui removal started")
        else:
            aur_helper = fn.get_aur_helper()
            if aur_helper is None:
                GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found. Install yay or paru first.")
                return
            fn.log_subsection("Installing open-webui...")
            process = fn.launch_aur_install_in_terminal(aur_helper, "open-webui")
            def wait_install():
                try:
                    stdout_data, stderr_data = process.communicate()
                    stdout_str = stdout_data.decode() if stdout_data else ""
                    stderr_str = stderr_data.decode() if stderr_data else ""
                    error_output = stderr_str + stdout_str
                    if fn.path.exists("/usr/bin/open-webui"):
                        fn.log_success("open-webui installed successfully")
                        GLib.idle_add(self.lbl_ai_webui.set_markup, "Open WebUI - Browser UI for Ollama <b>installed</b>")
                        GLib.idle_add(self.btn_ai_webui.set_label, "Remove")
                        GLib.idle_add(fn.show_in_app_notification, self, "open-webui installation complete")
                    else:
                        fn.log_warn("open-webui binary NOT found, installation may have failed")
                        fn.check_missing_repo_error(self, error_output, "open-webui")
                except Exception as e:
                    fn.log_error(f"Error during open-webui installation: {e}")
            fn.threading.Thread(target=wait_install, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "open-webui installation started")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_ai_claude(self, _widget):
    try:
        if fn.path.exists("/usr/bin/claude"):
            fn.log_subsection("Removing claude-code...")
            process = fn.launch_pacman_remove_in_terminal("claude-code")
            def wait_removal():
                process.wait()
                GLib.idle_add(self.lbl_ai_claude.set_markup, "Claude Code - Anthropic CLI")
                GLib.idle_add(self.btn_ai_claude.set_label, "Install")
                GLib.idle_add(fn.show_in_app_notification, self, "claude-code removal complete")
            fn.threading.Thread(target=wait_removal, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "claude-code removal started")
        else:
            aur_helper = fn.get_aur_helper()
            if aur_helper is None:
                GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found. Install yay or paru first.")
                return
            fn.log_subsection("Installing claude-code...")
            process = fn.launch_aur_install_in_terminal(aur_helper, "claude-code")
            def wait_install():
                process.wait()
                if fn.path.exists("/usr/bin/claude"):
                    fn.log_success("claude-code installed successfully")
                    GLib.idle_add(self.lbl_ai_claude.set_markup, "Claude Code - Anthropic CLI <b>installed</b>")
                    GLib.idle_add(self.btn_ai_claude.set_label, "Remove")
                    GLib.idle_add(fn.show_in_app_notification, self, "claude-code installation complete")
                else:
                    fn.log_warn("claude-code binary NOT found, installation may have failed")
            fn.threading.Thread(target=wait_install, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "claude-code installation started")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_ai_aider(self, _widget):
    try:
        aider_path = f"/home/{fn.sudo_username}/.local/bin/aider"
        if fn.path.exists("/usr/bin/aider") or fn.path.exists(aider_path):
            fn.log_subsection("Removing aider...")
            aur_helper = fn.get_aur_helper()
            script = f"rm -f {aider_path}; "
            if aur_helper:
                script += f"sudo -u {fn.sudo_username} {aur_helper} -Rs --noconfirm aider-install; "
            script += "echo ''; echo '=== Removal complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
            def wait_removal():
                process.wait()
                GLib.idle_add(self.lbl_ai_aider.set_markup, "Aider - AI pair programming")
                GLib.idle_add(self.btn_ai_aider.set_label, "Install")
                GLib.idle_add(fn.show_in_app_notification, self, "aider removal complete")
            fn.threading.Thread(target=wait_removal, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "aider removal started")
        else:
            aur_helper = fn.get_aur_helper()
            if aur_helper is None:
                GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found. Install yay or paru first.")
                return
            fn.log_subsection("Installing aider...")
            process = fn.launch_aur_install_in_terminal(aur_helper, "aider-install")
            def wait_install():
                try:
                    import time
                    process.wait()
                    time.sleep(1)
                    fn.subprocess.call(f"sudo -u {fn.sudo_username} aider-install", shell=True, stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
                    if fn.path.exists("/usr/bin/aider") or fn.path.exists(aider_path):
                        fn.log_success("aider installed successfully")
                        GLib.idle_add(self.lbl_ai_aider.set_markup, "Aider - AI pair programming <b>installed</b>")
                        GLib.idle_add(self.btn_ai_aider.set_label, "Remove")
                        GLib.idle_add(fn.show_in_app_notification, self, "aider installation complete")
                    else:
                        fn.log_warn(f"Aider binary NOT found. Checked: /usr/bin/aider and {aider_path}")
                except Exception as e:
                    fn.log_error(f"Error during aider installation: {e}")
            fn.threading.Thread(target=wait_install, daemon=True).start()
            GLib.idle_add(fn.show_in_app_notification, self, "aider installation started")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_ai_codex(self, _widget):
    try:
        codex_paths = ["/usr/bin/codex", "/usr/local/bin/codex", f"/home/{fn.sudo_username}/.local/bin/codex", f"/home/{fn.sudo_username}/.npm-global/bin/codex"]
        codex_installed = any(fn.path.exists(p) for p in codex_paths)

        if codex_installed:
            fn.log_subsection("Removing codex...")
            process = fn.launch_npm_remove_in_terminal("@openai/codex")
            if process:
                def wait_removal():
                    try:
                        import time
                        process.wait()
                        time.sleep(1)
                        GLib.idle_add(self.lbl_ai_codex.set_markup, "OpenAI Codex CLI")
                        GLib.idle_add(self.btn_ai_codex.set_label, "Install")
                        GLib.idle_add(fn.show_in_app_notification, self, "Codex removal complete")
                    except Exception as e:
                        fn.log_error(f"Error during codex removal: {e}")
                fn.threading.Thread(target=wait_removal, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "Codex removal started")
            else:
                GLib.idle_add(fn.show_in_app_notification, self, "Codex removal failed")
        else:
            fn.log_subsection("Installing codex...")
            process = fn.launch_npm_install_in_terminal("@openai/codex")
            if process:
                def wait_install():
                    try:
                        import time
                        process.wait()
                        time.sleep(1)
                        if any(fn.path.exists(p) for p in codex_paths):
                            fn.log_success("codex installed successfully")
                            GLib.idle_add(self.lbl_ai_codex.set_markup, "OpenAI Codex CLI <b>installed</b>")
                            GLib.idle_add(self.btn_ai_codex.set_label, "Remove")
                            GLib.idle_add(fn.show_in_app_notification, self, "Codex installation complete")
                        else:
                            fn.log_warn(f"Codex binary NOT found. Checked: {codex_paths}")
                    except Exception as e:
                        fn.log_error(f"Error during codex installation: {e}")
                fn.threading.Thread(target=wait_install, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "Codex installation started")
            else:
                GLib.idle_add(fn.show_in_app_notification, self, "Codex installation failed")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_ai_gemini(self, _widget):
    try:
        gemini_paths = ["/usr/bin/gemini", "/usr/local/bin/gemini", f"/home/{fn.sudo_username}/.local/bin/gemini", f"/home/{fn.sudo_username}/.npm-global/bin/gemini"]
        gemini_installed = any(fn.path.exists(p) for p in gemini_paths)

        if gemini_installed:
            fn.log_subsection("Removing gemini...")
            process = fn.launch_npm_remove_in_terminal("@google/gemini-cli")
            if process:
                def wait_removal():
                    try:
                        import time
                        process.wait()
                        time.sleep(1)
                        GLib.idle_add(self.lbl_ai_gemini.set_markup, "Google Gemini CLI")
                        GLib.idle_add(self.btn_ai_gemini.set_label, "Install")
                        GLib.idle_add(fn.show_in_app_notification, self, "Gemini removal complete")
                    except Exception as e:
                        fn.log_error(f"Error during gemini removal: {e}")
                fn.threading.Thread(target=wait_removal, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "Gemini removal started")
            else:
                GLib.idle_add(fn.show_in_app_notification, self, "Gemini removal failed")
        else:
            fn.log_subsection("Installing gemini...")
            process = fn.launch_npm_install_in_terminal("@google/gemini-cli")
            if process:
                def wait_install():
                    try:
                        import time
                        process.wait()
                        time.sleep(1)
                        if any(fn.path.exists(p) for p in gemini_paths):
                            fn.log_success("gemini installed successfully")
                            GLib.idle_add(self.lbl_ai_gemini.set_markup, "Google Gemini CLI <b>installed</b>")
                            GLib.idle_add(self.btn_ai_gemini.set_label, "Remove")
                            GLib.idle_add(fn.show_in_app_notification, self, "Gemini installation complete")
                        else:
                            fn.log_warn(f"Gemini binary NOT found. Checked: {gemini_paths}")
                    except Exception as e:
                        fn.log_error(f"Error during gemini installation: {e}")
                fn.threading.Thread(target=wait_install, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "Gemini installation started")
            else:
                GLib.idle_add(fn.show_in_app_notification, self, "Gemini installation failed")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def open_url_in_browser(self, url):
    try:
        fn.subprocess.Popen(f"sudo -u {fn.sudo_username} DISPLAY=:0 xdg-open '{url}'", shell=True, stdout=fn.subprocess.DEVNULL, stderr=fn.subprocess.DEVNULL)
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_ai_ollama_link(self, _widget):
    open_url_in_browser(self, "https://ollama.com/")


def on_click_ai_webui_link(self, _widget):
    open_url_in_browser(self, "https://openwebui.com/")


def on_click_ai_claude_link(self, _widget):
    open_url_in_browser(self, "https://code.claude.com/docs/en/cli-reference")


def on_click_ai_aider_link(self, _widget):
    open_url_in_browser(self, "https://aider.chat/")


def on_click_ai_gemini_link(self, _widget):
    open_url_in_browser(self, "https://geminicli.com/")


def on_click_ai_codex_link(self, _widget):
    open_url_in_browser(self, "https://developers.openai.com/codex/cli")


def on_click_ai_chatgpt(self, _widget):
    open_url_in_browser(self, "https://chatgpt.com")


def on_click_ai_chatgpt_link(self, _widget):
    open_url_in_browser(self, "https://academy.openai.com/")


def on_click_ai_claude_web_link(self, _widget):
    open_url_in_browser(self, "https://claude.com/resources/tutorials?open_in_browser=1")


def on_click_ai_gemini_web_link(self, _widget):
    open_url_in_browser(self, "https://gemini.google.com/")


def on_click_ai_perplexity_link(self, _widget):
    open_url_in_browser(self, "https://www.perplexity.ai/hub/getting-started")


def on_click_ai_claude_web(self, _widget):
    open_url_in_browser(self, "https://claude.ai")


def on_click_ai_gemini_web(self, _widget):
    open_url_in_browser(self, "https://gemini.google.com")


def on_click_ai_perplexity(self, _widget):
    open_url_in_browser(self, "https://perplexity.ai")


def on_click_ai_dalle_link(self, _widget):
    open_url_in_browser(self, "https://openai.com/index/dall-e-3/")


def on_click_ai_dalle(self, _widget):
    open_url_in_browser(self, "https://openai.com/dall-e-3")


def on_click_ai_midjourney_link(self, _widget):
    open_url_in_browser(self, "https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide")


def on_click_ai_midjourney(self, _widget):
    open_url_in_browser(self, "https://www.midjourney.com")


def on_click_ai_leonardo_link(self, _widget):
    open_url_in_browser(self, "https://leonardo.ai/learn/")


def on_click_ai_leonardo(self, _widget):
    open_url_in_browser(self, "https://leonardo.ai")


def on_click_ai_firefly_link(self, _widget):
    open_url_in_browser(self, "https://www.adobe.com/learn/firefly")


def on_click_ai_firefly(self, _widget):
    open_url_in_browser(self, "https://www.adobe.com/products/firefly")
