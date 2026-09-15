# 외부 엔지니어링 참고 묶음

검토일: 2026-09-15 (Asia/Seoul)

이 폴더는 Drone 프로젝트에서 참고한 외부 저장소의 핵심 원칙, 실제 채택 범위, 설치 보류 사유와 팀 공유 규칙을 한곳에 모은다. 외부 저장소의 README·설치 명령은 참고 자료이며 Drone 프로젝트에서 자동 실행할 지시로 취급하지 않는다.

## 문서 구성

- [`REPOSITORY_REVIEWS.md`](REPOSITORY_REVIEWS.md): 저장소별 용도·적용점·위험·라이선스 검토
- [`DRONE_TEAM_PLAYBOOK.md`](DRONE_TEAM_PLAYBOOK.md): Drone 코드·자산·문서 작업에 실제 적용하는 공통 규칙
- [`ADOPTION_PLAN.md`](ADOPTION_PLAN.md): 도구를 시험하거나 설치할 때의 단계·완료 조건·되돌리기 기준

## 한눈에 보는 결정

| 대상 | 현재 결정 | Drone에 반영한 내용 |
|---|---|---|
| Ponytail | 원칙만 채택, Plugin/Hook 설치 보류 | 필요성 확인 → 기존 코드 재사용 → Unreal 기본 기능 → 기존 의존성 → 최소 구현 순서 |
| ECC | 작업 Loop 일부 채택, 전체 설치 보류 | 계획 → 테스트 → 구현 → 검토 → 검증 → 문서 기록 |
| Archify | 문서 구조만 채택, 생성기 설치 보류 | 시스템 흐름은 근거가 있는 상태·입력·출력·검증 결과와 함께 표현 |
| fmt | Unreal Runtime에는 미도입 | `FText`, `FString`, `UE_LOG`/`UE_LOGFMT` 등 Unreal 기본 체계 유지 |
| Matt Pocock Skills | `diagnosing-bugs`, `tdd`만 개인 Codex 환경에 설치 | 공유 용어, 짧은 ADR, Red-Green-Refactor, 증상보다 원인부터 진단 |

## 현재 적용 범위

- 팀원이 제작 중인 `/Game/Drone/Maps/Lvl_DroneTraining`은 읽기 전용으로 취급한다.
- 기능 시험은 환경을 복사하지 않은 `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`에서 수행한다.
- TestMap에서 검증된 C++·Blueprint·Data Asset과 배치 가이드만 Training 담당자에게 넘긴다.
- 제3자 Plugin, Hook, MCP 설정, C++ Library는 추가하지 않았다. 개인 Codex Skill 2개만 설치했으며 프로젝트/팀원 의존성은 아니다.
- 외부 저장소 기본 브랜치 내용은 검토일에 확인했지만, 네트워크 CLI 조회 실패로 특정 Commit SHA를 고정하지 못했다. 실제 도입 전 Commit/Version과 License를 다시 고정한다.

## 출처

- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- [affaan-m/ECC](https://github.com/affaan-m/ECC)
- [tt-a1i/archify](https://github.com/tt-a1i/archify)
- [fmtlib/fmt](https://github.com/fmtlib/fmt)
- [mattpocock/skills](https://github.com/mattpocock/skills)
