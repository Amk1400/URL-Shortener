# 📘 README - Midterm Final Checklist

This README **must remain in your repository** and **must be fully completed** before submitting the midterm.

---

## 1. API Test Coverage Table

Fill in the second column with the **name of the student** who implemented and tested each API.

| # | API Endpoint / Feature | Implemented & Tested By (Student Name) |
|---|------------------------|-----------------------------------------|
| 1 | Create Short Link - **POST /links** | Alice |
| 2 | Redirect to Original URL - **GET /{code}** | Bob |
| 3 | Get All Shortened Links - **GET /links** | Alice |
| 4 | Delete Short Link - **DELETE /links/{code}** | Bob |

---

## 2. Code Generation Method (Section 6.4)

Check the method you used to generate the short code:

- [ ] **1. Random Generation**
- [x] **2. ID → Base62 Conversion**
- [ ] **3. Hash-based Generation**

(Only select the one you actually implemented.)

---

## 3. Bonus User Story: TTL (Expiration Time) for Shortened Links)

If you implemented the bonus user story, mark the box and complete the required details.

- [x] **TTL Feature Implemented**

**If checked, fill in the following information:**

- **ENV variable or config key used:** 
 `LINK_TTL_SECONDS=400`

You must also ensure this key exists in `.env.example` with a sample value.


- **Location of TTL Logic (File + Function):** 

Specify the exact location where TTL expiration is checked and expired links are detected/removed.

 `services/link_service.py → delete_expired_links()`

- **How TTL cleanup is triggered:** 
You must write a Command that removes expired links (created_at + TTL < now()).

Here, write:

- Full file path of the command
- Command name / execution method
- Scheduler details
---

## 4. Postman Collection (Required)

A **Postman Collection** has been created and includes all four API routes:

- **POST /links**
- **GET /{code}**
- **GET /links**
- **DELETE /links/{code}**

### Screenshots (included in GitHub)

For each route, two screenshots have been added:

- Successful response (2xx) 
- Error-handled response (4xx)

Screenshots are located in:

‍‍      ‍```
   /postman
   ```



### Naming Example:

```
postman/
post-links-201-success.png
post-links-400-invalid-url.png
get-code-302-redirect.png
get-code-404-not-found.png
get-links-200-success.png
delete-code-200-success.png
delete-code-404-not-found.png
```

Filenames must clearly show:

- Route 
- HTTP status 
- Success or error 

---

**✔️ Make sure this README is fully completed before submission.**