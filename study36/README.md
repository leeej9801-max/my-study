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

- pod 정보 보기
```bash
kubectl get pods -o wide
```

- pod 접속 하기
```bash
kubectl exec -it web -- /bin/bash
```

- nginx `curl` 명령어로 확인 하기
```bash
curl localhost
```

- 매니페스트 파일 를 이용하여 pod 생성하기
```bash
kubectl apply -f web-pod.yaml
```

# pod 종료 및 삭제
```bash
kubectl delete all --all
```
