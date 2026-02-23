## 쿠버네티스 명령어 : `kubectl`

- 명령어 알아보기
```bash
kubectl api-resources
```

- 명령어 사용 설명
```bash
kubectl --help
```

- 로그 확인 설명
```bash
kubectl logs --help
```

- pod 생성
```bash
kubectl run web --image=nginx:1.28 --port 80
```

- 서비스 Port 활성화(외부 접속 허용 설정)
```bash
kubectl port-forward pod/web 80:80
```
