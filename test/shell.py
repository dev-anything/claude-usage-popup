import subprocess

# capture_output=True를 사용하면 stdout과 stderr를 모두 객체에 담습니다.
result = subprocess.run("claude update", shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")

print(f"Output ====> {result.stdout}")

# 만약 업데이트 중 에러나 안내 메시지가 stderr로 출력될 경우 확인
if result.stderr:
    print(f"Error/Message ====> {result.stderr}")


print(f"[PARSING] ==> {result.stdout[0:10]}")