# API Güvenlik Analiz Raporu

## 🔹 POST /echo
**Açıklama:** Echo test

### 📥 Parametreler
- `message` (body), type: `string`, required: `True`

### 💻 Curl Komutu:
```bash
curl -X POST "https://localhost/echo" -H "Authorization: Bearer demo_token" -H "Content-Type: application/json" -d '"example"'
```

---

## 🔹 GET /users
**Açıklama:** Get a full list of users

### 📥 Parametreler
- `username` (path), type: `string`, required: `True`
- `with_email` (query), type: `boolean`, required: `False`

### 💻 Curl Komutu:
```bash
curl -X GET "https://localhost/users?with_email=true" -H "Authorization: Bearer demo_token"
```

---

## 🔹 GET /users/{username}
**Açıklama:** Get user by user name

### 📥 Parametreler
- `pretty_print` (query), type: `boolean`, required: `False`
- `username` (path), type: `string`, required: `True`
- `with_email` (query), type: `boolean`, required: `False`

### 💻 Curl Komutu:
```bash
curl -X GET "https://localhost/users/example?pretty_print=true&with_email=true" -H "Authorization: Bearer demo_token"
```

### 1. Olası Test Senaryoları
* Örnek Senaryo: User'nin username'unun doğru olduğu ve user'nin email address'i var olduğu durumlarda, API endpoint'e bir sql query yi geçirerek SQL injection saldırısı yapabilir.

### 2. Güvenlik Açıkları
* Örnek Senaryo: User'nin username'unun doğru olduğu ve user'nin email address'i var olduğu durumlarda, API endpoint'e bir XSS payloadını geçirerek XSS saldırısı yapabilir.

### 3. Açıklamalı Örnek Senaryolar
* Örnek Senaryo: User'nin username'unun doğru olduğu ve user'nin email address'i var olduğu durumlarda, API endpoint'e bir username değişim parameterini geçirerek IDOR saldırısı yapabilir.

**Açıklamalı Beispiel Senaryosu:**

* User'nin username'unun doğru olduğu ve user'nin email address'i var olduğu durumlarda, API endpoint successful trảlanmalıdır.
+ Veri Tipi: GET Request
+ Username: Valid user name (örneğin "johnDoe")
+ with_email: True
* User'nin username'unun doğru olmadığını ve user'nin email address'i yok olduğunu gösteren casos:
+ Veri Tipi: GET Request
+ Username: Hatalı veya пуст username (örneğin "john Doe" veya " ")
+ with_email: False

**Mantıksal Kötüye Kullanım Senaryosu (Abuse Case):**

* API endpoint'in güvenlik özelliklerini test etmek için, bir kullanıcı input'ini bir API endpoint'e geçirerek sistemde hatayla karşılaşılabilir.
+ Örnek Senaryo: User'nin username'unun doğru olmadığı ve user'nin email address'i yok olduğu durumlarda, API endpoint'e bir empty query parameterini geçirerek abuse case yapabilir.
+ Veri Tipi: GET Request
+ Username: Hatalı veya пуст username (örneğin "john Doe" veya " ")
+ with_email: False

---

## 🔹 PUT /users/{username}
**Açıklama:** Update the user

### 📥 Parametreler
- `pretty_print` (query), type: `boolean`, required: `False`
- `username` (path), type: `string`, required: `True`
- `body` (body), type: `None`, required: `True`

### 💻 Curl Komutu:
```bash
curl -X PUT "https://localhost/users/example?pretty_print=true" -H "Authorization: Bearer demo_token" -H "Content-Type: application/json" -d '"example"'
```

---

## 🔹 DELETE /users/{username}
**Açıklama:** Delete user

### 📥 Parametreler
- `pretty_print` (query), type: `boolean`, required: `False`
- `username` (path), type: `string`, required: `True`

### 💻 Curl Komutu:
```bash
curl -X DELETE "https://localhost/users/example?pretty_print=true" -H "Authorization: Bearer demo_token"
```

---

