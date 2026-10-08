with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'gradioUrl' in line:
            print(f"Line {i}: {repr(line)}")
