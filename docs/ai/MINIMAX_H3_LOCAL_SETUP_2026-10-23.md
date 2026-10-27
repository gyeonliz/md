# MiniMax H3 로컬 설치·실행 가이드 (D PC)

작성 2026-10-23, 작업 도구 Claude. 날짜별 테스트 수치는 `docs/history/DRONE_WORKLOG.md`의 "2026-10-23 D PC — MiniMax H3 로컬 설치·T2V 테스트" 절에 있다.

## 무엇인가

- MiniMax H3 = 2026-07-31 공개된 MiniMax의 옴니모달 **영상 생성 모델**(Hailuo 3.0). 텍스트·이미지·영상·오디오 입력 → 최대 15초 2K 영상 + 스테레오 오디오.
- D PC(RTX A4000 16GB, RAM 64GB)에 ComfyUI 포터블 v0.42.1 + 공식 ComfyUI 배포 가중치(`Comfy-Org/MiniMax-H3`)로 T2V 생성이 동작함을 확인했다(2026-10-23).

## 라이선스 주의 (사용자 결정 사항)

- MiniMax H3 Community License(2026-08-02)는 **대한민국을 Excluded Territory**로 지정한다. 한국 내 가중치 사용·복제·배포는 라이선스상 허가되지 않으며, 별도 라이선스는 MiniMax에 요청해야 한다(api@minimax.io).
- 2026-10-23 사용자에게 API/로컬/중단 선택지를 제시했고, 사용자가 **개인 실험 목적 로컬 설치**를 선택했다. 상업적 사용·배포·공개 산출물에는 쓰지 않는다.
- 그 외 조건: 연매출 2천만 달러 이상 상업 제품은 사전 허가, 출력물로 다른 AI 모델 개선 금지, 상업 제품 UI에 "MiniMax H3" 표시.
- 라이선스 범위를 벗어나는 용도는 MiniMax API(platform.minimax.io, 모델 ID `MiniMax-H3`, 2K 초당 $0.13) 또는 ComfyUI API 노드를 쓴다.

## 설치 구성

| 항목 | 경로 / 값 |
|---|---|
| ComfyUI 포터블 | `D:\JGY\ai\ComfyUI_windows_portable` (v0.42.1, Python 3.13.14, torch 2.14.0+cu130) |
| 수동 실행 | `D:\JGY\ai\ComfyUI_windows_portable\run_nvidia_gpu.bat` → http://127.0.0.1:8188 |
| Claude 세션 실행 | `D:\JGY\project\.claude\launch.json`의 "comfyui" 구성(`--disable-auto-launch --listen 127.0.0.1 --port 8188`) |
| 설치 원본 | `D:\JGY\ai\dl\ComfyUI_windows_portable_nvidia.7z` (2.0GB). 7-Zip 없이 Windows 내장 `C:\Windows\System32\tar.exe -xf`로 해제 |
| 테스트 스크립트 | `D:\JGY\ai\h3_test\run_h3_t2v.py` — ComfyUI HTTP API(`/prompt`, `/history`)로 T2V 큐·대기·출력 경로 출력 |
| 출력 | `D:\JGY\ai\ComfyUI_windows_portable\ComfyUI\output\video\` |

### 모델 파일 (`ComfyUI/models/` 아래, 총 약 37GB, Hugging Face `Comfy-Org/MiniMax-H3`)

| 폴더 | 파일 | 크기 | 비고 |
|---|---|---|---|
| diffusion_models | `minimax_h3_fl2va_pruned_w6a8.safetensors` | 16.0GB | 공식 최소 체크포인트(ComfyUI 0.38+). 템플릿 기본값은 `pruned_int8_convrot` 21GB |
| text_encoders | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | 15.7GB | Qwen3-VL 32B, 공식 문서 "모든 GPU 동작" |
| vae | `minimax_h3_video_vae_int8_convrot.safetensors` | 2.8GB | 영상 VAE |
| vae | `minimax_h3_audio_vae_fp32.safetensors` | 0.6GB | 오디오 VAE |
| loras | `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` | 2.0GB | 터보 LoRA. 템플릿은 켜면 6스텝, 끄면 20스텝 |

- 핵심 노드(`MiniMaxH3ImageToVideo`, `EmptyMiniMaxH3LatentAV`, `MiniMaxH3SigmaShift` 등)는 ComfyUI 0.42.1 본체 내장. 커스텀 노드 불필요.
- 내장 템플릿: Template Library > Video > "MiniMax H3 Image to Video"(T2V 겸용, `video_minimax_h3_i2v.json`), Reference to Video, Multiframe Reference, Fun ControlNet, I2V continuation. R2V는 `ref2va` 디노이저(16GB) 추가 다운로드 필요.
- 이미지(first/last_frame)를 연결하지 않으면 T2V로 동작. 프레임 수는 24fps 기준 17k+5 그리드로 스냅(2초→56, 5초→124).
- unsloth GGUF 경로는 ComfyUI-GGUF 노드의 H3 지원을 확인하지 못해 채택하지 않았다.

## 워크플로 (스크립트가 만드는 API 형식)

UNETLoader(w6a8) → LoraLoaderModelOnly(turbo) → BasicGuider / BasicScheduler(simple, steps) ; CLIPLoader(type=minimax) + VAELoader(video) → MiniMaxH3ImageToVideo(prompt, width, height, length) → positive + latent → SamplerCustomAdvanced(res_multistep) → VAEDecode / VAEDecodeAudio → CreateVideo(24fps) → SaveVideo(auto/auto).

```bash
D:\JGY\ai\ComfyUI_windows_portable\python_embeded\python.exe -I D:\JGY\ai\h3_test\run_h3_t2v.py "English prompt" --w 864 --h 480 --sec 5 --steps 6 --seed 1
```

옵션: `--no-lora`(20스텝 권장), `--prefix video/이름`. 서버가 떠 있어야 한다.

## 16GB 카드 운용 메모

- 디노이저 15.2GB·텍스트 인코더 15GB가 ComfyUI 동적 VRAM 로딩으로 RAM↔VRAM을 오가며 동작한다. 실행 중 GPU 사용 약 14.7GB. 다른 GPU 앱이 2.5GB를 쓰는 상태에서도 성공.
- 권장 첫 설정: 0.4MP(864x480 16:9), 5초, 터보 LoRA 6스텝. 2K는 별도 업스케일 패스가 필요.
- 체감 시간(2026-10-23): 608x352·2.3초 약 1.5분, 864x480·5.2초 약 10분(모델 초기화 4분 24초 포함, 스텝당 약 53초). 수치 이력은 WORKLOG 참조.
- `--use-sage-attention`은 sageattention 패키지 미설치로 미시도.

## 다음 작업 후보

- 터보 LoRA 끄고 20스텝 품질 비교.
- I2V(첫 프레임 지정)·R2V(참조 이미지) 테스트.
- 드론 프로젝트 홍보/컨셉 영상 용도 검토는 라이선스(개인 실험 한정) 때문에 API 경로로 전환해야 함.
