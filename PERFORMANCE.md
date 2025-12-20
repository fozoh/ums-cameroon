# Performance Optimization Guide

This guide covers strategies to optimize UMS Cameroon for production workloads.

## 1. Database Optimization

### Add Indexes

```python
# In backend/students/models.py

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matric_number = models.CharField(max_length=20, unique=True, db_index=True)  # Add index
    cgpa = models.FloatField(default=0.0, db_index=True)  # Frequently filtered
    
    class Meta:
        indexes = [
            models.Index(fields=['cgpa', 'level']),  # Composite index for at-risk queries
        ]

class ExamResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['student', 'course']),
        ]
        unique_together = ('student', 'course')
```

### Query Optimization

```python
# backend/students/views.py

# ❌ SLOW: N+1 queries
def student_results_view(request):
    results = ExamResult.objects.filter(student=request.user.student_profile)
    # This triggers N queries for related courses
    return Response([{'course': r.course.code} for r in results])

# ✅ FAST: Use select_related
def student_results_view(request):
    results = ExamResult.objects.filter(
        student=request.user.student_profile
    ).select_related('course', 'student')  # Load related data in one query
    return Response([{'course': r.course.code} for r in results])
```

### Query Pagination

```python
# Implement pagination to limit result sets
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# Use in views
class StudentCAListView(generics.ListAPIView):
    pagination_class = StandardPagination
    # ...
```

### Connection Pooling

```bash
# Install pgbouncer for PostgreSQL connection pooling
# For production with many concurrent users
sudo apt install -y pgbouncer
```

---

## 2. Caching Strategy

### Django Cache Framework

```python
# backend/ums/settings.py

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'ums_',
        'TIMEOUT': 300,  # 5 minutes default
    }
}
```

### Cache Expensive Queries

```python
# backend/students/views.py

from django.core.cache import cache

def predict_at_risk_students(request):
    # Cache the result for 1 hour
    cache_key = f'at_risk_{request.user.id}'
    at_risk = cache.get(cache_key)
    
    if at_risk is None:
        # Expensive computation
        at_risk = StudentPathway.objects.filter(
            cgpa__lt=2.0,
            status='active'
        ).select_related('student')
        cache.set(cache_key, at_risk, 3600)
    
    return Response(at_risk)
```

### Cache HTTP Responses

```python
# Use Django's cache_page decorator
from django.views.decorators.cache import cache_page

@cache_page(300)  # Cache for 5 minutes
def resit_timetable(request):
    # ...
```

---

## 3. Frontend Optimization

### Code Splitting

```javascript
// frontend/src/App.jsx
import React, { lazy, Suspense } from 'react';

const AdminDashboard = lazy(() => import('./pages/AdminDashboard'));
const StudentDashboard = lazy(() => import('./pages/StudentDashboard'));

export default function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Route path="/admin" element={<AdminDashboard />} />
      <Route path="/student" element={<StudentDashboard />} />
    </Suspense>
  );
}
```

### Image Optimization

```javascript
// Use WebP with fallback
<picture>
  <source srcSet="image.webp" type="image/webp" />
  <img src="image.jpg" alt="description" />
</picture>
```

### Minify & Compress

```bash
# Already done by npm run build
# Ensure gzip compression is enabled in nginx
```

### React DevTools Profiling

```bash
# Identify slow components
npm run build
# Analyze with npm start and React DevTools
```

---

## 4. API Response Optimization

### Compress Responses

```python
# backend/ums/settings.py
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # Compress responses
    # ...
]
```

### Field Filtering

```python
# Allow clients to request only needed fields
GET /api/results/?fields=course,grade

# Implement with rest_framework
from rest_framework import serializers

class DynamicFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.context['request'].query_params.get('fields')
        if fields:
            allowed = set(fields.split(','))
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
```

---

## 5. Server Configuration

### Gunicorn Workers

```bash
# backend/Dockerfile
# Calculate optimal worker count: (2 x CPU cores) + 1
# For 4 cores: 9 workers

CMD ["gunicorn", \
     "--workers=9", \
     "--worker-class=gthread", \
     "--threads=2", \
     "--bind=0.0.0.0:8000", \
     "ums.wsgi:application"]
```

### Nginx Configuration

```nginx
# nginx.conf
upstream backend {
    least_conn;  # Load balance algorithm
    server backend:8000 max_fails=3 fail_timeout=30s;
}

server {
    # Enable gzip
    gzip on;
    gzip_types text/plain text/css text/xml text/javascript application/json;
    gzip_min_length 1000;
    
    # Enable caching
    expires 1h;
    add_header Cache-Control "public, max-age=3600";
    
    # Enable HTTP/2
    listen 443 ssl http2;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

---

## 6. Monitoring & Profiling

### Identify Bottlenecks

```python
# Use Django Debug Toolbar (dev only)
pip install django-debug-toolbar

# Settings
INSTALLED_APPS = ['debug_toolbar', ...]
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ...]
INTERNAL_IPS = ['127.0.0.1']
```

### Application Performance Monitoring (APM)

```bash
# Use services like New Relic, DataDog, or open-source Sentry
pip install sentry-sdk

# In settings.py
import sentry_sdk
sentry_sdk.init(
    dsn="https://<key>@sentry.io/<project>",
    traces_sample_rate=0.1
)
```

### Database Query Monitoring

```python
# Log slow queries
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## 7. Load Testing

### Using Locust

```bash
pip install locust
```

```python
# locustfile.py
from locust import HttpUser, task

class UserBehavior(HttpUser):
    @task
    def get_results(self):
        self.client.get('/api/results/')
    
    @task
    def login(self):
        self.client.post('/api/login/', json={
            'username': 'test',
            'password': 'test'
        })
```

```bash
locust -f locustfile.py --host=http://localhost:8000
```

---

## 8. Recommendations Checklist

- [ ] Add database indexes for frequently queried fields
- [ ] Use select_related/prefetch_related in queries
- [ ] Implement caching (Redis)
- [ ] Enable gzip compression
- [ ] Minify frontend assets
- [ ] Use CDN for static files
- [ ] Setup monitoring & alerting
- [ ] Load test before launch
- [ ] Enable HTTP/2 and SSL
- [ ] Configure connection pooling
- [ ] Optimize images (WebP)
- [ ] Code split React components

---

## Performance Benchmarks (Target)

| Metric | Target |
|--------|--------|
| Page load time | < 2s |
| API response time (p95) | < 200ms |
| Database query time (p95) | < 100ms |
| Frontend bundle size | < 100KB gzip |
| Concurrent users supported | 1000+ |

---

## Further Reading

- [Django Performance Optimization](https://docs.djangoproject.com/en/4.2/topics/performance/)
- [React Performance Optimization](https://react.dev/reference/react/Profiler)
- [PostgreSQL Query Optimization](https://www.postgresql.org/docs/current/sql-explain.html)
- [Nginx Performance Tuning](https://nginx.org/en/docs/)
