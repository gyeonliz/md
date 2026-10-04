# Bangkok City·OilRig Preview 이식 기준

기준일: 2026-09-30 (Asia/Seoul)

## 결론

10/04 사용자 확인: Lvl_BangkokCity.umap은 ec2e88f(10/01 팀원)에서 의도적으로 삭제됨(사용 불가 판단). ASSET-BANGKOK-01은 종료(맵 삭제). 아래9월 D PC 이식·검증은 당시 근거이며 현재 맵 존재/Pass를 뜻하지 않는다. ThirdParty/BangkokCity 의존987개·LFS약11.46GiB는 남아 있고 정리 여부는 사용자 결정 대기.

- Bangkok은 공급 폴더의 자산 전시용 `Maps/Overview`가 아니라 실제 도시 환경 `Maps/BangkokCity`를 이식했다.
- 당시 이식 맵은 /Game/Drone/Maps/Lvl_BangkokCity였으나 10/01 의도된 삭제로 현재 없다.
- 프로젝트 소유 의존 자산은 `/Game/Drone/ThirdParty/BangkokCity` 아래 987개다.
- OilRig의 기존 `/Game/Drone/Maps/Lvl_OilRig`은 `/Game/Liope_Tr/Maps/Overview` 기반 자산 전시 맵이므로 보존한다.
- 실제 오일리그 장면인 `/Game/Liope_Tr/Maps/Preview`는 별도 `/Game/Drone/Maps/Lvl_OilRigPreview`로 이식했다. 의존 자산은 `/Game/Drone/ThirdParty/OilRigPreview` 아래 614개다.

## Bangkok 처리 방법

원본 `D:\JGY\project\BangkokCity`는 수정하지 않았다. `D:\JGY\project\Unreal_260821\_Staging\DroneAssetStage`의 복사본에서만 다음 작업을 했다.

1. `/Game/BangkokCity/Maps/BangkokCity`를 `/Game/Drone/Maps/Lvl_BangkokCity`로 복제했다.
2. 환경 맵이 Drone의 GameMode·Controller·Pawn·UI를 바꾸지 않도록 Map GameMode Override를 비웠다.
3. 맵의 재귀 의존성만 `/Game/Drone/ThirdParty/BangkokCity`로 이동했다.
4. 이동 후 Redirector를 ResavePackages로 해소하고 맵 참조를 새 경로로 저장했다.
5. 검증된 맵 1개와 의존 자산 폴더만 본 프로젝트에 복사했다.

첫 대량 저장에서 스크립트가 `/Game/Drone` 전체를 저장해 기존 스테이징 팩까지 재빌드하며 중단된 문제가 있었다. `StageDependencyClosure.py`는 이후 대상 ThirdParty 루트와 유지 Seed만 저장하도록 좁혔다. UE 5.8에서 Python `AssetTools.fixup_referencers`는 노출되지 않으므로 Redirector 정리는 Epic 공식 `ResavePackages -FixupRedirects` 방식으로 처리한다.

## 자동 검증 결과

| 항목 | 결과 |
|---|---|
| 중앙 Map | `/Game/Drone/Maps/Lvl_BangkokCity` |
| ThirdParty 자산 | 987 `.uasset` |
| Map 포함 의존성 폐쇄 | 988 Package |
| 외부 `/Game` 참조 | 0 |
| 누락 참조 | 0 |
| Map load | 성공 |
| Map GameMode Override | `None` |
| Map Check | `0 errors / 0 warnings` |
| 신규 용량 | 12,309,059,738 bytes, 약 11.46GiB |
| Git 속성 | `.uasset`, `.umap` 모두 LFS |

## OilRig Overview와 Preview 분리

기존 이식 도구 `Tools/AssetMigration/PrepareOilRigMap.py`(10/04 삭제됨, Git 이력 참조; 현행 실행 안내 아님)의 Source Map은 `/Game/Liope_Tr/Maps/Overview`, Target은 `/Game/Drone/Maps/Lvl_OilRig`다. 이 처리에서 Vendor GameMode를 비우고 구형 FirstPerson Demo Door Actor 8개를 제거한 뒤 환경 의존성만 이식했다. Preview 전용 FirstPerson Map 체인은 중앙 OilRig 맵에 포함하지 않았다.

사용자 확인으로 실제 플레이 환경은 `Preview`임을 확정했다. 기존 검증본을 덮지 않고 다음과 같이 별도 이식했다.

1. 원본 `D:\JGY\project\Unreal_260821\OilRigLiope_Tr`를 별도 `OilRigPreviewStage`에 복사했다.
2. `Preview`를 `Lvl_OilRigPreview`로 복제하고 Vendor GameMode Override를 비웠다.
3. Sample Door Blueprint 32개가 FirstPerson 캐릭터·팔·입력을 끌어오므로, 문과 프레임 외형 64개는 동일 World Transform·Material의 `StaticMeshActor`로 보존하고 상호작용 Wrapper만 제거했다.
4. 재귀 의존 자산 614개를 `/Game/Drone/ThirdParty/OilRigPreview`로 이동했다.
5. 빈 StaticMeshActor 14개와 메시·Transform이 완전히 같은 중복 1개를 제거했다. 서로 다른 메시가 같은 위치를 공유하는 공급사 조립 구조는 유지했다.

| 항목 | 결과 |
|---|---|
| 실제 장면 Map | `/Game/Drone/Maps/Lvl_OilRigPreview` |
| ThirdParty 자산 | 614 `.uasset` |
| Map 포함 의존성 폐쇄 | 615 Package |
| 외부 `/Game` 참조 | 0 |
| 누락 참조 | 0 |
| Map load | 성공 |
| Map GameMode Override | `None` |
| Map Check | `0 errors / 0 warnings` |
| 신규 용량 | 4,082,822,021 bytes, 약 3.80GiB |
| 기존 Overview | `/Game/Drone/Maps/Lvl_OilRig` 그대로 보존 |

## 사용자가 확인할 일

1. Editor에서 /Game/Drone/Maps/Lvl_OilRigPreview만 연다. Bangkok 맵 확인 지시는 삭제로 종료했다.
2. Missing Material, 검은 Texture, 조명 과노출, 스케일·충돌 이상을 확인한다.
3. OilRig Preview의 문·문틀 32세트가 제 위치에 보이는지 확인한다. 현재 문은 외형/충돌만 있고 FirstPerson 상호작용은 의도적으로 제거됐다.
4. 첫 로드 시간과 대표 구간 FPS를 기록한다.
5. `Build > Map Check`를 다시 실행해 0/0을 화면에서도 확인한다.
6. GitHub Desktop에서 Bangkok/OilRig Preview 맵·ThirdParty 폴더·이식 도구·문서만 커밋할지 확인한다. 기존 `Lvl_DroneTutorialSystemsTest`와 `MetroMaintenanceStation` 변경은 별도 사용자 작업이다.
7. Bangkok 약 11.46GiB와 OilRig Preview 약 3.80GiB가 전부 Git LFS 업로드 대상이므로 Push 전에 현재 LFS 예산과 네트워크를 확인한다.

## 재현 도구

- `Tools/AssetMigration/PrepareBangkokCityMap.py`: 중앙 맵 복제와 GameMode 제거
- `Tools/AssetMigration/StageDependencyClosure.py`: 의존성 폐쇄 이동과 외부/누락 검사
- `Tools/AssetMigration/AuditBangkokCityMigration.py`: 본 프로젝트 Map load·참조·GameMode 감사
- `Tools/AssetMigration/PrepareOilRigPreviewMap.py`(10/04 삭제됨, Git 이력 참조; 현행 실행 안내 아님): Preview 복제, GameMode 제거, Door 외형 정적화
- `Tools/AssetMigration/StageDependencyClosure.py`: OilRig Preview 의존성 전용 경로 이동
- `Tools/AssetMigration/CleanOilRigPreviewMap.py`(10/04 삭제됨, Git 이력 참조; 현행 실행 안내 아님): 빈/완전 중복 StaticMeshActor 정리
- `Tools/AssetMigration/AuditOilRigPreviewMigration.py`: 본 프로젝트 Map load·참조·GameMode·Map Check 감사

스테이징 원본 복사본은 Git 대상이 아니며 본 프로젝트 실행에는 필요 없다.
