# In this file, we define two endpoints: /installed_programs and /uninstall_programs.
# The installed_programs endpoint returns a list of installed programs. We use the psutil library to get a list of
# running processes, filter out any non-application processes, and return the list of installed programs as a JSON response.
# The /uninstall_programs endpoint receives a list of programs to uninstall as a JSON payload. It then iterates over
# the list of programs, executes the appropriate uninstall command, and returns a JSON response containing the results
# of each uninstall attempt.
# Please keep in mind that this example uses subprocess to execute uninstall commands, which can be
# potentially dangerous if not properly sanitized.

from flask import Flask, jsonify, request
import psutil
import win32api

app = Flask(__name__)


@app.route('/installed_programs', methods=['GET'])
def get_installed_programs():
    installed_programs = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Get the program name from the process executable path
            program_name = proc.name().lower()
            if program_name.endswith('.exe') and not program_name.startswith('system32'):
                installed_programs.append(program_name[:-4])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return jsonify(installed_programs=installed_programs)


@app.route('/uninstall_programs', methods=['POST'])
def uninstall_programs():
    programs_to_uninstall = request.json['programs_to_uninstall']
    uninstall_results = {}
    for program in programs_to_uninstall:
        # Confirm uninstallation with user
        if not confirm_uninstall(program):
            continue
        try:
            # Uninstall program using the Windows Registry
            win32api.RegDeleteKey(win32api.HKEY_LOCAL_MACHINE,
                                  f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{program}")
            uninstall_results[program] = 'Uninstalled successfully'
        except Exception as e:
            # Handle errors and provide detailed error messages
            uninstall_results[program] = f'Failed to uninstall: {str(e)}'
    # Refresh list of installed programs after uninstallation
    installed_programs = get_installed_programs().get_json()['installed_programs']
    return jsonify(uninstall_results=uninstall_results, installed_programs=installed_programs)


def confirm_uninstall(program_name):
    # Display a confirmation dialog asking the user to confirm uninstallation
    return messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall '{program_name}'?")


if __name__ == '__main__':
    app.run(debug=True)
