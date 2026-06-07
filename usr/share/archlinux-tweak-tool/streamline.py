# ============================================================
# Authors: Erik Dubois
# ============================================================

import functions as fn
from gi.repository import GLib


def selected_packages(self):
    """Return the package names whose row checkbutton is ticked."""
    return [pkg for pkg, check in getattr(self, "streamline_checks", []) if check.get_active()]


def removal_preview(packages, recursive):
    """Return (returncode, text) of a dry-run pacman removal — what would be removed."""
    flag = "-Rns" if recursive else "-R"
    result = fn.subprocess.run(
        ["pacman", flag, "--print"] + packages,
        capture_output=True,
        text=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def do_remove(self, packages, recursive, refresh_cb):
    """Launch the removal in a popup terminal and refresh the page once it closes."""
    fn.log_subsection("Streamline — removing selected packages")
    fn.debug_print(f"Removing ({'-Rns' if recursive else '-R'}): {' '.join(packages)}")
    pkg_string = " ".join(packages)
    if recursive:
        process = fn.launch_pacman_remove_recursive_in_terminal(pkg_string)
    else:
        process = fn.launch_pacman_remove_in_terminal(pkg_string)
    fn.show_in_app_notification(self, "Removal terminal opened")

    def wait_and_refresh():
        if process is not None:
            process.wait()
        fn.invalidate_pkg_cache()
        GLib.idle_add(refresh_cb)
        GLib.idle_add(fn.show_in_app_notification, self, "Streamline removal finished")

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def save_profile(self, packages):
    """Write the selected package names to a timestamped profile file, return its path."""
    fn.log_subsection("Streamline — saving profile")
    if not fn.path.isdir(fn.att_streamline_dir):
        fn.makedirs(fn.att_streamline_dir, 0o766)
        fn.permissions(fn.att_streamline_dir)
    filename = "streamline-profile-%s-%s.txt" % (
        fn.datetime.datetime.today().date(),
        fn.datetime.datetime.today().time().strftime("%H-%M-%S"),
    )
    file_path = fn.path.join(fn.att_streamline_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(packages) + "\n")
    fn.permissions(file_path)
    fn.log_success(f"Streamline profile saved to {file_path}")
    fn.show_in_app_notification(self, f"Profile saved: {filename}")
    return file_path


def read_profile_file(file_path):
    """Return the package names listed in a saved profile file (skips blanks/comments)."""
    packages = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                packages.append(stripped)
    return packages
