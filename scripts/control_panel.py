import os
import argparse
import re

CONTROL_PANEL_FILE = os.path.join(os.path.dirname(__file__), '..', 'control_panel.txt')
CONTROL_PANEL_FILE = os.path.abspath(CONTROL_PANEL_FILE)

ACTIVE_MARK = '✅'
EMPTY_MARK = '  '
ON_FLAG = '---on'


def load_control_panel():
    if not os.path.exists(CONTROL_PANEL_FILE):
        return []
    with open(CONTROL_PANEL_FILE, 'r', encoding='utf-8') as f:
        return [ln.rstrip() for ln in f if ln.strip()]


def get_active_server():
    entries = load_control_panel()
    for entry in entries:
        stripped = entry.lstrip()
        if stripped.startswith(ACTIVE_MARK):
            return stripped[len(ACTIVE_MARK):].lstrip()
    return None


def show_panel():
    entries = load_control_panel()
    if not entries:
        print('No entries in control_panel.txt')
        return
    for e in entries:
        stripped = e.lstrip()
        if stripped.startswith(ACTIVE_MARK):
            base = stripped[len(ACTIVE_MARK):].lstrip()
            mark = ACTIVE_MARK
        else:
            base = stripped
            mark = EMPTY_MARK
        
        # Check if this entry has the ON flag
        has_on_flag = ON_FLAG in base
        if has_on_flag:
            base = base.replace(ON_FLAG, '').strip()
            print(f"{mark} {base} {ON_FLAG}")
        else:
            print(f"{mark} {base}")


def activate(filename, switch_on=False):
    if not filename:
        print('Please provide a filename to activate')
        return
    fname = filename.strip()
    entries = load_control_panel()
    
    # Extract names and flags
    processed_entries = []
    for e in entries:
        stripped = e.lstrip().lstrip(ACTIVE_MARK).strip()
        # Check if this entry has the ON flag and preserve it
        if ON_FLAG in stripped:
            base_name = stripped.replace(ON_FLAG, '').strip()
            processed_entries.append((base_name, True))
        else:
            processed_entries.append((stripped, False))
    
    # Get list of base names
    names = [entry[0] for entry in processed_entries]
    
    # Add the new filename if it doesn't exist
    if fname not in names:
        names.append(fname)
        processed_entries.append((fname, False))
    
    # If switch_on is True, toggle the ON flag for the activated file
    # and remove it from all others
    if switch_on:
        processed_entries = [(name, True if name == fname else False) for name, _ in processed_entries]
    
    # Rewrite with only fname active (active marked with leading tick)
    with open(CONTROL_PANEL_FILE, 'w', encoding='utf-8') as f:
        for name, has_on in processed_entries:
            if name == fname:
                if has_on:
                    f.write(f"{ACTIVE_MARK} {name} {ON_FLAG}\n")
                else:
                    f.write(f"{ACTIVE_MARK} {name}\n")
            else:
                if has_on:
                    f.write(f"{name} {ON_FLAG}\n")
                else:
                    f.write(f"{name}\n")
    
    status = f"Activated: {ACTIVE_MARK} {fname}"
    if switch_on:
        status += f" with {ON_FLAG} flag"
    print(status)
    
    # Show current state
    show_panel()


if __name__ == '__main__':
    # This CLI is intended to be executed inside GitHub Actions only.
    # It will exit when run locally unless RUN_LOCALLY=1 is set for debugging.
    gh_actions = os.getenv('GITHUB_ACTIONS', '').lower()
    run_local = os.getenv('RUN_LOCALLY', '') == '1'
    if gh_actions != 'true' and not run_local:
        print("This control-panel tool is intended to run inside GitHub Actions only.\n" \
              "To enable local runs for debugging set RUN_LOCALLY=1 in your environment.")
        raise SystemExit(1)

    parser = argparse.ArgumentParser(description='Control panel manager for v2ray subscription')
    sub = parser.add_subparsers(dest='cmd')
    sub.add_parser('show', help='Show control panel entries and active server')
    
    act = sub.add_parser('activate', help='Activate a server file listed in control_panel.txt (adds if missing)')
    act.add_argument('filename', help='Server filename to activate (e.g. servers.txt or servers1.txt)')
    act.add_argument('--on', action='store_true', help='Add the ---on flag to the activated server')
    
    switch = sub.add_parser('switch', help='Switch to a server with the ---on flag')
    switch.add_argument('filename', help='Server filename to switch to (e.g. servers.txt or servers1.txt)')

    args = parser.parse_args()
    if args.cmd == 'show':
        show_panel()
    elif args.cmd == 'activate':
        activate(args.filename, args.on)
    elif args.cmd == 'switch':
        activate(args.filename, True)
    else:
        parser.print_help()
