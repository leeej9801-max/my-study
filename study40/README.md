## Helm (k8s package manager)

- [Helm 설치](https://helm.sh/ko/docs/intro/install)
```bash
winget install Helm.Helm
```

- Helm 목록 보기
```bash
helm list
```

- Helm Local Repository 등록
```bash
helm repo add [Chart명] [Chart 배포 URL]
```

- Helm Local Repository 목록
```bash
helm repo list
```

- Helm Local Repository 검색
```bash
helm search repo [Chart명]
```

- Helm Chart 설치
```bash
helm install [Chart명] [Package 위치]
```

- Helm Chart 삭제
```bash
helm uninstall [Chart명]
```
