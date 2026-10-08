with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('const [loading, setLoading] = useState(true);', 'const [loading, setLoading] = useState(true);\n  const router = useRouter();')

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
