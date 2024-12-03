(venv) cherylmaevahfodjo@cheryls-mbp ERP % cd frontend && np
m run dev

> fofal-erp@0.1.0 dev
> vite

Port 3000 is in use, trying another one...

  VITE v4.5.5  ready in 512 ms

  ➜  Local:   http://localhost:3001/
  ➜  Network: use --host to expose
  ➜  press h to show help
Error:   Failed to scan for dependencies from entries:
  /Users/cherylmaevahfodjo/ERP/ERP/frontend/index.html

  ✘ [ERROR] No matching export in "src/types/inventaire.ts" for import "SeuilStock"

    src/components/inventaire/StatsInventaire.tsx:14:45:
      14 │ ...roduit, PeriodeInventaire, SeuilStock } from '../../types/inven...
         ╵                               ~~~~~~~~~~


✘ [ERROR] No matching export in "src/types/production.ts" for import "QualiteRecolte"

    src/components/production/ParcelleDetails.tsx:22:45:
      22 │ ...roductionEvent, Recolte, QualiteRecolte } from '../../types/pro...
         ╵                             ~~~~~~~~~~~~~~


✘ [ERROR] No matching export in "src/types/production.ts" for import "CultureType"

    src/components/production/ParcellesList.tsx:22:19:
      22 │ import { Parcelle, CultureType, ParcelleStatus } from '../../types...
         ╵                    ~~~~~~~~~~~


✘ [ERROR] No matching export in "src/types/production.ts" for import "ParcelleStatus"

    src/components/production/ParcellesList.tsx:22:32:
      22 │ ...{ Parcelle, CultureType, ParcelleStatus } from '../../types/pro...
         ╵                             ~~~~~~~~~~~~~~


✘ [ERROR] No matching export in "src/types/production.ts" for import "CultureType"

    src/components/production/ProductionStats.tsx:12:9:
      12 │ import { CultureType } from '../../types/production';
         ╵          ~~~~~~~~~~~


    at failureErrorWithLog (/Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:1649:15)
    at /Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:1058:25
    at runOnEndCallbacks (/Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:1484:45)
    at buildResponseToResult (/Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:1056:7)
    at /Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:1068:9
    at new Promise (<anonymous>)
    at requestCallbacks.on-end (/Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:1067:54)
    at handleRequest (/Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:729:19)
    at handleIncomingPacket (/Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:755:7)
    at Socket.readFromStdout (/Users/cherylmaevahfodjo/ERP/ERP/frontend/node_modules/esbuild/lib/main.js:679:7)
