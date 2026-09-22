# 프로젝트형 일경험 수행계획서 수정 가이드

기준일: 2026-09-22 (Asia/Seoul)

대상 문서:

`C:\Users\Metacon_41\Downloads\제출서류-1\새 폴더\1.프로젝트형 일경험 수행계획서_정규연.hwp`

이 가이드는 원본 HWP를 수정하지 않고 문서의 실제 텍스트와 서식을 읽어 정리했다. 회색·기울임 글씨는 예시이므로 모두 실제 프로젝트 내용으로 교체하고, 교체한 글씨는 검정색·기울임 해제로 통일한다.

## 1. 먼저 확인할 결론

- 현재 문서의 기업 정보, 실행기간, 팀원 이름과 1차 역할 표는 이미 입력돼 있다.
- 프로젝트명은 `언리얼·유니티 기반`으로 되어 있지만 실제 프로젝트는 Unreal Engine 기반이므로 `유니티`를 빼는 것이 맞다.
- 회색·기울임 예시는 `주요기능`, `필요역량`, `예상 결과물`, `기대효과`, `기능 표`, `예상 결과물 설명`, `8주 일정`, `역할 분담`, `예산`에 남아 있다.
- 회색은 아니지만 `oooo 앱`, `중고거래`, `판매물품`, `CNN`, `파이썬·자바`, `Android·iOS`, `AWS RDS·S3`도 다른 프로젝트의 예시이므로 반드시 교체한다.
- 수행계획서이므로 완료형인 `구현했다`보다 계획형인 `구현한다`, `검증한다`, `제작한다`를 사용한다.
- 공식 프로그램 기간 밖에서 한 일을 프로그램 실적으로 단정하지 않는다. 기존 Prototype을 언급해야 한다면 `기초 Prototype을 바탕으로 고도화한다` 정도로 표현한다.

## 2. 그대로 두어도 되는 항목

아래 값은 실제 정보가 맞을 때만 유지한다.

| 항목 | 현재 값 | 처리 |
|---|---|---|
| 제안기업 | 제이쓰리씨 | 기업 확인 후 유지 |
| 사업장 주소 | 서울특별시 강서구 마곡중앙로111, 101동 523(업무)호 | 기업 확인 후 유지 |
| 담당자 | 최승호 대표 | 기업 확인 후 유지 |
| 연락처·이메일 | 문서 기입값 | 제출 전 오탈자 확인 |
| 직무 분야 | IT | 유지 권장 |
| 실행기간 | 2026.09.28.~2026.11.22. (8주) | 운영기관 일정과 일치하면 유지 |
| 팀명 | 1팀 | 운영기관 배정과 일치하면 유지 |
| 팀원 | 정규연·전유경·이수림·박정환 | 이름·순서 확인 |
| 1차 역할 | 언리얼 프로그래밍·레벨디자인·시네마틱·기획 | 실제 합의와 일치하면 유지 |

## 3. 상단 프로젝트 개요 교체안

### 프로젝트명

현재:

> 언리얼·유니티 기반 PC용 인터랙티브 시뮬레이터 콘텐츠 개발 프로젝트

권장:

> Unreal Engine 기반 PC용 드론 운용·정찰 미션 시뮬레이터 프로토타입 개발

`Project:Droner`가 최종 제목으로 확정된 경우에만 제목 뒤에 병기한다.

### 프로젝트 소개 중 `2. 제안배경`

기업 소개 문단은 기업 확인 후 유지하고, 회색 예시로 표시된 제안배경은 아래처럼 바꾼다.

> 드론·XR·시뮬레이터와 같은 실시간 3D 콘텐츠 분야에서는 조작, 사용자 인터페이스, AI, 레벨 디자인과 자산 통합을 함께 다룰 수 있는 실무 역량이 요구됩니다. 그러나 단일 기능 중심의 실습만으로는 기획부터 구현, 협업, 검증까지 이어지는 전체 제작 공정을 경험하기 어렵습니다. 이에 실무 전문가의 코칭 아래 Unreal Engine 기반 PC 콘텐츠를 팀 단위로 제작하며 학업과 산업 현장의 간극을 줄이고, 참여자가 현장형 개발 역량을 습득할 수 있는 프로젝트를 추진하고자 합니다.

### 프로젝트 소개 중 `3. 제안내용`

> 참여자는 Unreal Engine 5.8과 C++·Blueprint를 활용해 드론 조종, 비행 훈련, 미션 선택, 목표 수행, AI와 환경 방해요소가 포함된 싱글플레이 프로토타입을 개발합니다. 기획·레벨디자인·시네마틱·프로그래밍 역할을 분담하고, Git·Git LFS와 기능별 TestMap 및 반복 검증 절차를 활용해 통합 가능한 결과물을 완성합니다.

### 주요기능

기존의 `AI 알고리즘 선택`, `유사 물품 숨김`, `최적 물품 추천`은 전부 삭제하고 다음처럼 교체한다.

- Drone 비행 조작, Camera와 Keyboard·Mouse·Gamepad 입력
- Spline 안내선, 순서형 Gate, 속도·고도 HUD와 Segment·Lap 기록
- 로비, Mission 선택·Briefing, Drone 선택, 목표·결과 UI
- 정찰 Scan, FPV 자폭, Payload 픽업·드랍 Mission 기능
- AI 순찰·감지·추적, Smart Object·포탑과 재밍·기상 방해요소

칸이 좁으면 앞의 세 줄만 쓰고 세부 기능은 뒤쪽 기능 표에서 설명한다.

### 필요역량

기존의 `파이썬·자바스크립트`, `MS-Office` 예시는 다음으로 교체한다.

- Unreal Engine C++·Blueprint·UMG 활용 능력
- 3D Level Design, Asset 연결과 Collision 조정 능력
- Mission·UI·Cinematic 기획 및 팀 협업 능력
- Git·Git LFS, 문서화와 기능 검증 능력

### 예상 결과물 이미지 3칸

예시 문구를 지우고 실제 화면을 넣는다.

1. Tutorial Course: Drone, Spline 안내선, Ring Gate와 Flight HUD가 함께 보이는 화면
2. Front-end: Mission 선택, 설명과 Drone 선택 UI가 보이는 화면
3. Mission Gameplay: AI·Smart Object 또는 Scan·Payload·FPV 기능이 보이는 화면

최종 화면이 없으면 `개발 중 Greybox 화면`이라고 명시한다. 인터넷 참고 이미지를 결과물처럼 넣지 않는다.

### 기대효과 및 활용 분야

> Unreal C++와 Blueprint를 함께 사용하는 실시간 Gameplay 구조 설계, Data-driven Mission 제작, AI·UI·Level 기능 통합, Git LFS 기반 협업과 반복 검증 역량을 강화합니다. 결과물은 PC용 Drone 조작 Tutorial과 Mission형 인터랙티브 콘텐츠의 Prototype, 팀 개발 산출물 및 취업 Portfolio로 활용하며, 이후 XR·시뮬레이터 콘텐츠로 확장할 수 있는 기반으로 사용합니다.

## 4. `2. 프로젝트 수행계획` 본문 교체안

### 1-가. 추진배경 및 필요성

`oooo 앱`, `월간 이용자 1,800만 명`, `중고거래`, `유사 판매 물품` 문장은 전부 삭제한다.

권장 문구:

> ㅇ 드론·시뮬레이터·XR 등 실시간 3D 콘텐츠 산업은 조작, UI, AI와 Level을 통합할 수 있는 실무형 개발 역량을 요구함  
> ㅇ 단일 기능 실습만으로는 기획, 구현, Asset 통합, 팀 협업과 검증까지 이어지는 전체 제작 공정을 경험하기 어려움  
> ㅇ Unreal Engine 기반 Drone Mission Prototype을 팀 단위로 제작해 실무 개발 흐름과 문제 해결 경험을 확보할 필요가 있음

### 1-나. 프로젝트 소개

기존 판매물품 AI 문장을 다음으로 교체한다.

> ㅇ Drone을 직접 조종해 비행 훈련과 정찰·전달·회피·전투 목표를 수행하는 싱글플레이 PC Prototype 개발  
> ㅇ Tutorial에서는 Spline Course, 순서형 Gate, Telemetry HUD와 Segment·Lap 기록을 제공  
> ㅇ Story Mission에서는 Lobby→Mission 선택·Briefing→Drone 선택→목표 수행→결과 확인 흐름을 구현  
> ㅇ AI·Smart Object·Turret·재밍·기상 요소를 Mission 상황에 단계적으로 통합

### 2-가. 주요 기능 표

기존 `파이썬`, `자바`, `판매물품 분류`, `스마트폰 앱` 행은 삭제한다. 표 행을 추가할 수 있으면 다음 네 행을 사용한다.

| 구분 | 기능 | 설명 |
|---|---|---|
| Gameplay | Drone 조작·Camera | Enhanced Input 기반 Keyboard·Mouse·Gamepad 조작, 비행 Mode와 Camera 전환 |
| Tutorial | Course·Gate·기록 | Spline Course, 순차 Gate, 속도·고도 HUD, Segment·Lap 시간·거리·평균속도 기록 |
| Mission/UI | Front-end·Objective | Mission 선택·Briefing·Drone 선택·목표 UI·성공/실패와 재도전 흐름 |
| AI/환경 | NPC·Smart Object·방해요소 | 순찰·감지·추적, 포탑 점유, 재밍·바람·비 Greybox를 Mission에 연결 |

행을 늘릴 수 없으면 두 행으로 합친다.

| 구분 | 기능 | 설명 |
|---|---|---|
| Gameplay | Drone·Tutorial | 비행 조작, Spline·Gate, Telemetry와 기록 시스템 구현 |
| Mission | UI·AI·환경 | Mission 흐름, 목표 UI, AI·Smart Object·재밍·기상 요소 통합 |

### 2-나. 적용 기술 및 역량

`판매 물품 분류 알고리즘`, `CNN`을 삭제하고 다음으로 교체한다.

> ㅇ Unreal Gameplay 구조 설계  
> - C++은 상태·규칙·계산·검증을 담당하고 Blueprint·UMG는 Asset 연결, UI와 조정값을 담당하도록 분리  
> ㅇ Data-driven Mission·UI  
> - Data Asset과 Event 기반으로 Mission 선택, Drone 선택, 목표와 결과 상태를 연결  
> ㅇ Drone Tutorial과 AI  
> - Enhanced Input, Spline·Spline Mesh, AI Perception, StateTree와 Smart Object 활용  
> ㅇ 협업·품질 관리  
> - Git·Git LFS, TestMap, Editor Build, Blueprint Compile과 Unreal Automation Test 활용

### 2-다. 예상 결과물

이미지 칸에는 대표 화면 한 장 또는 세 화면을 합친 이미지 한 장을 넣는다.

설명 칸 권장 문구:

> - PC에서 실행 가능한 Unreal Engine Drone Mission Greybox Prototype  
> - Tutorial Course·Gate·Telemetry·Segment/Lap 기록 기능  
> - Mission 선택·Briefing·Drone 선택·목표·결과 UI  
> - Scan·FPV 자폭·Payload 전달과 AI·Smart Object 연동 시험 기능  
> - 기능별 TestMap, 검증 결과와 팀원용 제작·운영 문서

## 5. 8주 추진일정

실행기간이 확정됐다면 주차는 다음과 같다.

| 주차 | 기간 |
|---|---|
| 1주차 | 09.28.~10.04. |
| 2주차 | 10.05.~10.11. |
| 3주차 | 10.12.~10.18. |
| 4주차 | 10.19.~10.25. |
| 5주차 | 10.26.~11.01. |
| 6주차 | 11.02.~11.08. |
| 7주차 | 11.09.~11.15. |
| 8주차 | 11.16.~11.22. |

현재 표 구조에 맞춘 권장 입력은 다음과 같다.

| 구분 | 추진 내용 | 표시할 주차 |
|---|---|---|
| 도입 | 요구사항·Figma·기존 Prototype 분석, 개발환경과 Git/LFS 기준 확정 | 1 |
| 계획 | 역할 분담, C++–Blueprint 책임·Data 구조·Milestone 설정 | 1~2 |
| 실행 1 | Drone 입력·비행·Camera·Telemetry와 Tutorial Course·Gate | 2~4 |
| 실행 2 | Front-end, Mission·Drone Data, 선택·목표·결과 UI | 4~6 |
| 실행 3 | AI·Smart Object·무기·재밍·기상과 Level 통합 | 5~7 |
| 디버깅 | Build·Blueprint Compile·PIE·Standalone 반복 검증과 결함 수정 | 7~8 |
| 오프라인 미팅 | 중간 산출물·차단사항·통합 결과 Review | 실제 합의한 회차만 표시 |

표의 색칠 또는 `●` 표시는 실제 일정과 팀 합의를 확인한 뒤 넣는다.

## 6. 역할 분담 표 교체안

상단의 간단한 역할 표보다 뒤쪽 회색 예시 역할 표가 더 구체적이다. `Front-end·AWS RDS·S3`, `캐릭터 디자인`, `데이터 수집` 예시는 삭제한다.

| 구분 | 이름 | 주요 역할 권장안 |
|---|---|---|
| 팀장 | 정규연 | Unreal C++ Gameplay 개발·기능 통합, Blueprint 조정값 노출, Git/Git LFS와 Build·자동화 검증 관리 |
| 팀원1 | 전유경 | Level Design, Tutorial Course·Gate, Mission Map·Collision·Lighting·Smart Object 배치 |
| 팀원2 | 이수림 | 시작·Mission Trailer, Sequencer·Camera Shot·자막과 Cinematic Asset 제작 |
| 팀원3 | 박정환 | Game·Mission 기획, 목표·Rule·Data 명세, UI 문구와 Playtest 항목 정리 |

실제 팀 합의가 다르면 이름별 책임을 먼저 수정한다. 공동 작업은 `통합 Test·시연·문서 검토`로 별도 한 줄을 추가해도 된다.

## 7. 수행 방법과 멘토 활용

### 커뮤니케이션·공유

실제로 사용하는 도구만 남긴다.

> ㅇ 커뮤니케이션: 팀 합의 채널로 진행 상황과 차단사항을 수시 공유하고, 주 1회 Online Meeting과 격주 Offline Meeting에서 주간 목표와 통합 결과를 점검  
> ㅇ 프로젝트 공유: GitHub·Git LFS로 Source와 Unreal Asset을 공유하고, Trello와 Markdown 문서로 담당·진행·검증 상태를 기록

`ZOOM`, `카카오톡`, `Discord` 중 실제 사용하는 수단을 문장에 명시한다.

### 멘토 선임 및 활용

멘토 이름과 일정은 임의로 만들지 말고 기업·운영기관 확인 후 기입한다.

> ㅇ 선발 기준: 운영지침의 멘토 요건을 충족하고 Unreal Engine 또는 실시간 3D 콘텐츠 개발·Project 관리 경험을 보유한 실무자  
> ㅇ 활용 계획: 1주차 요구사항·역할 Review, 주 1회 기술·기획 Feedback, 4주차 중간 Milestone Review, 8주차 최종 시연·산출물 Review

## 8. 예산 표 처리

현재 회색 예산은 전부 다른 프로젝트의 예시다. 특히 `도메인`, `아이템 샘플`, `대구-부산·천안 000기업 방문`은 Drone 프로젝트 근거가 없으므로 그대로 제출하면 안 된다.

- `900,000원×2개월=1,800,000원`이 공식 배정액과 일치하는지 먼저 확인한다.
- 지출 항목은 2026년 프로젝트 실행비 집행 가이드와 담당자 승인을 받은 것만 적는다.
- 후보는 회의실 임차, Project 전용 Software·Asset 사용료, 참고 도서, 인쇄·시연물, 승인된 현장조사 교통비와 회의비다.
- 각 행은 `단가×수량×횟수=금액`이 맞아야 하며 총계는 예산 총액과 정확히 일치해야 한다.
- Unreal Engine 자체 사용료처럼 실제 지출이 없는 항목, 승인되지 않은 개인 구독·장비·교통, 영수증 증빙이 어려운 항목은 넣지 않는다.
- 정확한 품목과 금액이 확정되기 전에는 예시 숫자를 조금만 바꾸지 말고 표 전체를 `검토 중`으로 관리한다.

예산 행 작성 형식:

| 지출항목 | 세부내역 예시 형식 | 사용시기 | 금액 |
|---|---|---|---|
| 임차비 | 회의실 `[단가×시간×횟수]` | 격주 또는 실제 일정 | 계산값 |
| Software·Asset | 승인된 License·Marketplace Asset `[단가×수량]` | Project 기간 내 | 계산값 |
| 도서·인쇄 | Unreal·게임기획 참고자료 또는 최종 시연물 `[단가×수량]` | 실제 구매 주차 | 계산값 |
| 교통·회의 | 승인된 Offline Meeting·현장조사 `[단가×인원×횟수]` | 실제 일정 | 계산값 |

## 9. 제출 전 잔존 예시 검색

한글의 찾기 기능으로 아래 단어를 하나씩 검색해 남은 예시가 없는지 확인한다.

```text
oooo
중고거래
판매물품
유사 물품
CNN
파이썬
자바
안드로이드
IOS
AWS
RDS
S3
000기업
(예상 결과물 이미지)
#
```

최종 확인:

- 교체한 본문은 검정색·기울임 해제
- 표의 행 높이와 페이지 넘침 확인
- 회사·팀원 개인정보와 실행기간 재확인
- `유니티`와 Unreal 전용 기술 내용의 충돌 제거
- 현재 구현과 8주 계획을 구분하고 완료하지 않은 기능을 완료 실적으로 쓰지 않음
- 예산 총액과 세부 합계 일치
- HWP 저장 후 PDF로 한번 출력해 글자 잘림·표 깨짐 확인

## 10. 과장하지 않을 표현

- 실제 군사 시스템 납품·계약
- 실기체와 동일한 비행물리 재현
- Network·Android 구현
- 모든 Story Mission과 최종 Art 완성
- 출시·수상·상용 Service

안전한 표현은 `싱글플레이 PC Greybox Prototype`, `실시간 3D 콘텐츠`, `Mission형 Drone 조작 경험`, `계획·구현·검증 역량`이다.
