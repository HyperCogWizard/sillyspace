# CircleCI to GitHub Actions Migration

This repository has been migrated from CircleCI to GitHub Actions. The new workflow file is located at `.github/workflows/ci.yml`.

## Migration Summary

### Original CircleCI Configuration
- **File**: `.circleci/config.yml`
- **Jobs**: 15 main jobs plus 1 package job
- **Features**: Workspace persistence, ccache optimization, PostgreSQL services, complex dependency chain

### New GitHub Actions Configuration
- **File**: `.github/workflows/ci.yml`
- **Jobs**: 16 jobs (same functionality as CircleCI)
- **Triggers**: Push and Pull Request on `master` and `main` branches

## Key Translations

### 1. Workspace Persistence
**CircleCI**:
```yaml
- persist_to_workspace:
    root: /ws/
    paths: [cogutil, atomspace, ccache]
- attach_workspace:
    at: /ws
```

**GitHub Actions**:
```yaml
- name: Upload workspace
  uses: actions/upload-artifact@v4
  with:
    name: workspace-atomspace
    path: |
      cogutil/
      atomspace/
      ccache/
- name: Download workspace
  uses: actions/download-artifact@v4
  with:
    name: workspace-atomspace
```

### 2. Caching
**CircleCI**:
```yaml
- restore_cache:
    keys:
      - ccache-{{ checksum "/tmp/date" }}
      - ccache-
- save_cache:
    key: ccache-{{ checksum "/tmp/date" }}
    paths: [/ws/ccache]
```

**GitHub Actions**:
```yaml
- name: Cache ccache
  uses: actions/cache@v4
  with:
    path: ${{ github.workspace }}/ccache
    key: ccache-${{ runner.os }}-${{ github.run_id }}
    restore-keys: |
      ccache-${{ runner.os }}-
```

### 3. Service Containers
**CircleCI**:
```yaml
- image: $CIRCLE_PROJECT_USERNAME/postgres
  name: opencog-postgres
```

**GitHub Actions**:
```yaml
services:
  postgres:
    image: postgres:13
    env:
      POSTGRES_USER: opencog_test
      POSTGRES_PASSWORD: cheese
      POSTGRES_DB: opencog_test
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432
```

### 4. Job Dependencies
**CircleCI**:
```yaml
workflows:
  build-test-package:
    jobs:
      - atomspace
      - unify:
          requires: [atomspace]
      - ure:
          requires: [atomspace, unify]
```

**GitHub Actions**:
```yaml
jobs:
  atomspace:
    runs-on: ubuntu-latest
  unify:
    needs: atomspace
  ure:
    needs: [atomspace, unify]
```

## Job Dependencies Graph

```
atomspace (root)
├── atomspace-storage
│   ├── atomspace-pgres
│   │   └── matrix
│   ├── atomspace-rocks
│   └── cogserver
│       ├── atomspace-cog
│       └── attention
│           └── opencog (with ure)
├── spacetime
│   └── pln (with ure)
└── unify
    └── ure
        ├── miner
        └── pln (with spacetime)
        └── opencog (with attention, cogserver)
            └── package (master branch only)
```

## Key Differences

### Advantages of GitHub Actions Version
1. **Native Integration**: Better integration with GitHub repository features
2. **Modern Syntax**: More readable YAML structure
3. **Built-in Caching**: Native cache actions with better key management
4. **Service Health Checks**: Built-in health checking for service containers
5. **Conditional Execution**: More flexible conditional job execution

### Maintained Features
1. **Same Build Process**: All CMake configure, build, test, install steps preserved
2. **Dependency Chain**: Exact same job dependency structure maintained
3. **Test Execution**: All test runs and log collection preserved
4. **Environment Variables**: All necessary environment variables translated
5. **Parallel Execution**: Jobs run in parallel where dependencies allow

## Notes
- The `as-moses` job was commented out in CircleCI and is not included
- Some test runs are disabled due to known issues (referenced in comments)
- Package job only runs on `master` branch (matches CircleCI behavior)
- Uses `ubuntu-latest` instead of custom Docker images with system package installation