# Drone Git LFS 용량·대역폭 절감 계획

기준일: 2026-09-15 (Asia/Seoul)

이 문서는 `D:\JGY\project\drone`의 실제 Git LFS Pointer를 로컬에서 집계한 결과와, 팀 작업을 깨뜨리지 않고 GitHub LFS 사용량을 줄이는 순서를 정리한다. 이 기록만으로 `.gitattributes`를 변경하거나 Asset을 삭제·이동하지 않는다.

## 결론

현재 `*.uasset`, `*.umap` 전체를 LFS로 두는 규칙은 유지한다. 이를 `100MB 이상만 LFS`로 바꾸는 것은 해결책이 아니다.

- Git Attributes는 파일 크기를 조건으로 추적하지 않고 경로·확장자 Pattern으로 적용한다.
- 100MB 미만 Unreal Package를 일반 Git으로 돌려도 파일 내용 자체가 사라지지 않는다. 병합 불가능한 Binary의 모든 버전이 일반 Git 이력에 쌓여 Clone과 Fetch가 더 무거워진다.
- GitHub 일반 Git은 100MB를 넘는 단일 파일을 차단하므로 큰 Unreal Package에는 어차피 LFS가 필요하다.
- 현재 용량의 핵심은 작은 Blueprint 수가 아니라 `10~100MiB` Texture·Mesh·Map과 외부 환경 Pack이다.

따라서 절감 기준은 **파일 크기 Threshold가 아니라 프로젝트 필수 범위와 선택형 외부 Asset 범위의 분리**다.

## 2026-09-15 실제 집계

집계 기준은 현재 로컬 `main=10da7ce`와 로컬에 존재하는 전체 Ref다. 당일 GitHub DNS 조회 실패가 있었으므로 서버에만 존재하는 새 Commit까지 포함했다고 주장하지 않는다.

### 현재 Commit이 참조하는 LFS

| 구간 | 파일 수 | 용량 | 비율 |
|---|---:|---:|---:|
| 1MiB 미만 | 3,602 | 0.45GiB | 1.6% |
| 1~10MiB | 999 | 4.26GiB | 15.4% |
| 10~100MiB | 942 | 21.34GiB | 77.2% |
| 100MiB 이상 | 7 | 1.60GiB | 5.8% |
| 합계 | 5,550 | 약 27.66GiB | 100% |

`100MiB 이상만 LFS`로 바꾸면 LFS 밖으로 이동하는 것은 현재 데이터의 대부분인 약 26.05GiB다. 이것은 삭제가 아니라 일반 Git Binary 이력으로의 이동이므로 저장소 운영이 더 나빠진다. 반대로 1MiB 미만 Asset 전체는 3,602개지만 0.45GiB뿐이라 작은 파일 예외를 만들어 얻는 절감도 작다.

### 70MiB 안전선 가정

70MiB로 낮추면 GitHub의 일반 Git 단일 Object 100MiB Hard Limit까지 약 30MiB 여유가 생긴다. 이 의미에서는 100MiB와 정확히 맞추는 것보다 안전하다. 그러나 현재 파일에 적용하면 결과는 다음과 같다.

| 가정 | 일반 Git으로 이동 | LFS에 남음 |
|---|---:|---:|
| 50MiB Threshold | 5,512개·24.17GiB | 38개·3.49GiB |
| 70MiB Threshold | 5,538개·25.67GiB | 12개·1.99GiB |
| 100MiB Threshold | 5,543개·26.05GiB | 7개·1.60GiB |

즉 70MiB는 **Push 거절 안전선**은 되지만 **저장소 용량 안전선**은 아니다. 새 Curated 저장소에서 시작해도 최소 25.67GiB의 Unreal Binary Snapshot이 일반 Git으로 들어가며, 이후 각 Binary 버전도 일반 Git 이력과 Clone 대상이 된다. GitHub의 일반 Git 저장소 권장 On-disk 상한은 10GB이고 단일 Git Object 권장 크기는 1MB이므로 이 구성은 권장 범위를 크게 벗어난다.

또한 `.gitattributes`는 파일 크기 조건을 지원하지 않는다. 70MiB 규칙은 확장자 한 줄로 만들 수 없으며 Commit Hook/CI가 매번 크기를 검사해 개별 경로를 LFS로 전환해야 한다. 69MiB Map이 다음 저장에서 75MiB가 되면 추적 방식을 바꾸고 기존 Git Blob 처리까지 해야 하므로 팀 운영이 복잡해진다.

### 전체 로컬 Ref의 고유 LFS Object

- 고유 Object 6,137개
- 약 29.62GiB
- 현재 Commit 대비 과거 고유 Object 증가는 약 1.96GiB

즉, 현재는 오래된 이력보다 **현재 Checkout 자체의 27.66GiB**가 더 큰 문제다. 다만 LFS Package를 수정해 Push할 때마다 전체 파일 크기의 새 Object가 추가되므로 374.94MiB Training Map이나 약 206MiB MilitaryBase Map을 반복 저장하면 이력 비용이 빠르게 커진다.

### 현재 경로별 구성

| 구분 | 파일 수 | 용량 |
|---|---:|---:|
| 프로젝트 소유 `Content/Drone` (`ThirdParty` 제외) | 67 | 0.89GiB |
| `Content/Drone/ThirdParty` | 1,061 | 4.61GiB |
| `Content/Drone` 밖 Vendor Root | 4,422 | 22.16GiB |

큰 Root는 `Content/MillitaryBase` 7.67GiB, `Content/FC_MilitaryCamp` 6.20GiB, `Content/STF` 3.04GiB, `Content/Battlefield` 2.71GiB 순이다. 이 값은 삭제 가능량이 아니라 우선 감사할 범위다. 실제 Map의 Dependency Closure에 들어가는 Asset은 임의로 빼면 안 된다.

## 왜 Map 저장이 특히 비싼가

전체 이력의 큰 Object에는 다음과 같은 Map 버전이 반복된다.

- `Lvl_DroneTraining.umap`: 374.94MiB 크기의 서로 다른 Object 3개
- `Lvl_MilitaryBase.umap`: 약 204.79~206.08MiB 버전 여러 개
- `Lvl_MilitaryBase_Test.umap`: 206.34MiB

LFS는 변경된 부분만 GitHub 저장량에 추가하는 방식이 아니라 변경된 파일의 새 전체 Object를 저장한다. 팀원이 제작 중인 Training Map을 건드리지 않고 0.27MiB 경량 TestMap을 분리한 현재 결정은 용량 측면에서도 맞다.

## 안전한 실행 순서

### 1단계 — 지금 바로 적용하는 운영 규칙

1. `.gitattributes`의 모든 `.uasset`·`.umap` LFS 규칙을 유지한다.
2. `git lfs fetch --all`, `git lfs push --all`은 백업·이관처럼 목적이 명확할 때만 실행한다.
3. 대형 Map은 담당자를 한 명으로 정하고 동시에 수정하지 않는다. Test는 경량 TestMap 또는 별도 작은 Map에서 한다.
4. 동일 환경 Map의 시험 사본을 Git에 여러 개 만들지 않는다.
5. GitHub Actions와 자동 검증에서 LFS 본문이 필요 없는 Job은 LFS 다운로드를 끈다.
6. GitHub Billing의 LFS Budget과 Alert를 설정한다. 초과 과금을 원하지 않으면 Budget을 0으로 유지하되, Push/Download가 막힐 수 있음을 팀에 알린다.
7. GitHub Source Archive에 LFS Object 포함 옵션은 특별한 배포 이유가 없으면 켜지 않는다.

### 2단계 — 현재 Checkout과 팀원 다운로드 축소

1. 환경별 대표 Map에서 Unreal Asset Registry/Reference Viewer 기반 Dependency Closure를 다시 산출한다.
2. 실제 채택 Map·직접/간접 Dependency만 보존하고 Demo Map, Overview, Source Texture, 중복 LOD·고해상도 변형을 후보로 분류한다.
3. 프로젝트 Core는 C++·Config·프로젝트 소유 Asset·경량 TestMap으로 유지한다.
4. 선택형 환경 Pack은 외부 Asset Depot에 두고 `pack id / version / hash / 설치 대상 경로 / License` Manifest와 검증 Script로 받는다.
5. Core Asset이 선택형 Pack을 Hard Reference하지 않게 하고, 환경별 Mission/Map만 해당 Pack을 요구하게 한다.

같은 GitHub Billing 소유자 아래에 Repo만 하나 더 만드는 것은 전체 LFS 저장 할당량을 줄이지 않는다. 다만 팀원이 필요한 Repo만 Clone하도록 나누는 데는 도움이 된다. 저장 할당량 자체를 옮기려면 별도 외부 저장소/NAS/Object Storage 또는 다른 Billing 주체가 필요하다.

### 3단계 — 선택 다운로드 Profile

Git LFS는 `lfs.fetchinclude`와 `lfs.fetchexclude`로 경로별 다운로드를 제한할 수 있다. 그러나 LFS Pointer만 남은 `.uasset`·`.umap`을 Unreal Content 아래 둔 채 Editor를 열면 잘못된 Package로 인식될 수 있다. 따라서 단순 `fetchinclude`를 팀 기본값으로 바로 배포하지 않는다.

후속 `GIT-LFS-CAP-01`에서 다음을 별도 Clone으로 검증한다.

1. `GIT_LFS_SKIP_SMUDGE=1`로 자동 LFS Download를 끈 Clone
2. Git Sparse Checkout으로 불필요한 Optional Content Folder 자체를 Worktree에서 제외
3. 선택한 Profile의 LFS Object만 `git lfs fetch --include=...`로 수신
4. `git lfs checkout`, Package Magic, Asset Registry, Build, 지정 Map Load 검증

Profile 예시는 `Core`, `Tutorial`, `MilitaryBase`, `MilitaryCamp`, `Battlefield`, `AI`로 나누되 Dependency 감사가 끝나기 전 경로 목록을 확정하지 않는다. Repository-wide `.lfsconfig`도 아직 추가하지 않는다.

### 4단계 — GitHub 저장량 자체를 크게 줄여야 할 때

현재 Branch에서 Asset을 지우면 새 Clone의 현재 LFS Download는 줄일 수 있지만, 이미 GitHub에 올라간 LFS Object는 원격 저장 할당량에 계속 포함된다. 단순 `.gitattributes` 변경, Commit 삭제 또는 로컬 `git lfs prune`만으로 GitHub 사용량이 줄어든다고 간주하지 않는다.

정말 원격 저장량을 초기화해야 한다면 다음 중 하나를 사용자·팀 합의 뒤 선택한다.

- 검증된 Curated Snapshot으로 새 저장소를 만들고 팀원이 모두 새로 Clone한다.
- 기존 저장소의 Issue/Star/Fork/URL 영향까지 감수하고 백업 후 삭제·재생성한다.
- GitHub Support에 원격 LFS Object 정리 가능 범위를 문의한다.
- 현재 전체 Asset을 계속 GitHub에 유지해야 하면 적절한 요금제로 용량을 확보한다.

이 단계는 파괴적이고 팀 전체 Clone을 무효화할 수 있으므로 Codex가 임의로 실행하지 않는다.

## 이번 결정

- `.gitattributes` 변경: 하지 않음
- Unreal Asset 삭제·이동: 하지 않음
- Git 이력 재작성: 하지 않음
- 원격 Push/Repo 재생성: 하지 않음
- 다음 기술 작업: `GIT-LFS-CAP-01`에서 Map별 Dependency Closure와 외부 Depot 후보를 산출하고, 별도 Clone에서 Sparse/LFS Profile을 검증

## Free/Pro에서 월 $5 Budget 예상

2026-09-15 GitHub 공식 Calculator 기준 추가 LFS Storage는 `$0.07/GiB-month`, 추가 Download Bandwidth는 `$0.0875/GiB`다. Free/Pro에는 Storage 10GiB와 월 Download 10GiB가 포함된다. GitHub Billing 화면의 실제 Associated Storage가 최종 과금 기준이며, 아래 값은 로컬 전체 Ref 고유 Object 29.62GiB를 원격과 같다고 가정한 근사치다.

| 월 사용 상황 | 예상 추가 비용 |
|---|---:|
| 저장만 유지, 큰 Download 없음 | `(29.62-10) × $0.07` = 약 `$1.37/월` |
| 현재 27.66GiB 전체 Clone 1회 | 저장 `$1.37` + 초과 Download `(27.66-10) × $0.0875` 약 `$1.55` = 약 `$2.92/월` |
| 현재 27.66GiB 전체 Clone 2회 | 저장 `$1.37` + 초과 Download `(55.32-10) × $0.0875` 약 `$3.97` = 약 `$5.34/월` |

따라서 `$5`가 **월 Budget**이라면 평소 변경분 Pull과 한 달 전체 Clone 1회 정도는 현재 규모에서 대체로 감당한다. 같은 달 전체 Clone 2회, CI/Actions의 전체 LFS Download, LFS를 포함한 Source Archive Download가 겹치면 한도를 넘을 수 있다. `$5`는 두 달치 선불 잔액이 아니라 월별 지출 상한으로 이해한다. 실제 사용량만 청구되며 `Stop usage when budget limit is reached`를 켜면 초과 과금 대신 그 달 LFS 사용이 차단될 수 있다.

Team/Enterprise Plan은 Storage와 월 Bandwidth가 각각 250GiB 포함되므로 현재 규모만으로는 추가 과금이 발생하지 않는다. 개인 Free/Pro 기준 계산과 섞지 않는다.

## 공식 근거

- [GitHub Git LFS 과금](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)
- [GitHub Git LFS 구성](https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage)
- [GitHub 일반 Git 저장소·Object 권장/강제 제한](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits)
- [GitHub 원격 LFS Object 제거](https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage)
- [GitHub Archive의 LFS Object](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-git-lfs-objects-in-archives-of-your-repository)
- [Git LFS fetch include/exclude 공식 Manual](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-fetch.adoc)
