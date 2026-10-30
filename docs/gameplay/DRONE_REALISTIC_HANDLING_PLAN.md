# 현실 조종감 기준과 후속 개발 계획

기준: 2026-10-30 D PC. 정확한 파일럿 테스트맵에만 접촉·회전항력·착륙 보정을 추가한 현재 소스 기준이다. Build·자동/RHI·실물 확인 결과는 STATUS/WORKLOG를 따른다. 폭탄 SI 항력 수리·자동 검증과 기존 본체 경로를 아래에서 구분한다. 장치별 입력·Legacy OFF 항력/World중력 정책을 유지하고 FPV/Fiber의 자폭 감지와 하부 물리 충돌 범위를 분리했다. 자폭 센서·넓은 역할 카메라는 [역할 정본](DRONE_TYPES_AND_CONTROL_MODES.md), 실제 검증은 [WORKLOG](../history/DRONE_WORKLOG.md)를 따른다. controlledRacer opt-in·실기체 교정·본미션/B·C·손 조종·패키징의 기존 지원 한계는 유지한다.

모터 OFF에서도 공기저항은 적용된다. Legacy 정상OFF의 조기 분기에서 빠졌던 공유 공력 계산을 4모드에 연결하고 시작/목표추력0·World중력·기존 선형/제곱항력과 인공제동0을 유지했다. 항력계수를 강하게 조절한 수리가 아니다. 30/240fps의 수평 감속·10초 감속·낙하 중 수평감속/추력0/재시동과 LocalPlayerController+실제 World.Tick 이동이 자동 통과했다. 기본/게임의 ON assisted 구조는 유지하고 controlled candidate는 기존에도 OFF 항력을 계산했으므로 이번 Legacy 결함과 구분한다.

## 현재 운동·관성 계산식

전체 기체에 같은 강체 물리를 적용하지 않는다. 기본 본미션은 Legacy이며, 로터 후보의 관성텐서 적분은 controlled Racer·Acro Mode1/2에서만 사용한다. 키/패드/RC는 같은 모드의 물리식을 공유하되 스로틀의 절대값/중앙 hover·곡선·안전 가드가 다르다. Space/Ctrl 쉬운/게임은 별도 상승/착지 보조다.

| 경로 | 병진 운동 | 회전 |
|---|---|---|
| Legacy 쉬운/게임 ON | FloatingPawnMovement 입력 가속·자동 감속·상승 보조 | 조작 보조 회전 |
| Legacy Acro ON | 합산 추력/총질량·중력·선형/제곱 항력 | 목표 각속도 1차 응답, 관성텐서 미사용 |
| Legacy OFF | 추력0·World중력·공유 항력, 실제 지지면에서 마찰/정립 보조 | 로터 토크 적분 아님 |
| 파일럿 로터 후보 | 로터별 힘·상대 항력·중력·접촉 충격량/마찰 | 대각 관성·로터/접촉 토크·회전항력, 낮은 추력의 ON/OFF 접지 착륙 보조 |
| 전투 폭탄 | 실제 Payload 질량·중력·바람 상대 SI 제곱항력 | 텀블링·양력·회전 공력 미구현 |

### Legacy 추력·항력·회전

`m = m_dry + m_payload`, `T_target = u T_max`다. 모터 1차 응답은 `T_new = T_target + (T_old-T_target) exp(-dt/tau_m)`이며 가속도에는 프레임 구간 평균 추력 `T_mean`을 사용한다. `a = BodyUp * T_mean/m + g`이고 C++ 기본값은 건조2kg·최대합산40N·추력응답0.055초·ON 설정중력9.8m/s²다. 자산/BP 값이 우선하며 실기체 측정값은 아니다. OFF는 World중력을 읽고 추력을0으로 처리한다. 호버 출력은 `m*g/T_max`이고 적재 질량도 포함한다.

Legacy 회전은 `omega_new = omega_target + (omega_old-omega_target) exp(-dt/tau_r)`, `tau_r` 기본0.08초다. 프레임 회전량은 `omega_target*dt + (omega_old-omega_target)*tau_r*(1-exp(-dt/tau_r))`를 축각으로 적용한다. 이는 회전 관성처럼 반응을 지연시키는 근사이며 `J`나 모터별 토크를 계산한 것이 아니다.

Legacy 항력은 cm/s 속도에 `r = clamp(m_dry/m,0.05,1)`, 먼저 `v *= exp(-lambda*r*dt)`, 다음 `v += -k*r*|v|*v*dt`를 적용한다. 기본 `lambda=0.12/s`, `k=0.00004/cm`(SI 환산0.004/m)다. 이 경로의 항력은 Movement의 월드 속도를 사용하며 바람은 WeatherResponse의 별도 보간 위치 drift다. 후보처럼 상대 공기속도 하나로 결합한 모델은 아니다. 근거는 `DroneAcroFlightComponent.cpp:289,339,380`, `DroneWeatherResponseComponent.cpp:68,125`다.

Legacy의 정지 지지면·모터OFF 접선 속력은 `s_new=max(0,s-mu*max(0,-g dot n)*dt)`로 줄인다. 기본 마찰계수0.4·접촉여유0.5cm이며 실제 hit·정지 지지면·법선 등을 확인한다. 후보는 `GetMotorOffGroundSupport()`에서 제외되므로 이 마찰/정립 보정을 상속하지 않는다. 근거는 `DroneFlightPawn.cpp:628,664,684`다.

### 파일럿 로터 후보의 관성·공력

후보는 SI 단위(m, kg, s, N, Nm, rad)·몸체 FLU 좌표를 사용하며 UE cm/축 부호를 경계에서 변환한다. 로터마다 `F_i = T_i axis_i`, `tau_i = (r_i-r_CG) cross F_i - axis_i*spin_i*k_tau_i*T_i`를 합산한다. 각속도는 다음 강체 식을 실제 적분한다.

`omega_dot = J^-1 * (sum(tau_i) - C*omega - omega cross (J*omega))`

회전 항력 C는 파일럿 접촉 opt-in에서만 활성화하고 그 외에는0이다. 기존 토크/관성 적분과 별도 지수 half-step으로 감쇠한다.

`v_air_body = R^-1 * (v_world-wind)`이며 축별 항력은 `F_drag_j = -c_j*v_j - 0.5*rho*(CdA)_j*v_j*abs(v_j)`다. 병진 가속도는 `a_world = R*(sum(F_i)+F_drag)/m + g`다. 중간 시점 가속도/각속도를 구해 `p_new=p_old+v_old*dt+0.5*a_mid*dt^2`, `v_new=v_old+a_mid*dt`와 쿼터니언 자세를 갱신한다. 후보를 켜면 Legacy 이동/적분·별도 바람 drift를 중지해 중복 적용하지 않는다. 근거는 `DroneFlightDynamicsKernel.cpp:24,99,109,338`, `DroneFlightDynamicsMovementComponent.cpp:110`다.

합성 기본값은 `J=diag(0.05,0.05,0.05) kg m²`, X쿼드4로터·팔0.25m·각 최대추력25%·반작용계수0.01m다. `rho=1.225kg/m³`, 축별 `CdA=0.01306122449m²`, 선형항력 `c=0.24kg/s`, 각속도 제어 `P=0.625`, `I=D=0`, 토크상한 `(4,4,0.2)Nm`다. 질량/최대추력/모터응답은 기존 기체 설정에서 상속한다. 관성·형상·공력·제어이득은 실기체 질량분포나 풍동/비행 실측으로 교정하지 않았다. 기본2kg의 단축 직선운동에서 기존 항력 수준에 맞춘 비교값이며 Legacy의 벡터속력 항력과 후보의 축별 항력은 대각 운동에서 다르다. 근거는 `DroneRotorFlightSettings.h:61`, `.cpp:5,70`다.

계산 간격은 기본1/120초, 한 프레임 최대16회·누적 지연0.25초이며 초과 시간은 drop으로 기록한다. Chaos 강체 비행 백엔드는 없고 `ChaosCandidate`는 거부한다.

### 파일럿 시험용 Data Asset과 50% 호버

`/Game/Drone/TestData/DA_RotorPilot_PhysicsTuning`의 **Physical Flight Settings**가 정확한 파일럿맵의 유효 물리값 정본이다. Setup의 PhysicsTuning 참조가 이 자산을 읽으며 원래 Racer Definition/BP는 저장하지 않는다. 저장한 값을 반영하려면 PIE를 다시 시작하거나 모터 OFF에서8재시작/6·7 재선택한다. 기존 Setup Landing 필드는 직렬화 보존용이며 편집 위치는 이 Data Asset으로 옮겼다. 일반 미션/다른 맵은 기존 정책을 유지한다.

| 시험 시작값 | 값 | 조정 효과 |
|---|---|---|
| DryMassKilograms / MaximumTotalThrustNewtons | 0.9kg / 17.64N | 기본 World중력9.8에서 최대 추력/중량=2. 질량만 줄여 같은 비율을 유지하면 하강 가속도가 저절로 빨라지지는 않는다 |
| MotorResponseTimeSeconds | 0.035s | 추력 상태의 응답 지연 |
| RotorDynamics.InertiaDiagonalKilogramMetersSquared | (0.0225,0.0225,0.0225)kg·m² | 회전 관성. P=(0.28125), torque max=(1.8,1.8,0.09)Nm |
| 선형항력 / CdA / 회전항력 | (0.108,0.108,0.054)kg/s / 축별0.005877551m² / 축별0.01125Nm·s | 공중 속도·회전 감쇠 |
| GroundFrictionCoefficient / ContactRestitution | 0.4 / 0 | 마찰과 착지 반발. 공중 속도나 모터 상태를 착지 때 강제로 초기화하는 기능이 아니다 |
| PilotHover | Enabled, StickHover01=0.5, DescentExponent=1.5 | 스로틀50%를 실제 중량에 맞추고 그 아래 추력을 더 빨리 줄임 |
| 약한 호버 보정 | VerticalDampingPerSecond=0.2, StickAssistHalfWidth01=0.08, MaximumAssistWeightFraction=0.05 | 42~58% 안에서 중앙일수록 강함. 최대 중량5%의 수직속도 보정; 고도 기억/적분항 없음 |

키보드/패드는 기존 입력 정책에서 이미 물리 호버분율mg/Tmax로 중립을 변환하므로, 파일럿 어댑터는 이를 스틱 영역으로 되돌린 뒤 새 곡선에 한 번만 넣는다. RC 절대축은 되돌림 없이 그대로 쓴다. 예를 들어 질량1.2kg/최대17.64N이면 물리 호버분율은2/3이지만 중앙복귀 명령은 여전히 파일럿50%이며 실제 추력11.76N을 유지한다. GetCurrentAcroHoverThrottleNormalized의 물리분율 의미와 모터 시동/최하단 안전가드는 유지한다.

이 값들은 체감 조정용 합성 시작값이며 실기체 실측 사양이 아니다. 4/5는 Legacy 이동을 사용하고6/7만 아래의 로터 후보 호버 곡선/보정을 사용한다. 지원은 기존 무적재 Racer/CG0 범위다.

아래는 수평·무풍·회전 명령0·추력 포화 없음의 식이다. `u`는 RC 절대축0~1 또는 중앙복귀 장치의 곡선 처리 뒤 중립을s로 정규화한 명령, `s=0.5`, `h=mg/Tmax`이며 충분한 최대 추력이 있을 때 적용한다.

```text
u <= s: T_base = mg * (u/s)^1.5
u >  s: T_base = Tmax * [h + (1-h)*(u-s)/(1-s)]
w = clamp(1 - abs(u-s)/0.08, 0, 1)
deltaT = w * clamp(-m*0.2*v_z, -0.05*mg, +0.05*mg)
T_target = clamp(T_base + deltaT, 0, Tmax)
T_end = T_target + (T_start-T_target)*exp(-dt/0.035)
T_mean = T_target + (T_start-T_target)*0.035/dt*(1-exp(-dt/0.035))
a_world = R(q)*(sum(rotor_force_mean)+F_drag_body)/m + gravity_world
v_new = v_old + a_mid*dt
p_new = p_old + v_old*dt + 0.5*a_mid*dt^2
```

deltaT는 모터ON·공중·BodyUp.Z>0.7일 때만 작동한다. 모터OFF는 추력0과 실제 World중력/항력으로 낙하한다. 회전 명령이 있으면 로터별 배분/포화와 각 로터의 모터 응답이 먼저 적용된다. `m=0.9kg`에서50%는8.82N/가속도0,45%는약7.53N/하향1.43m/s²,40%는약6.31N/하향2.79m/s²다(항력·보정·추력 지연 전). 중력을 추가 배수하거나 가속도 항을 누적하지 않는다. 실제 속도에는 이전 관성이 남으며 지속적인 추력은 속도를 계속 바꾼다.

반복 이착륙 검사는 실제 Setup→saved Racer·World Tick으로30/120fps·6회 동일 입력을 실행한다. 시간 장부와 모터가 한 일 대비 에너지를 함께 검사하며, 기존 설정의 비정상 누적은 재현되지 않았다. 기존 restitution0.1에서는 착지 직후 상승속도와 두 번째 점프 높이 증가가 관측됐으며 새 시험값은 반발을0으로 둔다. 원시 비교·하강/약한보정 실측·중간 실패는 WORKLOG와 로컬 PilotMotionTuning_20261030이 정본이다. 실물 조종 느낌은 사용자 확인 대기다.

### 파일럿 맵의 접촉·회전·착륙 보정

이 보강은 정확한 `/Game/Drone/Maps/TestMap/Lvl_DroneRotorDynamicsPilot`의 Game/PIE World·controlled 표식·명시적 opt-in에서만 사용한다. 다른 맵에서는 설정 사본의 opt-in과 회전 항력을 강제로 끈다. 공유 설정 기본값은 OFF·마찰0·회전항력0·정립rate0이며 제품맵/DA/BP를 저장하지 않는다. 이 맵에서도4/5는 기존 Legacy,6/7은 보강된 로터 후보를 사용한다.

파일럿4~7은 `RotorDynamics.bEnablePilotBodyHull`로 보이는 본체에 맞춘 평평한 native 상자1개를 사용한다. 별도 시험용 PhysicsTuning의 기본값만 ON이고 공유 기본값/다른 맵은 OFF다. Racer의 본체 LOD0 실측은 Actor 기준 min `(-28.0562,-33.7186,0.07459)`, max `(28.0562,33.7187,35.4409)`cm, 크기 약56.1×67.4×35.4cm다. 별도 프로펠러 전체74.6×100cm를 판정에 포함하지 않는다. 상자 형상 중심만 Z≈17.7577cm이며 Actor/CG0·외형/카메라 상대변환은 유지한다. 원래 반경45cm 구는 밑면이−45cm여서 외형이 약45cm 뜨는 원인이었다. 출발 위치와 접지 검사는 구 반경 대신 실제 상자 밑면을 사용한다. 중립 외형으로 fit하므로 전환 직전의 시각 bank/shake를 고정 판정에 포함하지 않는다. 원래 메시/BP/DA와 작성 맵은 저장하지 않는다.

기존 Sphere 포인터/카메라·외형 연결은 비충돌 anchor로 보존한다. 파일럿4/5는 후보 적분만 해제하고 같은 Hull을 FloatingPawnMovement의 UpdatedComponent로 유지하므로4↔5↔6↔7 전환에서 판정 교체나45cm 높이 이동이 없다. 일반 해제/수명 종료에는 원래 루트·충돌 프로필·overlap·UpdatedComponent를 복원한다. 쉬운/게임의 원래 비행식·입력은 유지하고 Ctrl 접지OFF·모터OFF 마찰/정립·hit callback만 실제 active primitive와 native shape 검사로 연결한다. 접지한 모터OFF 외형만 잔류 시각 기울기를 중립으로 복귀시킨다. 별도 넓은 로터 probe는 이 Hull에서 사용하지 않고 본체 native 충돌을 사용한다. 회전 guard도4~7에 공유한다. `UDronePilotFloatingPawnMovement`는 같은 기존 컴포넌트 이름/UFloating API를 유지하며 이 맵의 offset Hull에서만 MTD 겹침 중심을 보정하고 다른 맵은 Super를 따른다. 본미션의 구형 판정은 유지한다.

6/7 커널의 접촉점 속도는 `v_contact = v_CG + omega_world cross r - v_surface`다. 새 상자는 native 충돌 시점의 외형 접점을 사용하며 바닥 네 모서리가 같은 평면에 실제 지지될 때만 평평한 지지 접점을 구성한다. 구형 opt-out의 접점은 `sphere_center - normal*실제반경`을 유지한다. UE 이동 pullback을 회전 팔에 더하지 않는다. 방향 d의 역유효질량은 `1/m + d dot ((I_world^-1*(r cross d)) cross r)`다. 법선 충격량 `Jn=-(1+e)*(v_contact dot n)/역유효질량(n)`으로 침투 방향 속도를 제거하고, 접선 충격량은 접점 미끄럼을 멈추는 양과 `mu*Jn` 중 작은 값으로 제한한다. 이 단계의 Jn에 중력 지지가 포함되므로 `m*g*dt`를 다시 더하지 않는다.4/5는 이 로터 커널로 전환하지 않고 기존 FloatingPawnMovement·모터OFF 접지 마찰/정립 계산을 유지한다.

충격 후 `v += impulse/m`, `omega_body += R^-1*(r cross impulse)/J`를 적용한다. 구형 중심의 순수 법선 충격은 회전을 만들지 않으며 접선 마찰이 회전 토크를 만든다. 상자에는 실제 형상의 접촉 팔/외곽 거리를 사용한다. native sweep·MTD·Slide를 유지하고 위치가 같은 회전도 상자 모서리 이동량을 나눠 겹침을 확인한다. 이는 CG0·단일 본체 상자와 제한된 평면 지지 모델이며 기체 전체 메시의 다점 강체 접촉이나 full Chaos 비행을 뜻하지 않는다. 질량·관성·공력·50% 호버·착륙 보조 계수는 별도 PhysicsTuning 값을 유지한다.

상자 후보의 병진 native sweep이 실제로 막힌 step에는 SI 속도도 같은 제약과 일치시킨다. 접점 충격 계산 뒤 남은 `v_rel=v_CG-v_surface`의 `dot(v_rel,n)<0` 성분만 `v_rel-=n*dot(v_rel,n)`으로 제거한다. 표면 기준 운동에너지가 늘지 않을 때만 적용하며 접선 속도·충돌 토크·모터 상태는 유지한다. 실제 병진 blocking hit가 없는 공중·회전만 막힌 경우에는 적용하지 않는다. 이는 모서리 접점의 회전 보상 속도와 회전을 별도로 막는 swept adapter의 차이를 맞추는 근사 제약이며 공력 계수 변경이 아니다.

회전 항력 토크는 `tau_drag=-C*omega_body`다. 커널은 `omega *= exp(-(C/J)*dt/2)`를 기존 토크/관성 적분의 앞뒤에 적용해 계수가 커도 감쇠 자체가 에너지를 늘리지 않도록 한다. 현재 시험DA의 C는 축별0.01125Nm·s다. 다른 맵과 opt-in OFF는 C=0으로 기존 경로를 유지한다.

자연 착륙 보정은 `NaturalLandingAssist.bEnabled`가 켜진 파일럿6/7 후보에서 사용한다. 최근 실제 blocking hit와 같은 정지 지지면을 native pullback 여유 안에서 계속 확인한다. 모터 ON/OFF 모두 **요청 추력과 실제 추력이 각각 중량의94% 이하**일 때 진입하며, 진입 후에는99% 초과 시 즉시 해제한다. 최초 실제 바닥 충돌 전의 접선 속도와 `|omega|*외곽거리`는 각각3m/s 이하, 기체 위쪽/지지법선 내적은0.1 초과여야 한다. 이 적격 첫 접촉의 기수 방향을 기억하며 같은 지지면/유효시간 내에 상자 모서리 충격이 만든 회전은 실제 접지에서만 감쇠한다. 실제 충돌 시각과 기억을 위한 같은 바닥 native 관측 시각은 별도이며, 이미 실제 접촉으로 시작한 기억만 같은 면·변환·법선·Up·현재 명령 조건에서 새 관측으로 갱신한다. 매 step의 실제 지지·명령/추력·Up·접선 속도 제한은 계속 확인한다. 물리 속도가 잠시 상한을 넘으면 힘·자세·지원 시간 가산은 계속 거부하되 이미 적격인 방향 기억만 유효시간 안에서 보존한다. 지지면으로부터 상향 분리 속도가0.15m/s를 넘거나 각축 회전 목표가20°/s를 넘으면 보정을 먼저 해제한다. 새 이륙 명령은 모터 응답 지연을 기다리지 않고 요청 추력으로 즉시 판단한다.

실제 접지 직후 각속도는 `exp(-24*dt)`, 접선 속도는 `exp(-6*dt)`로 감쇠해 구르며 뒤집히는 것을 줄인다. 자세는 실제 지지0.08초 확인 뒤0.2초 동안 `ramp=x*x*(3-2*x)`로 보정 강도를 올리고 `alpha=1-exp(-6*ramp*dt)`의 quaternion Slerp로 지지면에 정렬한다. 최초 적격 바닥 hit의 heading을 보존하고 모터 ON 상태·요청 collective를 유지한다. 같은 정지 지지면의 짧은 반동/초기 중첩에는0.25초의 기존 면·변환·Up·현재 입력/추력 조건 안에서 방향과 이미 실제 지지로 쌓은 시간을 보존한다. 실제 지원이 없는 동안은 active·감쇠·자세 보정과 시간 가산을 멈춘다. 상자 후보의 지지 시간은 이 짧은 틈에서 일시정지하고 구형 opt-out은 기존 연속 확인을 유지한다. 다른 지지면/벽/천장·강한 입력·오래 떠 있음·뒤집힘에는 기억과 시간을 폐기한다. 자연 보조 OFF의 기존 최근지지 기한0.1초는 유지한다. 활성 중에는 제어기의 오래된 I/D 상태만 비워 충돌을 줄인다. 공중3cm 근접·벽/천장·뒤집힘·고추력/강한 회전 의도·동력상실/파괴는 보정 대상이 아니며, 위치를 지면으로 당기거나 모터를 자동 OFF하지 않는다. 이는 물리 충격량과 구분되는 명시적 게임 보조이며 실기체 교정값은 아니다. 자연 보조를 끈 수동 opt-in의 기존 OFF/0.5m/s 착륙 경로는 유지한다.

현재 파일럿의 접촉·착륙 계수는 위 별도 PhysicsTuning 자산의 RotorDynamics에서 편집한다. NaturalLandingAssist의 Enabled/Enter0.94/Exit0.99/MaximumBodyRateCommand20°/s/SupportConfirmation0.08s/BlendIn0.2s/AngularSettling24/s/MaximumUpwardSeparation0.15m/s와 UprightLandingAlignmentRate6/s/MaximumSpeed3m/s/MinimumUpDot0.1을 사용한다. 공유 기본값은 OFF/수치0이며 다른 맵에서는 자연 보조와 PilotHover를 강제로 끈다. 접근속도 편집/검증 상한은5m/s다. 기존 DA/BP·맵은 자동 저장하지 않는다.

### 전투 폭탄

폭탄은 `v_air=(v_world-wind)`를 m/s로 바꿔 `F_drag=-0.5*rho*Cd*A*|v_air|*v_air`, `a_drag=F_drag/m_payload`를 계산한다. 기본 `rho=1.225`, `Cd=1`, `A=0.005m²`이며 실제 Payload 질량을 사용한다. 반 단계 중력→`v_air/(1+k*|v_air|*dt)` 해석 감쇠→반 단계 중력으로 갱신하고 swept 충돌을 유지한다. 회전/텀블링/양력과 실측 탄도 교정은 없다. 근거는 `DroneBombMovementComponent.cpp:38,48`다.

## 현재 적용 경로와 투하물

기체와 투하물은 별도 운동 경로다. 아래는 현재 Source와 실제 saved Drop 런타임 조회를 기준으로 한다. 폭탄 SI 항력은 실제 World/Projectile 30·120fps·단위/바람·고속 비교를 자동 검증했으며, 손조종 완료를 의미하지 않는다.

| 대상/상태 | 현재 계산 | 경계 |
|---|---|---|
| Legacy Acro Mode1/2 ON | 합산 추력/총질량·중력·1차 모터 응답·선형+속도제곱 항력·각속도 응답 | 관성 텐서/로터별 토크의 완전한 강체 모델은 아님 |
| Legacy 쉬운/게임 ON | FloatingPawnMovement의 가속·감속/상승하강 보조 | Acro 힘 적분과 다른 조작 보조 모델 |
| Legacy 정상 모터 OFF4모드 | 추력0·World중력·공유 선형/속도제곱 항력 | 지면 접촉 마찰과 공중 항력을 구분 |
| 전투 폭탄 수리 소스 | swept ProjectileMovement·World중력×1·기체 속도+하향3m/s·상대 공기속도 SI 제곱항력 | 30m/s 상한 제거/최대1/120초 substep. 30/120fps 감속/거리/에너지 소산·질량 차이 검증. 회전/양력/실측 형상 공력 모형은 아님 |
| opt-in Racer 후보 | 상대 공기속도·SI 항력·로터 힘/토크·대각관성 | 일반 Drop과 기본 본미션의 현재 백엔드가 아님 |

실제 saved Drop 조회는 건조2kg+적재0.75kg=2.75kg, 최대 합산추력40N·모터 응답0.055초·World 중력9.8m/s², 기본 선형0.12/s·제곱0.00004/cm다. Legacy Acro는 두 항력에 dry/total mass 비(적재 시2/2.75)를 곱하고 선형은 지수 감쇠, 제곱항은 가속도로 적분한다. 실제 기체의 Cd·면적을 검교정한 값은 아니다. 쉬운/게임 ON의 감속도는 조회된 현재 기본 모드에서1818.18cm/s²이며 별도 보조 계산이다. 지면 마찰은 모터OFF·실제 정지 지지면 접촉을 확인한 때만 작용하고 C++ 기본 마찰계수0.4·접촉 허용0.5cm를 사용한다. 땅에 닿지 않은 상태의 감속은 항력이 담당한다. 앞선 투하/피해/교대 검증은 공중 감속 검증을 포함하지 않았다. 검증 날짜·수선 경과는 [WORKLOG](../history/DRONE_WORKLOG.md)에 기록한다.

### 폭탄 항력과 조정 위치

`UDroneBombMovementComponent`는 `v_air=(v_world-wind)/100`(m/s), `F=-0.5*rho*Cd*A*|v_air|*v_air`(N), `a=F/m`를 사용한다. 실제 투하물 질량을 읽으며 Weather snapshot 바람은 상대속도에 한 번만 사용한다. 반중력/지면 마찰로 공중 감속을 대신하지 않는다. 반 단계 중력→해석적 제곱항 감쇠→반 단계 중력으로 적분하고 UE native swept 충돌을 유지한다.

기본 rho=1.225kg/m³·Cd=1·기준면적0.005m²(50cm²)는 실측이 없는 게임 시작값이다. 커진 표시용 메시의 크기를 실물 공력 면적으로 간주하지 않는다. 폭탄 Movement의 `Drone|Bomb|Aerodynamics` 속성에서 조정하며, 질량은 실제 Payload 질량이다. 배송 화물은 기존 ProjectileMovement·수직 투하·마찰을 유지한다. 실제 0.75kg 폭탄의 수평속도12→10.43777m/s·수평거리22.57548m(2초)를30/120fps에서 확인했다. 같은 형상1.5kg은11.17140m/s·23.25984m로 더 멀리 간다. 지면 접촉/속도 상한 없는 측정이며 자세·회전·양력까지 실기체로 검교정한 결과는 아니다. [실행 근거](../history/DRONE_WORKLOG.md)를 따른다.

## Racer 로터 1차 후보

`/Game/Drone/Maps/TestMap/Lvl_DroneRotorDynamicsPilot`을 열고 Play한다. 새 전용 맵의 DroneRotorControlledTest tag와 Setup이 기존 saved `DA_Drone_Racer_Greybox`의 PawnClass/Definition을 읽어 메모리에서만 Acro Mode2·FixedStepCandidate로 진입시킨다. 시작은 motor OFF다. 원래 DA/BP와 제품맵은 opt-in으로 저장하지 않는다.

이 맵의 숫자열 시점/모드/날씨 단축키는 [입력 정본](../tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md#파일럿-테스트맵-전용-숫자키)을 따른다.4/5는 Legacy 쉬운/게임으로 이동하고6/7만 로터 후보를 사용하므로 같은 맵의 모든 모드가 같은 물리 계산을 쓰는 것은 아니다.

| 항목 | 현재 지원·구분 |
|---|---|
| 백엔드/기체 | Legacy가 기본. Racer1종의 명시 opt-in FixedStepCandidate·Acro Mode1/2만 지원 |
| 월드/무게중심 | 명시 controlled tag·CG0·외부pose writer 없음. 활성 altitude manager가 있거나 net rig/observer lesson이 존재하는 World는 진입 거부 |
| 운동 | 로터별 힘/반작용토크·대각관성·rate 제어/배분/포화·THRUST 지연·중력/상대공기속도 항력을 공유 SI커널로 계산 |
| 단독 writer/시간 | 후보 이동소유자1개. Legacy Floating/Acro 적분·수직clamp·Weather 별도drift를 중복적용하지 않음. bounded fixed-step의 성공step/pose commit·pending/drop을 기록, hold/pause는 진행하지 않음 |
| 접촉/모터 | 구 swept 이동·normal 속도투영·support slop의 후보 근사접촉. 자동 시동/OFF·무추력 중력·실접지·재이륙. 무장 ArmSwitch·방전·사망과 구분 |
| 가상 계수 | 원래saved Racer는2kg/40N/tau0.055, 현재 파일럿은별도DA0.9kg/17.64N/tau0.035. geometry/inertia/drag/gains와시험값은synthetic이며실기체채택사양아님 |

<a id="자동-스로틀-모터-정책과-검증-범위"></a>

현재 Source를 반영한 DLL로 실행해야 하며, 소스의 단축키 추가와 실행 파일 반영 여부는 별도로 확인한다. Space 새 입력 시동/상승·CtrlOFF·해제hover와 RC/패드 안전정책은 [입력 정본](../tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md#space키-자동-시동off-정책)을 따른다. 후보맵과 기본 Legacy 정책은 보존한다.

Acro의 hover/가속은 같은 중력 helper를 사용한다. Legacy는 설정 중력, candidate는 World 중력이며 live hover를 장치별 출력에 반영한다. Legacy 모터1차응답은 프레임 끝 추력 대신 구간평균 추력으로 가속을 계산해 응답의 FPS 차이를 줄였다. 최종 LegacyResponseFrameParity와 candidate 실제 Tick 경로 비교가 통과했다. Legacy drag/position 전체 적분 또는 모든 backend를 재작성한 것은 아니다.

쉬운/게임 조작은 기존 FloatingPawnMovement의 climb/속도 보조다. hover는 입력 중립 기준이며 전체 기체의 힘/질량/중력 물리를 통일했다는 뜻이 아니다. 후보 커널은 구성 시 질량/geometry를 캐시하고 live payload·물리설정 변경 시 재구성하지 않으므로 지원 밖 확장에 주의한다. 현재 controlledRacer 무적재/CG0 범위를 유지한다. 실제 key/axis·saved 역할·중력/추력·카메라 변환 자동 검증과 실물 손조작·전체미션 Pass를 구분한다.

별도 ChaosContactComparison은 실제 sphere body 질량2kg·대각관성0.05kgm² 재조회·solver 진행0.100000005초/마지막dt0.008333334초·힘가속/바닥정착을 확인한 최소 비교다. full Chaos flight callback/backend를 설치한 것이 아니며 `ChaosCandidate`는 명시거부한다. 확장B/ChaosC의 최종채택·실기체교정·payload/비영CG·일반강체/로터충돌·고속추락·제품미션 altitude/net/observer 호환·전기체전환·손조종/숙련자 평가·패키징은 미완료다.

## 확정한 방향과 아직 정하지 않은 것

|구분|현재 결정|후속 결정에 미치는 영향|
|---|---|---|
|Racer|실제 레이싱 드론을 참조한다|레이싱에서의 입력 반응·선회·스로틀 보정·FPV 시야를 비교한다|
|Scout·Drop·FPVStrike·FiberOptic|전쟁에 사용되는 기체를 역할별로 참조한다|정찰·운반/투하·FPV·유선 역할의 질량·적재·제어·카메라 차이를 조사한다. 모든 기체를 같은 FPV Rate로 통일하지 않는다|
|GroundUGV|공중 기체와 구분한 지상 모델을 유지한다|주행·접지·조향을 별도로 검증한다|
|실기체 모델·정확한 사양|미정|질량·추력·관성·배터리·로터 수치를 이름만 보고 정하지 않는다|
|주 제어 모드·Rates/스로틀 설정|미정|Mode1/2 축 배치와 Rate/Angle/고도·위치 보조를 구분해 정한다|
|사용·검증 장치|일반 게임패드와 InterLink DX 모두|두 장치를 따로 검증한다. InterLink 카메라 상하의 축/버튼 배정·보정 정책은 미정이며 새 배정 승인이 아니다|
|비행 로그·영상·숙련자 평가|자료와 평가 가능 여부 미정|자료 확보 전에는 일반 모델/수치 검증과 실기체 일치 판정을 구분한다|
|최종 물리 구조|확장 B와 Chaos C 모두 미확정|참조 응답·회전 관성/포화·접촉 요구와 성능을 비교한 뒤 선택한다|

참조 종류만 확정된 상태다. 특정 제품 채택·실제 제어 모드·현실감 합격 기준까지 결정된 것은 아니다. 장거리 타격 후보의 플레이 기체 구현도 이번 계획에 포함해 완료 처리하지 않는다.

## 현재 구현에서 출발할 부분과 한계

Legacy 기본 구조는 [역할·조작 가이드](DRONE_TYPES_AND_CONTROL_MODES.md)를 따른다. 아래 기본/게임·Legacy Acro 한계는 기존 모델에 대한 정적 조사이며 위 opt-in 로터후보와 구분한다. 여섯 DA 수치의 이전 C PC 조회를 전기체 실사양으로 쓰지 않는다. 원래 Racer의2kg/40N/tau0.055와 현재 파일럿 전용DA의0.9kg/17.64N/tau0.035를 구분한다.

|부분|현재 확인|현실 조종감 검증에서 필요한 구분|
|---|---|---|
|기본/게임 조작|UFloatingPawnMovement에 이동 입력을 주며 기울기 표현·감속 계수가 다르다|기체 자세가 로터 추력의 방향을 바꿔 가속하는 구조와 동일하지 않다|
|Acro|추력·질량·중력·모터 응답·항력을 계산하고 각속도 응답을 적분한다|각속도 1차 응답과 직접 자세 회전은 관성 텐서·유한 토크·모터 배분/포화를 계산하는 모델과 다르다|
|기체 프로파일|이전C PC의6개DA 공통2kg/40N 일부값·BP override 꺼짐, 원래Racer2kg/40N·파일럿전용DA0.9kg/17.64N 구분|synthetic 가상값과 실사양을 구분하고 나머지기체 런타임/UGV 공중추력 적용을 추정하지 않음|
|바람·항력|Acro 속도/항력과 WeatherResponse의 별도 AddActorWorldOffset Drift가 나뉜다|Movement 속도·위치 차분·바람을 함께 계측하고 새 상대 공기속도 공력과 기존 위치 이동을 중복 적용하지 않는다|
|배터리·적재|시간 기반 배터리와 적재 질량 반영은 있다|전압 강하·가용 출력·적재 위치/무게중심·회전 관성은 별도 범위다|
|접촉|몸체/로터 충돌 검사·반사·시각 회전 반응이 있다|충돌이 없는 것이 아니라, 접촉 충격량이 실제 각속도에 미치는 강체 회전과 구분해야 한다|
|모터/접지 상태|사람 조종 Legacy와 opt-in Racer에 자동 시동/OFF·무추력 중력·정상 착지/재이륙 구현·자동검증|중립호버와 OFF·공격 ArmSwitch·배터리 fault/파손을 분리. AI/UGV 기존 모델·실물 채널 미추가 유지|

UFloatingPawnMovement는 속도·가속 제한을 제공하지만 자체 중력은 구현하지 않는다. 프로젝트 Acro가 더한 중력과 엔진 기본 이동 기능을 혼동하지 않는다. [Epic 공식 API](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/UFloatingPawnMovement)

Legacy 제동값의 정지 시간/거리는 조건부 예측이다. 실제 입력·풍속·적재·모드 계측 전 사용자 관성을 재현한 값으로 쓰지 않는다. 위1차후보 자동검증도 실기체 현실감/숙련자 합격 완료가 아니다.

## 권장 접근과 B/C 선택 기준

추천 순서는 **참조 조건과 입력/화면 기준 확보 → 한 기체의 응답 계측 → 모델 한계 확인 → 구조 선택**이다. 먼저 제동 수치만 올리거나 엔진 물리 옵션만 켜는 방식으로 현실감 달성을 선언하지 않는다.

|후보|유효한 범위|결정 전에 확인할 비용·한계|
|---|---|---|
|현재 B의 단순 보정|범위를 좁힌 정상 비행의 평균 응답을 비교하는 기준|각속도 1차 응답만으로 회전 관성·포화·적재 위치·접촉을 일관되게 설명할 수 있는지 제한이 있다|
|확장 B: 직접 강체 계산 + 제어/구동 모델|질량·관성·힘/토크·모터 한계·바람을 계산하는 자유 비행 후보|접지·마찰·복잡한 접촉을 직접 구현할 비용과 기존 코드 재사용 이점을 비교한다|
|C: Chaos 강체 + 같은 제어/구동 모델|회전·접촉·마찰·충격과 동적 물체 상호작용 활용 후보|기체 계수·모터·제어기·공력은 여전히 필요하다. 이동/테더/충돌 이관과 실제 맵 CPU·프레임 비용을 측정한다|

B/C는 보정 입력→같은 제어기→모터 배분/포화→모터 응답→힘/토크를 공통 조건으로 두고 비교한다. 로터별 구동 모델과 Chaos 사용은 별개의 선택이다. 로터 4개를 그렸거나 Chaos를 사용한다는 사실만으로 현실감을 판정하지 않는다. 서브스텝도 안정성과 CPU 비용을 함께 보며, 임의 Actor Tick이 엔진 물리와 자동으로 같은 간격에 실행된다고 가정하지 않는다. [Epic Physics Sub-Stepping](https://dev.epicgames.com/documentation/en-us/unreal-engine/physics-sub-stepping-in-unreal-engine)

공통 기체 물리 위에 실제 제어 방식의 목표를 구분한다. Rate/Acro는 각속도와 수동 출력을 명령하고 스틱 중립이 자동 수평·위치 정지를 뜻하지 않는다. Angle의 자세 복원, 고도 보조, 위치/속도 보조도 서로 다른 기능이다. 기본/게임이라는 현재 UI 이름에 자동 정지·관성 정도를 임의로 배정하지 않는다. Mode1/2는 축 배치 차이로 유지한다. [PX4 v1.16 Acro](https://docs.px4.io/v1.16/en/flight_modes_mc/acro), [제어 구조](https://docs.px4.io/v1.16/en/flight_stack/controller_diagrams)

## 59번 구현안 검토와 선행 계약

사용자 제공 `59_드론물리_기반데이터_구현안_20261022.md`는 설계참고이며 원문의 구현/담당지시 자체를 승인으로 보지 않는다. 이후 사용자의 직접 구현 요청 범위로 Racer1 opt-in 후보를 작성·검증했다. 기존Definition/FlightProfile·입력API/ID/저장 구조를 재사용하되 실사양/계수·최종확장B/ChaosC 채택은 여전히 미정이다.

- **시간/callback:** 자체 고정 accumulator·Chaos 가변 substep·fixed async를 구분한다. 실제 callback의 dt/SimTime·입력 timestamp·wall/game/physics 시계·catch-up/drop 정책과 배터리/랩/카운트다운의 시간을 먼저 정한다. 120/240Hz·8step은 비교 후보이며 확정 주기/한도가 아니다.
- **단위·CG·관성:** World/Body/주관성축·원점·deg/rad·좌표 부호와 SI→엔진 변환을 계약한다. COM offset을 절대 CG setter로, 관성 getter를 tensor 적용 API로 취급하지 않는다. 적용/재조회와 단위 힘·토크 검사를 준비하고 힘/중력·위치/자세 작성의 중복을 막는다.
- **기존 자산 이행:** 모델/스키마 버전 또는 명시적 opt-in과 조건부 검증을 둔다. 새 로터/관성 필드를 즉시 필수화해 기존 DA/BP의 출격·Preview·재출격을 막지 않는다. enum 숫자·Mission/Drone ID·저장 키·BP override/API를 보존한다.
- **계수 채택:** 60N과 제안 질량 조합·관성/CG·공력·모터/전압 계수·현수 길이·합격 오차는 채택 보류다. 표본의 제조사 값·합성 시험값·현재 가상값을 분리한다. 현재 합산 추력 상태의 지연을 같은 수치의 RPM 지연으로 옮겨 같은 응답이라고 보지 않으며 전압/전류/RPM/추력 모델을 닫고 sag를 중복 적용하지 않는다.
- **고정/현수 화물:** 고정 anchor·작은 진폭의 진자 기준과 움직이는 기체-화물 결합 검사를 분리한다. 별도 화물 질량을 기체에 중복 합산하지 않고 slack/인장 전용·기체 반력·해제 시 위치/선속도/각속도 이행을 정한다.

Legacy 회귀 기대값과 이관/조건부검증을 보존하고 신규커널5·pilot6·프로필1 및 기존회귀11을 Run003에서 확인했다. 과거59 정적조사와 이번실행의 실패/수선·계측·소스보존은 [WORKLOG](../history/DRONE_WORKLOG.md)와 `Saved/Automation/PhysicsImplementation_20261022`가 정본이다. 최소Chaos접촉 통과로 fullflight backend/실기체일치/B·C채택을 선언하지 않는다.

## 잔여 작업과 완료 기준

아래는 착수 순서와 검증 범위의 제안이다. 조사 완료를 각 기능의 구현 완료로 바꾸지 않는다.

|작업|현재 상태|다음 작업|완료를 판단할 근거|
|---|---|---|---|
|참조 기체·입력 계약|기체 종류 방향과 일반 패드·InterLink DX 두 검증 대상 확정, InterLink 카메라 상하 추가 축/버튼 배정·보정 미정. 기존45매핑/비행4축·Mode1/2 보존|역할별 후보 중 첫 참조 기체/제어 모드·조종기·Rates/expo·스로틀·FPV 조건을 정리|참조와 미정 항목, 재현 가능한 장치/프로파일 기록|
|현실적인 비행 물리|Racer1 opt-in FixedStepCandidate 구현·신규12/회귀11 Success, controlledMap/Acro1·2/CG0|payload/외부writer·실기체참조/장치/숙련자 검증·동일조건B/C비교|힘/토크/시간/실접지 실제계측과 회귀·한계·실기체반복과제 구분|
|화면 상하 시야·감도|쉬운/게임 조작의 감도X/Y·반전·UI/저장 구현, D PC 지정 자동 검사와 PNG 검토 확인 범위는 [설정 가이드](DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#카메라-감도반전과-designer) 참조|두 장치의 원시 축→Input Action→모드→SpringArm→최종 ViewTarget 계측. InterLink 상하 배정은 미정|실물 장치별 양방향/해제·적용/취소/기본값·실제 재실행/구버전 저장 복원. 자동 입력·메모리 직렬화와 구분|
|모터 OFF·착지·재이륙|사람 조종 Legacy의 정상OFF·공중OFF/항력/중력과 Racer 저장맵 재이륙 생명주기 자동검증|실물 RC/XInput·화면·경사/고속충돌·전체 본미션 조건은 후속|자동 simulated 입력과 실장치·미션별 반복기록 구분|
|LOS 사람 후퇴·드론 보기|후퇴/추적 구현·4단계 자동 계약 통과, 사람/드론 가시성 미확정|검사 World/LocalPlayer 연결 캡처·HitResult 디코더 수리 후 지면/가시성 확인|실제 TUT_LOS에서 사람 메시/카메라가 드론을 보고 과도한 Pitch/Roll 없이 가시성 확보|
|M3·M4 오브젝트/목표|M3 현행 목표·M4 실제3지점/UGV접지·3목표 자동 통과. 자동 피해 이벤트이며 손 조종/발사 아님|실물 플레이·M4 공중 기체 높이·최종 출발 위치/안전성·시나리오 보완|실제 맵의 진행/실패/성공·장치 입력, World 일치 화면과 구분 기록|
|본미션 렉|1280×720·품질3·출발점 무입력10초 CPU 계측 확보, 전체 플레이/GPU 미검증|M3 Fence BP 오류·CSV ensure와 M4 Lumen 경고를 분리 조사. 같은 입력/비행/사격 구간 계측|변경 전후 같은 과제 p50/p95·최대 지연·GPU 지원 확인. 진단 우회는 최적화 근거 아님|
|본미션 로딩|M3/M4 요청→선택→조작과 엔진 LoadMap 구간 확보, 수치는 WORKLOG|같은 PC/옵션·cold/warm/순서·입력 과제로 반복 비교|구간별 시간과 반복 편차. 프로세스 전체/캡처 대기를 로딩/FPS로 쓰지 않음|
|사진·실물 입력 회귀|M1 조망/DROP·M2 차량 상세 연결, UI 검사 통과|M2 도로와 차량 대표·M3 재밍 외형/진입이탈·M4 전체/출발3곳 보완|사진 메타데이터/맵·대상 일치와 실제 키보드/패드 플레이. M3 흰 원반은 graybox이며 최종 레이더 외형 아님|

공중 모터 OFF·일반 착지는 배터리 소진/파손 경로와 구분한다. 사람 조종 Legacy와 opt-in Racer의 자동 시동/OFF·착지/재이륙은 구현·자동검증됐으며 실물 장치·경사/고속충돌·전체 본미션 확대는 후속이다. 일반 카메라 피치/고도 입력과 FPV/Fiber1인칭 쉬운/게임의 [전용 조준 보조](DRONE_TYPES_AND_CONTROL_MODES.md#fpv광섬유의-쉬운게임-조작-조준)를 구분한다.

## 변경 책임과 구현 전 계약

|담당 클래스/자산|다룰 책임|변경 전 맞출 계약|
|---|---|---|
|DroneFlightPawn·입력 IMC|입력 해석·모드·기체/카메라 명령 분리|장치 범위·중립 의미·축 배치·시점 전환·기존 Blueprint API|
|DroneAcroFlightComponent·이동/충돌 담당|힘·각속도/토크·적분·접촉을 적용하는 경로|위치/자세/속도의 단일 소유 경로, 바람과 호출 순서, 제한된 계산 간격|
|DroneDefinition·FlightProfile·Pawn BP|기체별 값과 자산 override|질량·추력·관성/무게중심·응답·항력의 단위/출처·적재 조건, 원본 백업|
|WeatherResponse|날씨 바람 전달|상대 공기속도와 위치 이동의 일관성|
|SettingsWidget·설정 Subsystem|카메라 감도/반전과 저장|UI/백엔드 소유 파일 조율, 적용/취소/기본값/기존 저장 호환|
|GroundDrive·LOS|UGV 주행과 관찰자 시야|공중 모델과 구분, 실제 TUT_LOS/UGV 맵 회귀|

기존 enum 숫자·Mission/Drone ID·저장 키·팀원 원본은 유지한다. 조정값은 Blueprint/Data Asset에서 바꿀 수 있게 하되, 실제 사양을 확보하기 전에 임의 수치를 확정하지 않는다. 생산 코드·자산 변경은 [세션 소유권](../git/DRONE_WORK_PC_SESSIONS.md)의 실행/카메라 담당이 범위를 맞춘 뒤 수행한다.

## 검증 단계

1. **참조와 입력/화면 기준:** 장치 min/center/max·갱신 간격·deadband·Rates/expo·스로틀·FPV 장착각/FOV를 기록한다. USB 입력부터 카메라/렌더까지 지연을 나눠 본다.
2. **한 기체의 정상 비행:** 같은 무적재/실제 적재·전압·무풍/바람 조건에서 호버·상승/하강·완만한 선회와 작은 각속도 입력을 비교한다.
3. **모델 한계와 구조 선택:** 저/중/고 출력의 반전·포화/복구·적재 위치·모터 OFF/접지에서 남는 오차를 확인해 확장 B/C를 선택한다. CPU·프레임·메모리 비용도 같은 맵에서 비교한다.
4. **숙련자 평가:** 같은 조종기/카메라와 과제로 입력 보정량·오버슈트·시간·주관적 차이를 함께 기록한다. 보정에 쓴 기동과 검증용 기동을 구분한다.
5. **실맵 회귀:** Physics Sandbox의 분리 시험 뒤 실제 본미션·TUT_LOS·팀원 레이싱 맵1·2·3·UGV에서 확인한다. 다른 맵의 통과로 대신하지 않는다.

합격 오차는 참조 반복 편차와 로그 해상도를 확인한 뒤 정한다. 프레임별 수치 차이·가상 호버 기준만으로 ‘실제 조종자 이질감 거의 없음’을 확정하지 않는다. 새 실제 비행을 요구하기보다 이미 보유한 로그/영상·제조사/제어기 자료부터 활용한다.

엔진은 본미션/LOS/성능 실행 세션 하나만 사용한다. 읽기6GiB/UI RHI10GiB/실출격12GiB/Camp 일반20GiB·승인된 저메모리 모드16GiB 시작 여유와 실행 중 RAM·commit 각각4GiB 보호를 유지한다. 미달이면 같은 조건 반복이나 사용자 앱 강제 종료를 하지 않는다. Production Training 원본을 시험 저장하지 않으며, 10분 초과 패키징/전체 쿠킹/DDC 작업은 실행 시점을 먼저 확인한다.

현재 UI·M1 출격 상태와 PC별 실행 수치의 정본은 [STATUS](../../STATUS.md)·[WORKLOG](../history/DRONE_WORKLOG.md)다. 새 RHI 검사 통과는 물리 입력·미션 완료·패키징·숙련자 평가의 완료가 아니다. 실행 순서는 [WORKBOARD](../../WORKBOARD.md), 현재 화면/출발·목표 확인은 [시험 가이드](DRONE_TEST_MAP_GUIDE.md)를 따른다.
