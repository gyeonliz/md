# Drone 팀 작업 Playbook

## 1. 변경을 시작하기 전

1. 사용자·기획의 최신 요구인지 확인한다.
2. 담당 Map과 파일 소유권을 확인한다.
3. Editor 실행 여부와 저장되지 않은 변경을 확인한다.
4. 기존 코드·Blueprint·Data Asset·Unreal 기본 기능으로 해결 가능한지 찾는다.
5. 완료 조건을 자동 검증과 수동 화면 검증으로 분리한다.

`Lvl_DroneTraining`은 현재 팀원 소유 Production Map이다. 기능 개발을 이유로 저장, 복제, 자동 배치, 분할하지 않는다.

## 2. 구현 Loop

```text
요구·경계 확인
→ 재현 또는 실패 기준 작성
→ 가장 작은 기능 구현
→ 코드·자산 참조 자체 검토
→ Build·Blueprint·Map·자동화 검증
→ 필요한 화면·조작 수동 확인
→ STATUS·WORKBOARD·WORKLOG 갱신
→ 팀원에게 검증된 산출물과 배치 가이드 전달
```

자동 검증만 통과했고 화면 확인이 남았으면 `Done`이 아니라 `Doing` 또는 `수동 미확인`이다.

## 3. 의존성 선택 순서

1. 기능을 만들지 않고 해결할 수 있는가
2. 기존 프로젝트 코드·자산을 재사용할 수 있는가
3. Unreal Engine 기본 기능으로 가능한가
4. 이미 설치된 프로젝트 의존성으로 가능한가
5. 새 의존성의 이득이 Build·협업·보안 비용보다 큰가
6. TestMap에서 격리 검증과 제거가 가능한가

새 Plugin/Library가 필요한 경우에도 Runtime, Editor-only, 개인 Codex Tool을 구분한다. 개인 Tool을 프로젝트 Runtime 의존성처럼 공유하지 않는다.

## 4. TestMap과 Production Map 경계

| 구분 | 허용 | 금지 |
|---|---|---|
| `Lvl_DroneTutorialSystemsTest` | Ring Handle, Gate 상태색, 역할 표적, Carryable, HUD, Mission Rule 시험 | 대형 환경 복제, 최종 아트 배치 |
| `Lvl_DroneTraining` | 열람, 합의된 통합, 담당자 수동 배치 | 무단 저장·덮어쓰기·자동 구성·시험용 Actor 누적 |
| 기타 TestMap | AI, MG, 차량, 자동포탑, 역할 회귀 | Front-end/Production 기본 경로를 시험 편의로 변경 |

## 5. 실패 진단 규칙

1. 오류 메시지와 재현 입력을 보존한다.
2. Source, Asset, Config, LFS Pointer, Plugin/Toolchain 중 어느 계층인지 분리한다.
3. 재현 가능한 최소 Map/Test를 만든다.
4. 원인을 설명할 수 있는 수정만 적용한다.
5. 관련 집중 테스트 뒤 전체 회귀를 실행한다.
6. 임시 우회와 근본 수정은 문서에서 구분한다.

## 6. 공유 언어와 ADR

새 기능은 C++ Class명, Blueprint Asset명, 화면 한글명, 작업보드 카드명을 가능한 한 같은 개념으로 맞춘다. 다음에 해당하면 짧은 ADR을 남긴다.

- Production Map 소유권 또는 저장 규칙 변경
- Runtime Plugin/Library 추가
- 전역 Map/GameMode/Input 변경
- 대형 LFS 자산 이동·삭제
- 기존 공개 API 또는 Data Asset 계약 변경

ADR 최소 형식:

```text
제목 / 날짜 / 상태
맥락
결정
선택 이유
영향과 검증
되돌리는 방법
```

## 7. 문서와 Diagram

- Diagram은 실제 구현된 Actor/Component/Data Asset과 Test 이름을 사용한다.
- 계획 단계와 구현 완료를 색이나 Label로 구분한다.
- 변경 전·변경점·변경 후를 한 화면에 표현할 가치가 있을 때만 Diagram을 만든다.
- 복잡하지 않은 흐름은 Markdown 목록으로 유지한다.
- 외부 공유본에는 비밀번호, Token, 개인 경로의 민감 정보, 원시 Codex Session을 넣지 않는다.

## 8. 현재 Drone 적용 예

```text
팀원 Training Map 보존
→ 경량 Tutorial Systems Test Map 생성
→ Ring/표적/HUD 최소 Vertical Slice
→ TestMap 전용 자동화 + 수동 한·두 Lap
→ 실패 3건과 전체 회귀 분리
→ 검증된 BP/Data/가이드만 Training 담당자에게 인계
→ Mission Rule 데이터화
→ Jamming Vertical Slice
```

