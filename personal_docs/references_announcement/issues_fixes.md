<@&1475897949757378651>
The following are the preferred solutions for the issues you all are facing -

1️⃣ For timeout issues, please check the "task.toml" file and update it with the following configuration:

[agent]
timeout_sec = 1800

[verifier]
timeout_sec = 900

[environment]
allow_internet = false
build_timeout_sec = 600 or 900(only write one)
cpus = 2
memory_mb = 4096
storage_mb = 10240

2️⃣ Pin apt/dependency versions explicitly (e.g. `apt-get install -y --no-install-recommends git=1:2.39.5-0+deb12u2`). The repo gate `run_static_checks.py` FAILs unpinned apt packages, and the platform `pinned_dependencies` quality axis only passes when every apt package carries an exact version. (This supersedes the earlier announcement note that said not to pin on Debian — that guidance is retracted; pin on Debian too. If a specific Debian package version is hard to resolve, find the exact version with `apt-cache madison <pkg>` at build time rather than leaving it unpinned.)

3️⃣ If Oracle or NOP tests are not running, check the Summary → Common Failures section for fixes. Also review the default template files on the EC Training website and make all required changes properly for both Docker and task files.

4️⃣ Prefer using Rust, Go, and Bash for tasks, as these are currently receiving fewer revisions. 🚀

5️⃣ AutoEval / upstream `run_static_checks.py` rejects `tests/test.sh` footers that use `RC=$?` and `exit "$RC"`. Use the platform template: run `python -m pytest` with CTRF output, then immediately:

```bash
if [ $? -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi
```

Do not insert commands between pytest and `if [ $? -eq 0 ]`. See `references_announcement/Default_Task_Skeleton/tests/test.sh` and `../.cursor/rules/task-creation.mdc`.
