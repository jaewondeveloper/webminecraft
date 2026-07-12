# Web Minecraft — Jaewon Launcher

브라우저에서 마인크래프트를 실행하는 웹 런처입니다.

## 온라인 플레이 (GitHub Pages)

**https://jaewondeveloper.github.io/webminecraft/**

Chrome 또는 Edge에서 접속 → 버전 설치 → 플레이

## 로컬 플레이

```powershell
.\start-all.ps1
```

브라우저에서 **http://localhost:8090**

| 포트 | 버전 |
|------|------|
| 8090 | 웹 런처 |
| 8080 | Minecraft 1.12.2 WASM |
| 8084 | Minecraft 1.12.2 JS |
| 8081 | EaglyMC 1.8.8 JS |
| 8082 | EaglyMC 1.8.8 WASM |
| 8083 | EaglyMC 1.8.8 저사양 |
| 8085 | Astra Edition 1.19.2 |

## 버전 설치 저장

설정 → **버전 설치**에서 설치한 목록은 브라우저 `localStorage`에 저장됩니다.  
다시 접속해도 설치한 버전이 유지됩니다.

## 배포

`main` 또는 `master` 브랜치에 push하면 GitHub Actions가 Pages에 자동 배포합니다.

저장소 설정에서 **Pages → Source: GitHub Actions** 를 선택하세요.

런처 UI 수정 후 루트에 반영:

```powershell
.\scripts\sync_launcher_to_root.ps1
```

## 복구

8080 검은 화면: `.\scripts\setup_web.ps1`
