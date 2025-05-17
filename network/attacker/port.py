import subprocess

def run_nmap_scan():
    target_ip = "172.28.0.3"
    nmap_command = ["nmap", "-sS", "-Pn", "-n", "-p-", target_ip]

    try:
        result = subprocess.run(nmap_command, capture_output=True, text=True, check=True)
        print("Nmap command output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during nmap execution:")
        print(e.stderr)

if __name__ == "__main__":
    run_nmap_scan()