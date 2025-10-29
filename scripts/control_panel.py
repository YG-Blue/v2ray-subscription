import os
import argparse

CONTROL_PANEL_FILE = os.path.join(os.path.dirname(__file__), '..', 'control_panel.txt')
CONTROL_PANEL_FILE = os.path.abspath(CONTROL_PANEL_FILE)

ACTIVE_MARK = '✅'
EMPTY_MARK = '  '


def load_control_panel():
    if not os.path.exists(CONTROL_PANEL_FILE):
        return []
    with open(CONTROL_PANEL_FILE, 'r', encoding='utf-8') as f:
        return [ln.rstrip() for ln in f if ln.strip()]


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
        print(f"{mark} {base}")


def activate(filename):
    if not filename:
        print('Please provide a filename to activate')
        return
    fname = filename.strip()
    entries = load_control_panel()
    names = [e.lstrip().lstrip(ACTIVE_MARK).strip() for e in entries]
    if fname not in names:
        names.append(fname)
    # rewrite with only fname active (active marked with leading tick)
    with open(CONTROL_PANEL_FILE, 'w', encoding='utf-8') as f:
        for n in names:
            if n == fname:
                f.write(f"{ACTIVE_MARK} {n}\n")
            else:
                f.write(f"{n}\n")
    print(f"Activated: {ACTIVE_MARK} {fname}")
    # Show current state
    show_panel()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control panel manager for v2ray subscription')
    sub = parser.add_subparsers(dest='cmd')
    sub.add_parser('show', help='Show control panel entries and active server')
    act = sub.add_parser('activate', help='Activate a server file listed in control_panel.txt (adds if missing)')
    act.add_argument('filename', help='Server filename to activate (e.g. servers.txt or servers1.txt)')

    args = parser.parse_args()
    if args.cmd == 'show':
        show_panel()
    elif args.cmd == 'activate':
        activate(args.filename)
    else:
        parser.print_help()
