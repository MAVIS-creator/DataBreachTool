# 📧 Email Breach Checker

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)]()
[![License](https://img.shields.io/badge/License-MIT-success)]()
[![Status](https://img.shields.io/badge/Status-Active-informational)]()
[![HIBP API](https://img.shields.io/badge/API-Have%20I%20Been%20Pwned-ff69b4)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)]()

A Python CLI tool that checks if an email appears in known data breaches via the [Have I Been Pwned (HIBP) API](https://haveibeenpwned.com/API/v3). It prints friendly, detailed results about any breaches.

---

## ⚡ Features
- Interactive CLI flow — prompts for an email.
- Fetches detailed breach info: title, breach date, description, data classes, and domain.
- Graceful error handling (network failures, parsing issues, etc.).

---

## 🛠️ Requirements
- Python **3.7+**
- Package: `requests`

```bash
pip install requests
```

---

## 🚀 Quickstart
1. Save your script as `breach_checker.py` (or keep your current file name).
2. Install dependencies (see above).
3. Run the CLI and follow the prompt:

```bash
python breach_checker.py
```

Example:
```text
Enter your email address: example@email.com
Checking for breaches...
...
```

---

## 🔑 Using a HIBP API Key (for `/breachedaccount`)

The `/api/v3/breachedaccount/{email}` endpoint requires an API key. Here’s how to set it up:

### 1) Get an API Key
- Create an account and subscribe to the HIBP API. You'll receive a key string.

### 2) Store the Key as an Environment Variable
```bash
# macOS / Linux
export HIBP_API_KEY="<your-key>"

# Windows (PowerShell)
setx HIBP_API_KEY "<your-key>"
```

### 3) Update Your Script
Make sure your breach request includes these headers:

```python
import os

api_key = os.getenv("HIBP_API_KEY")
headers = {
    "hibp-api-key": api_key,               # required
    "User-Agent": "EmailBreachChecker/1.0" # required
}

breach_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
breach_response = requests.get(breach_url, headers=headers, timeout=15)
```

> **Tip:** Keep `truncateResponse=false` to receive full breach details.

<details>
<summary>Rate limiting & retry tips</summary>

- Respect HTTP `429` (Too Many Requests). Retry after the time indicated by `Retry-After`.
- Set a reasonable timeout on requests (e.g., 10–20 seconds).
- Cache or debounce identical lookups when possible.

</details>

---

## 🧑‍💻 Usage Examples

**Breached email:**
```text
Your email 'someone@example.com' has been found in the following data breaches:
- ExampleBreach (2021-06-10): ...
  Compromised data: Emails, Passwords, Phone numbers
  More info: example.com
--------------------
```

**Not found:**
```text
Your email 'someone@example.com' has not been found in any known data breaches (or is not in the pwnedbreaches database).
```

---

## 🔒 Security & Privacy
- **Never** log API keys or raw responses containing sensitive data.
- Use the official *k-anonymity* range API only for password hash checks (not for emails).
- Always include a clear `User-Agent` string identifying your app.

---

## ⚠️ Notes
- Some endpoints are paid/limited. Consult the [HIBP API docs](https://haveibeenpwned.com/API/v3) for the latest policies.
- If you see unexpected results, verify your headers and ensure your API key is set and valid.

---

## 📜 License
MIT — do what you want, just include the license and attribution where appropriate.

---

❤️ Built for developers. Stay safe out there.
