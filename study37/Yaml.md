## yaml 파일 작성

- api version 확인
```bash
kubectl explain service
```

- Pod용 yaml
```yaml
apiVersion: v1
kind: Pod

metadata:
  name: [Pod 이름]

spec:
  containers:
  - image: [docker 이미지]
      name: [container 이름]
```

- Deployment용 yaml
```bash
apiVersion: apps/v1
kind: Deployment

metadata:
  name: [Deployment 이름]

spec:
  replicas: [Pod 수]
  selector:
    matchLabels:
      app: [Pod 라벨명]
  template:
    metadata:
      labels:
        app: [Pod 라벨명]
    spec:
      containers:
        - image: [docker 이미지]
          name: [container 이름]
          ports:
          - containerPort: [service port]
```

- yaml 만들기
```bash
kubectl create deployment app-dp --replicas=2 --image=nginx:1.28 --dry-run -o yaml > app-dp.yaml
```

- `yaml`에 label 추가 
```yaml
template:
  metadata:
    labels:
      app: [Pod 라벨명]
```

- Pod 정보 실시간 확인
```bash
kubectl get pods --watch
```

- 수정하기
```bash
kubectl edit deployment/app-dp
```

- Service 만들기
```yaml
apiVersion: v1
kind: Service

metadata:
  name: app-sv

spec:
  type: NodePort
  seletor:
    app: app-label
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 80
```