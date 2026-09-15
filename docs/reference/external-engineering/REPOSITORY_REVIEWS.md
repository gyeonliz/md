# 외부 저장소 검토

검토일: 2026-09-15 (Asia/Seoul)

## 검토 원칙

- README의 주장은 프로젝트의 실제 코드·설정·로그보다 우선하지 않는다.
- 설치 명령, Hook, MCP, Agent/Skill 설정은 실행 가능한 공급망 입력으로 본다.
- 도입 전 정확한 Version 또는 Commit, License, 변경 파일, 실행 시점, 네트워크 접근, 제거 방법을 확인한다.
- 비슷한 도구를 중복 설치하지 않는다. 특히 Codex Hook·Skill·명령을 제공하는 도구는 한 번에 하나만 격리 시험한다.
- 외부 문구를 복사해 팀 규칙으로 삼지 않고 Drone 프로젝트에 맞게 재작성한다.

## 1. Ponytail

출처: [저장소](https://github.com/DietrichGebert/ponytail), [MIT License](https://github.com/DietrichGebert/ponytail/blob/main/LICENSE)

### 유용한 점

- 기능을 만들기 전에 정말 필요한지 확인하고, 이미 있는 코드와 플랫폼 기능을 먼저 찾도록 유도한다.
- 저장소를 먼저 읽고 실제 호출 흐름을 따라간 뒤 가장 작은 변경으로 해결한다.
- 최소 구현을 이유로 검증, 오류 처리, 보안, 접근성을 빼지 않는 경계를 둔다.

### Drone 적용

1. 요구가 아직 유효한지 확인한다.
2. `Source/Drone`, `/Game/Drone`의 기존 계약과 자산을 재사용한다.
3. Unreal Engine 기본 API와 Component/Data Asset 체계를 우선한다.
4. 이미 프로젝트에 있는 의존성을 확인한다.
5. 그래도 부족할 때만 새 Plugin/Library를 검토한다.
6. TestMap에서 동작하는 가장 작은 Vertical Slice를 만들고 회귀한다.

### 보류 사유

Codex Plugin과 Lifecycle Hook은 작업 방식 전체에 영향을 줄 수 있다. 현재 ECC와 역할이 겹치며 Drone에는 이미 고유 작업보드·검증 규칙이 있으므로 설치 효과가 확인되기 전에는 원칙만 사용한다.

## 2. Everything Claude Code(ECC)

출처: [저장소](https://github.com/affaan-m/ECC), [MIT License](https://github.com/affaan-m/ECC/blob/main/LICENSE)

### 유용한 점

- 계획, 테스트, 구현, 검토, 검증, 기억/문서화, 개선을 하나의 반복 Loop로 다룬다.
- Build 수정, 코드 검토, 보안 확인, Context 관리, 문서 갱신처럼 대형 프로젝트에서 반복되는 작업을 분리한다.
- Codex용 Native Plugin 경로와 범용 설치 경로를 구분한다.

### Drone 적용

- 모든 구현 카드는 `계획 → 실패/기준 테스트 → 최소 구현 → 자체 검토 → Build/자동화/화면 검증 → MD 기록` 순서를 따른다.
- Drone에 필요한 기능만 골라 사용한다. 방대한 Agent/Skill 전체를 프로젝트 기본값으로 삼지 않는다.
- 실제 맵 소유권, 대형 LFS 자산, Editor 실행 상태를 검토 단계에 포함한다.

### 보류 사유

ECC는 많은 Skill, Hook, Rule을 제공한다. Native Plugin, 범용 Installer, 수동 복사를 겹쳐 쓰면 중복 Hook과 충돌 가능성이 있다. 도입한다면 Dry Run 결과를 먼저 검토하고 설치 경로는 하나만 선택한다.

## 3. Archify

출처: [저장소](https://github.com/tt-a1i/archify), [MIT License](https://github.com/tt-a1i/archify/blob/main/LICENSE)

### 유용한 점

- Architecture, Workflow, Sequence, Data Flow, Lifecycle을 형식화된 중간 데이터로 만든 뒤 HTML/SVG 등으로 재현한다.
- 변경 전·변경점·변경 후를 비교하고 산출물이 실제 근거와 일치하는지 검증하는 방식이 유용하다.
- 자가 포함 산출물은 팀원에게 공유하기 쉽다.

### Drone 적용

- 우선 Markdown과 Mermaid로 `Front-end → Mission → Drone 선택 → 목표 → 결과` 흐름, Tutorial Gate/Lap Lifecycle, TestMap→Training 인계 경계를 기록한다.
- 상호작용 가능한 그림이 실제로 필요할 때만 Archify를 격리 설치한다.
- Diagram은 코드·Data Asset·테스트 이름과 연결하고, 추정 흐름은 명시적으로 `미구현`으로 표시한다.

### 보류 사유

현재 공유 요구는 Markdown으로 충족된다. 새 Node Tool과 Update Check를 바로 추가할 실익이 아직 검증되지 않았다.

## 4. fmt

출처: [저장소](https://github.com/fmtlib/fmt), [MIT License](https://github.com/fmtlib/fmt/blob/master/LICENSE)

### 유용한 점

- Type-safe C++ Formatting, Compile-time Format 확인, 사용자 정의 Type 지원을 제공한다.
- Unreal 밖에서 동작하는 독립 C++ Tool이나 Library에는 좋은 후보가 될 수 있다.

### Drone 코드 감사 결과와 결정

- 현재 `Source/Drone`에는 `fmt::`, `<fmt/...>` 사용이 없다.
- Runtime UI와 사용자 표시 문자열은 Unreal Localization을 고려한 `FText`가 기준이다.
- 로그와 내부 문자열은 Unreal의 `UE_LOG`/`UE_LOGFMT`, `FString` 체계로 충분하다.
- 따라서 `Drone.Build.cs`에 fmt 의존성을 추가하지 않는다. Standalone 비-Unreal C++ Tool이 생기고 측정 가능한 필요가 있을 때만 별도 검토한다.

## 5. Matt Pocock Skills

출처: [저장소](https://github.com/mattpocock/skills), [MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE)

### 유용한 점

- 작은 Skill을 조합하고 프로젝트 자체 Workflow를 대체하지 않는 접근이다.
- 문서를 이용해 요구를 충분히 질문하고, 팀 공유 언어를 만들며, TDD와 짧은 Feedback Loop를 유지한다.
- Bug를 수정하기 전에 증상, 재현, 원인, 수정, 회귀를 구분한다.

### Drone 적용

- 기능 이름과 상태 이름을 `DRONE_GLOSSARY.md` 또는 해당 설계 문서에 먼저 통일한다.
- 중요한 선택은 짧은 ADR 형식으로 `맥락 / 결정 / 이유 / 영향 / 되돌리기`를 기록한다.
- Crash나 자동화 실패는 원인 규명 전 임시 우회로 Done 처리하지 않는다.
- ECC와 겹치는 Skill은 중복 설치하지 않고 프로젝트 규칙으로만 우선 적용한다.

## 종합 결론

외부 저장소 다섯 개에서 얻은 가장 큰 이점은 도구 설치가 아니라 작업 기준 정리다. 현재 Drone은 Unreal, LFS 대형 자산, 팀원 소유 Map, 자동화와 수동 검증이 얽혀 있으므로 새로운 실행 Hook보다 작고 추적 가능한 규칙이 우선이다.

