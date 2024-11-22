Current runner version: '2.321.0'
Operating System
Runner Image
Runner Image Provisioner
GITHUB_TOKEN Permissions
Secret source: Actions
Prepare workflow directory
Prepare all required actions
Getting action download info
Download action repository 'actions/checkout@v3' (SHA:f43a0e5ff2bd294095638e18286ca9a3d1956744)
Download action repository 'actions/setup-node@v3' (SHA:1a4442cacd436585916779262731d5b162bc6ec7)
Complete job name: build-frontend
5s
Run actions/checkout@v3
Syncing repository: Kaiser9005/ERP
Getting Git version info
Temporarily overriding HOME='/home/runner/work/_temp/38a236d9-5b4e-4427-8ff1-e0e0c56e63a2' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/ERP/ERP
Deleting the contents of '/home/runner/work/ERP/ERP'
Initializing the repository
Disabling automatic garbage collection
Setting up auth
Fetching the repository
2s
15s
0s
2s
Run npm run build

> fofal-erp@0.1.0 build
> tsc && vite build

error TS6305: Output file '/home/runner/work/ERP/ERP/vite.config.d.ts' has not been built from source file '/home/runner/work/ERP/ERP/vite.config.ts'.
  The file is in the program because:
    Matched by include pattern 'vite.config.ts' in '/home/runner/work/ERP/ERP/tsconfig.json'
Error: Process completed with exit code 2.