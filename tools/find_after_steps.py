import json

with open(r'C:\Users\chisi\.gemini\antigravity\brain\9eb0d502-165f-4710-8622-365fac624da7\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index', 0)
        if 1262 <= idx <= 1500:
            tcs = data.get('tool_calls', [])
            for tc in tcs:
                if tc.get('name') == 'run_command':
                    cmd = tc.get('args', {}).get('CommandLine', '')
                    if any(k in cmd for k in ['.py', 'blender']):
                        print(f"Step {idx}: {cmd}")

