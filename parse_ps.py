import subprocess
from collections import Counter
from datetime import datetime


def parse(out: str) -> list[dict]:
    header, *lines = out.splitlines()
    procs = []
    for line in lines:
        user, pid, cpu, mem, *_, command = line.split(maxsplit=10)
        procs.append({"user": user, "pid": int(pid), "cpu": float(cpu),
                      "mem": float(mem), "command": command})
    return procs

def get_process_memory(process: dict) -> float:
    return process["mem"]

def get_process_cpu(process: dict) -> float:
    return process["cpu"]

def create_report(proc: list[dict]) -> str:
    users = sorted({i["user"] for i in proc})
    user_counts = Counter(i["user"] for i in proc)

    total_mem = sum(i["mem"] for i in proc)
    total_cpu = sum(i["cpu"] for i in proc)

    top_mem = max(procs, key=get_process_memory)
    top_cpu = max(procs, key=get_process_cpu)

    print_report = [
        "Отчёт о состоянии системы:",
        f"Пользователи системы: {', '.join(repr(user) for user in users)}",
        f"Процессов запущено: {len(procs)}",
        "Пользовательских процессов:",
    ]

    for user in users:
        print_report.append(f"{user}: {user_counts[user]}")

    print_report.extend([f"Всего памяти используется: {total_mem:.1f}%",
        f"Всего CPU используется: {total_cpu:.1f}%",
        f"Больше всего памяти использует: {top_mem['command'][:20]}",
        f"Больше всего CPU использует: {top_cpu['command'][:20]}",
    ])

    return "\n".join(print_report)


def save_to_file(report: str) -> str:
    filename = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report + "\n")
    return filename


out = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True).stdout
procs = parse(out)

report = create_report(procs)
print(report)

filename = save_to_file(report)
print(f"Отчёт сохранён в файл: {filename}")