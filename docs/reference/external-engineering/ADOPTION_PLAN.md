# 외부 도구 도입 계획

## 현재 상태

- Ponytail: 미설치
- ECC: 미설치
- Archify: 미설치
- fmt: Unreal Module 미추가
- Matt Pocock Skills: 개인 Codex 환경에 `diagnosing-bugs`, `tdd`만 설치

이번 검토에서는 문서 원칙과 위의 최소 Skill 2개만 반영했다. Hook, Plugin, MCP, Node Package, `Drone.Build.cs`는 변경하지 않았다. Skill은 `C:\Users\Metacon_41\.codex\skills` 아래 개인 도구이며 Unreal 저장소와 팀원 PC의 의존성이 아니다.

사용자는 실제 필요가 확인되면 설치 진행을 허용했다. 이는 아래 도입 Gate를 생략한다는 뜻이 아니며, 현재 TestMap 단계에는 필수 설치 대상이 없다고 판정했다.

## 도입 Gate

외부 도구는 다음 조건을 모두 만족할 때만 시험한다.

1. 해결하려는 반복 문제가 구체적으로 기록돼 있다.
2. 현재 Playbook이나 기존 도구로 해결하기 어렵다.
3. 정확한 Version/Commit과 License를 고정했다.
4. 설치 명령과 변경 파일을 Dry Run 또는 격리 폴더에서 확인했다.
5. Hook 실행 시점, Shell 명령, Network 접근, 수집 데이터와 저장 위치를 검토했다.
6. 기존 Codex Plugin/Skill/Hook과 중복이 없다.
7. 제거·Rollback 절차가 있다.
8. 팀 공유가 필요한 설정과 개인 설정을 분리했다.

## 후보별 시험 순서

### A. 작업 자동화 후보: ECC 또는 Ponytail 중 하나

- 동시에 설치하지 않는다.
- 첫 시험은 Drone 저장소가 아닌 임시/격리 Project에서 한다.
- ECC는 제공되는 Guided Dry Run으로 변경 파일을 먼저 확인한다.
- Ponytail은 Lifecycle Hook 원문과 실행 조건을 먼저 검토한다.
- 합격 기준은 문서/검증 누락 감소, 중복 명령 없음, 작업 속도 개선, 손쉬운 제거다.

### B. Diagram 후보: Archify

- 먼저 기존 Markdown으로 Mission Lifecycle Diagram 하나를 작성한다.
- 상호작용·Animation·다중 Export 요구가 실제로 생기면 Archify를 시험한다.
- 자동 Update Check가 팀 정책에 맞지 않으면 비활성화한다.
- 생성물만 공유할지 Tool 설정도 공유할지 분리한다.

### C. C++ Formatting 후보: fmt

- Unreal Runtime에는 도입하지 않는다.
- 향후 Unreal 밖의 독립 CLI/Converter가 생길 때 표준 Library와 성능/가독성을 비교한다.
- Unreal Module에 넣어야 한다면 ThirdParty Module, License, Target별 Link, Package 크기, 팀 Build를 먼저 검증한다.

### D. Skill: Matt Pocock Skills 최소 도입

- 공유 용어·ADR 원칙은 Playbook으로 유지한다.
- 현재 반복되는 Unreal 자동화 실패에 직접 필요한 `diagnosing-bugs`, `tdd`만 설치했다.
- 설치한 Skill은 다음 Codex Turn부터 사용할 수 있으며 Project Build/Runtime에는 들어가지 않는다.
- 전체 묶음과 `setup-matt-pocock-skills`는 기존 `CONTEXT/WORKBOARD` 체계와 중복되어 설치하지 않는다.

## 다음 액션

`AI-TOOL-REVIEW-01`은 TestMap Vertical Slice가 안정된 뒤 수행한다. 그 전에는 새로운 Agent/Hook 체계가 현재 맵 분리와 Unreal 검증을 방해하지 않도록 보류한다.
