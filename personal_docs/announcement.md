📢 **Important Project Updates**

Hey everyone, we have several major updates regarding tasks, CI requirements, and project resources. Please read everything carefully.

## 🔹 New `task.toml` Requirement

A new blocking CI check is being introduced. Every `task.toml` file must now include:

```toml
[environment]
allow_internet = false
```

### What this means:

Internet access will be blocked during runtime, so your `test.sh` scripts can no longer download or install dependencies while running.

### ❌ No longer allowed inside `test.sh`

- `apt-get install`
- `pip install`
- `curl`
- `uv installs`
- Any other runtime dependency installation

### ✅ Required approach

All verifier dependencies must already be included inside the Docker image through the `Dockerfile`.

---

## 🔹 New Task Skeletons Available

Updated task skeletons have been uploaded to the project website.

You can find them:

- In the **Resources** tab
- Linked alongside this announcement for easier access

These updated skeletons align with the new internet-disabled environment requirements.

---

## 🔹 New Large Codebase Task Ideas

New Large Codebase task ideas have been added to the **Task Gallery**.

These include:

- Pre-built environments
- Bundled verifier tests
- Ready-to-use supporting files

### How to find them:

Go to the **Task Gallery** and scroll to the new purple **“Large Codebase Tasks”** section.

These resources are meant to make large codebase task creation much easier and more approachable.

---

## 🔹 Clarification on Task Difficulty Thresholds

To determine task difficulty, evaluate thresholds in this order:
**Hard → Medium → Easy**

Stop at the first category your task matches.

### HARD

1. Accuracy ≤ 20% on the **best** model
2. Accuracy ≤ 20% on the **worst** model
   _(if condition #1 does not apply)_

### MEDIUM

3. 20% < Accuracy ≤ 60% on the worst model

### EASY

4. 60% < Accuracy ≤ 80% on the worst model

---

## 💡 Example

```txt
terminus-claude-opus-4-6: 100.0% (5/5 runs)  ← Best model
terminus-gpt5-2: 20.0% (1/5 runs)           ← Worst model
```

- HARD condition #1 fails because the best model scored 100%
- HARD condition #2 passes because the worst model scored 20%

✅ Therefore, this qualifies as a **HARD** task.

---

## 🔹 Dockerfile & Image Best Practices

A new documentation page covering Dockerfile and image best practices has also been added to the site.

Please take some time to review it carefully, as it contains important guidance for maintaining compatible and efficient environments.
