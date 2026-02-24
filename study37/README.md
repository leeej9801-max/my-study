## 서비스 트래픽 증가 시 서버 증설 방법

- 기존 POD 설정을 반복적으로 작성하기
- 디플로이먼트으로 POD 관리하기

#### `Deployment` 알아보기

- `Replica` : 복제본
- `ReplicaSet` : 복제본끼리의 묶음

> `manifest file` 만들기

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: backend-deployment

spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend-app
  template:
    metadata:
      labels:
        app: backend-app
    spec:
      containers:
        - name: fastapi-container
          image: backend:latest
          ports:
            - containerPort: 8000
          imagePullPolicy: IfNotPresent
```

#### Deployment 실습

- deployment 생성
```bash
kubectl apply -f fastapi-deployment.yaml
```

- deployment 동작 확인 명령어
```bash
kubectl get deployment
```

- Replicaset 동작 확인 명령어
```bash
kubectl get replicaset
```

- pod 동작 확인 명령어
```bash
kubectl get pods
```

#### POD 증가 실습

- `replicas` : ***3 -> 5*** deployment 파일 변경
- deployment 다시 적용하기
```bash
kubectl apply -f fastapi-deployment.yaml
```

#### POD 비정상 실습

- docker container `kill` 하기
```bash
docker ps
docker kill [container-ID]
kubectl get pods
```

## 외부로부터 들어오는 트래픽을 받아 파드에 균등하게 분배해주는 로드밸런서 역할 알아보기

#### `Pod` 에서 요청 보내는 방법

- `port-forward` : 로컬에서 포트 연결 방법
- `kubectl exec ...` : 내부 접속 방법

#### `Service` 종류

- `NodePort`: k8s 내부에서 해당 서비스에 접속하기 위한 포트를 열고 외부에서 접속 가능하도록 합니다.
- `ClusterIP`: k8s 내부에서만 통신할 수 있는 IP 주소를 부여, 외부에서는 요청할 수 없습니다.
- `LoadBalancer`: 외부의 로드밸런서(AWS의 로그밸런서 등)를 활용해 외부에서 접속할 수 있도록 연결 합니다.

> `manifest file` 만들기

```yaml
apiVersion: v1
kind: Service

metadata:
  name: backend-service

spec:
  type: NodePort
  selector:
    app: backend-app
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
      nodePort: 8000
```

> 외부 포트 범위 : `30000 ~ 32767`

#### Service 실습

- service 파일 적용 명령어
```bash
kubectl apply -f fastapi-service.yaml
```

- service 동작 확인 명령어
```bash
kubectl get service
```
