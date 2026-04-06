## `Namespace` 구성하기

- 목록 보기
```bash
kubectl get namespaces
```

- 현제 사용 중인 context 확인
```bash
kubectl config get-contexts
```

- ns 생성
```bash
kubectl create namespace n1
```

- yaml 생성
```bash
kubectl create namespace n2 --dry-run -o yaml > n2-ns.yaml
```

- Pod 생성
```bash
kubectl run web --image=nginx:1.28 --port 80 -n n1 --dry-run -o yaml
```

- Context 생성 및 등록
```bash
kubectl config set-context n1-context --cluster=docker-desktop  --user=docker-desktop  --namespace=n1
```

- Context 교체 
```bash
kubectl config use-context n1-context
```

- Context 삭제
```bash
kubectl config delete-context n1-context
```

- 클러스터 실행 상태 확인
```bash
kubectl cluster-info
```
