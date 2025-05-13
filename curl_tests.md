# filedepot API curl 테스트 명령어 예시

## Gateway (8000)

```
curl -X GET "http://localhost:8000/gateway/health" -H "accept: application/json"
```

## File (8001)

### 파일 업로드 (multipart/form-data)
```
curl -X POST "http://localhost:8001/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.txt" \
  -F "metadata=@meta.json"
```

## Data (8002)

```
curl -X POST "http://localhost:8002/data/insert" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"table": "my_table", "data": {"col1": "value"}}'
```

> 실제 엔드포인트/파라미터는 각 도메인별 라우트에 맞게 수정 필요
