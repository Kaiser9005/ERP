[read_file for 'problemes build frontend.md'] Result:

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


<environment_details>
# VSCode Visible Files
docs/diagrammes/flux_projets.md
docs/diagrammes/flux_projets.md
frontend/src/components/finance/GraphiqueTresorerie.tsx

# VSCode Open Tabs
docs/api/parametrage.md
docs/diagrammes/README.md
docs/api/production_reports.md
docs/guides/installation.md
models/task.py
schemas/task.py
models/resource.py
schemas/resource.py
frontend/src/components/dashboard/__tests__/ProductionStats.test.tsx
frontend/src/components/dashboard/__tests__/CashFlowChart.test.tsx
services/task_service.py
api/v1/endpoints/tasks.py
docs/api/tasks.md
services/production_report_service.py
api/v1/endpoints/production_reports.py
api/v1/endpoints/finance.py
.git/COMMIT_EDITMSG
frontend/src/types/task.ts
frontend/src/services/tasks.ts
frontend/src/types/cashflow.ts
frontend/src/types/common.ts
frontend/src/components/comptabilite/rapports/GrandLivre.tsx
frontend/src/types/parametrage.ts
frontend/src/components/finance/StatsFinance.tsx
frontend/src/components/dashboard/__tests__/FinanceStats.test.tsx
src/components/finance/TransactionsList.tsx
src/components/finance/TransactionForm.tsx
src/components/production/ParcelleDetails.tsx
src/components/production/ParcelleForm.tsx
src/components/production/ParcelleMap.tsx
src/components/production/ParcellesList.tsx
src/components/production/ProductionCalendar.tsx
src/components/production/ProductionDashboard.tsx
src/components/production/ProductionPage.tsx
src/components/production/ProductionStats.tsx
src/components/production/WeatherDashboard.tsx
src/components/projects/ProjectDetails.tsx
src/components/projects/ProjectForm.tsx
src/components/projects/ProjectsPage.tsx
frontend/src/components/parametrage/ParametrageLayout.tsx
frontend/src/components/parametrage/ParametresGeneraux.tsx
frontend/src/components/parametrage/ConfigurationModules.tsx
frontend/src/types/project.ts
frontend/src/components/projects/ProjectDetails.tsx
frontend/src/components/projects/__tests__/ProjectDetails.test.tsx
src/types/project.ts
docs/api/projects.md
frontend/src/components/projects/TaskList.tsx
frontend/src/routes/projects.tsx
frontend/src/routes/index.tsx
models/hr_formation.py
schemas/hr_formation.py
services/hr_formation_service.py
frontend/src/services/formation.ts
frontend/src/components/hr/formation/FormationList.tsx
frontend/src/components/hr/formation/FormationForm.tsx
frontend/src/components/hr/formation/FormationPage.tsx
docs/api/formation.md
tests/test_hr_formation_service.py
tests/integration/test_hr_formation_integration.py
tests/e2e/test_hr_formation_e2e.py
frontend/src/components/hr/formation/__tests__/FormationList.test.tsx
frontend/src/components/hr/formation/__tests__/FormationForm.test.tsx
frontend/src/components/hr/formation/__tests__/FormationPage.test.tsx
docs/guides/formation.md
api/v1/endpoints/hr_formation.py
frontend/src/types/formation.ts
frontend/src/routes/production.tsx
frontend/src/components/dashboard/RecentActivities.tsx
frontend/.gitignore
frontend/index.html
frontend/src/components/dashboard/ProductionChart.tsx
frontend/src/components/dashboard/modules/ProjectsModule.tsx
docs/developpement_futur.md
frontend/tsconfig.json
frontend/src/services/hr_agricole.ts
frontend/tsconfig.node.json
frontend/vite.config.ts
frontend/src/contexts/ThemeModeContext.tsx
frontend/src/components/auth/LoginPage.tsx
src/services/production.ts
src/services/projects.ts
src/types/production.ts
docs/diagrammes/flux_production.md
frontend/src/components/production/WeatherAnalytics.tsx
frontend/src/components/dashboard/__tests__/WeatherWidget.test.tsx
docs/modules/production.md
docs/diagrammes/architecture_nouvelle.md
docs/diagrammes/migration.md
services/ml/tableau_bord/alertes.py
tests/test_tableau_bord_predictions.py
tests/integration/test_tableau_bord_ml_integration.py
tests/e2e/test_tableau_bord_ml_e2e.py
docs/plan_developpement.md
~/erp_references/analysis/ameliorations_realisees.md
frontend/src/components/inventaire/DetailsProduit.tsx
frontend/src/components/inventaire/__tests__/DetailsProduit.test.tsx
frontend/src/components/inventaire/DialogueMouvementStock.tsx
frontend/src/components/inventaire/__tests__/DialogueMouvementStock.test.tsx
frontend/src/components/inventaire/FormulaireProduit.tsx
frontend/src/components/inventaire/__tests__/FormulaireProduit.test.tsx
frontend/src/components/inventaire/__tests__/ListeStock.test.tsx
scripts/analyze_duplicates.py
frontend/src/components/dashboard/__tests__/MLDashboard.test.tsx
frontend/src/components/inventaire/__tests__/StatsInventaire.test.tsx
src/routes/inventaire.tsx
src/routes/parametrage.tsx
src/routes/production.tsx
src/routes/projects.tsx
frontend/src/utils/format.ts
frontend/src/services/dashboard.ts
frontend/src/services/__tests__/dashboard.test.ts
tests/integration/test_ml_services_integration.py
tests/conftest.py
tests/integration/test_tableau_bord_unified.py
tests/e2e/test_tableau_meteo.py
.env
docs/modules/production_module.md
frontend/src/services/comptabilite.ts
frontend/src/services/notifications.ts
tests/ml/README.md
tests/ml/test_performance.py
tests/ml/.gitignore
tests/ml/__init__.py
tests/ml/utils.py
tests/ml/conftest.py
services/ml/tableau_bord/unification.py
pytest.ini
requirements.txt
tests/ml/projets/test_analysis.py
tests/ml/finance_comptabilite/test_finance_comptabilite_integration.py
tests/ml/finance_comptabilite/test_finance_comptabilite_couts.py
tests/ml/finance_comptabilite/test_finance_comptabilite_meteo.py
tests/ml/finance_comptabilite/test_finance_comptabilite_iot.py
frontend/vitest.config.ts
frontend/vitest.integration.config.ts
services/ml/tableau_bord/predictions.py
tests/test_tableau_bord_unification.py
tests/test_tableau_bord_alertes.py
docs/diagrammes/composants.md
src/types/api.ts
src/types/common.ts
src/components/finance/CashFlowChart.tsx
frontend/src/services/hr.ts
frontend/src/components/hr/types/formTypes.ts
frontend/src/components/hr/LeaveRequestForm.tsx
frontend/src/components/hr/schemas/employeeSchema.ts
docs/api/hr.md
docs/guides/developpement.md
docs/guides/typage.md
docs/modules/finance_part1.md
docs/modules/finance_part2.md
docs/modules/finance_part3_api_endpoints.md
docs/modules/finance_part3_models.md
docs/modules/finance_part3_support.md
docs/technique/modules/finance.md
docs/modules/comptabilite_part2.md
docs/modules/comptabilite_part3_api.md
src/components/dashboard/RecentActivities.tsx
src/components/dashboard/ProductionChart.tsx
src/components/dashboard/__tests__/ProductionChart.test.tsx
src/components/dashboard/__tests__/RecentActivities.test.tsx
src/components/dashboard/WeatherWidget.tsx
src/components/dashboard/__tests__/WeatherWidget.test.tsx
src/components/finance/__tests__/CashFlowChart.test.tsx
frontend/src/components/comptabilite/BudgetOverview.tsx
docs/modules/projects_ml.md
~/erp_references/analysis/plan_amelioration.md
services/ml/projets/__init__.py
services/ml/analytique/__init__.py
src/services/api.ts
services/ml/projets/service.py
services/ml/projets/base.py
services/ml/production/rendement.py
tests/ml/production/test_rendement.py
tests/ml/production/test_cycle.py
tests/ml/production/test_meteo.py
services/ml/production/cycle.py
services/ml/production/meteo.py
services/ml/production/qualite.py
tests/ml/production/test_qualite.py
services/ml/production/service.py
services/iot_monitoring_service.py
api/v1/endpoints/iot_monitoring.py
models/auth.py
api/v1/__init__.py
frontend/src/main.tsx
frontend/src/env.d.ts
frontend/src/config/axios.ts
frontend/src/components/dashboard/WidgetMeteo.tsx
frontend/src/components/dashboard/DashboardPage.tsx
frontend/src/theme.ts
../../.npm/_logs/2024-11-28T23_38_01_299Z-debug-0.log
frontend
tests/ml/production/test_integration.py
services/ml/production/__init__.py
services/ml/production/base.py
docs/reorganisation/phase1_ml_services.md
services/dashboard_service.py
tests/ml/projets/test_weather.py
tests/ml/projets/test_integration.py
services/projects_ml/optimization.py
services/projects_ml/analysis.py
services/projects_ml/weather.py
services/projects_ml/__init__.py
services/projects_ml_service.py
tests/projects_ml/test_base.py
tests/projects_ml/test_optimization.py
tests/projects_ml/test_analysis.py
tests/projects_ml/test_weather.py
tests/projects_ml/test_integration.py
tests/test_projects_ml_service.py
tests/projects_ml/README.md
docs/modules/projets_ml_tests_mars2024.md
docs/modules/comptabilite_updates.md
docs/modules/inventaire.md
docs/modules/inventaire/index.md
docs/modules/inventaire/ml/index.md
docs/modules/inventaire/ml/models.md
docs/modules/inventaire/ml/integrations.md
docs/modules/inventaire/ml/optimization.md
docs/modules/inventaire/ml/monitoring.md
docs/modules/inventaire/ml/tests.md
services/inventory_ml/config.py
tests/inventory_ml/test_performance.py
~/erp_references/analysis/ameliorations/inventaire_iot.md
models/hr_payroll.py
models/hr_contract.py
schemas/hr_payroll.py
services/hr_payroll_service.py
api/v1/endpoints/hr_payroll.py
docs/api/payroll.md
frontend/src/types/payroll.ts
frontend/src/services/payroll.ts
frontend/src/components/hr/payroll/PayrollList.tsx
frontend/src/components/hr/payroll/PayrollForm.tsx
frontend/src/components/hr/payroll/PayrollPage.tsx
frontend/src/components/hr/payroll/__tests__/PayrollList.test.tsx
frontend/src/components/hr/payroll/__tests__/PayrollForm.test.tsx
frontend/src/components/hr/payroll/__tests__/PayrollPage.test.tsx
tests/test_hr_payroll_service.py
tests/integration/test_hr_payroll_integration.py
tests/e2e/test_hr_payroll_e2e.py
~/erp_references/analysis/rh_module_analysis.md
~/erp_references/analysis/ameliorations/validation.md
docs/technique/modules/inventaire.md
docs/technique/modules/inventaire/frontend/historique_mouvements.md
docs/technique/modules/inventaire/services.md
docs/technique/modules/inventaire/tests.md
docs/technique/modules/inventaire/models.md
docs/technique/modules/inventaire/integrations.md
docs/technique/modules/inventaire/deployment.md
docs/technique/modules/inventaire/index.md
frontend/src/components/inventaire/PageInventaire.tsx
frontend/src/components/inventaire/__tests__/PageInventaire.test.tsx
docs/technique/modules/inventaire/frontend/index.md
schemas/hr_analytics.py
frontend/src/types/hr_analytics.ts
frontend/src/components/hr/analytics/__tests__/HRAnalyticsDashboard.test.tsx
frontend/src/config/queryClient.ts
frontend/src/components/hr/analytics/HRAnalyticsDashboard.tsx
frontend/src/components/hr/components/__tests__/StatCard.test.tsx
frontend/src/services/hr_analytics.ts
docs/plan_developpement_technique.md
docs/technique/index.md
docs/technique/modules/index.md
docs/technique/modules/rh.md
docs/technique/architecture.md
docs/technique/tests.md
docs/technique/standards.md
docs/technique/maintenance.md
docs/technique/modules/production.md
docs/modules/finance_index.md
docs/modules/finance_part3_evolutions.md
docs/modules/finance_comptabilite_integration.md
src/components/common/StatCard.tsx
src/contexts/ThemeModeContext.tsx
src/components/finance/FinanceStats.tsx
src/components/finance/TransactionDetails.tsx
frontend/src/components/comptabilite/CashFlowChart.tsx
frontend/src/components/projects/__tests__/ProjectForm.test.tsx
services/hr_analytics_service.py
api/v1/endpoints/hr_analytics.py
tests/test_hr_analytics_performance.py
docs/guides/hr_weather_integration.md
frontend/src/components/hr/weather/WeatherStatCard.tsx
frontend/src/components/hr/weather/WeatherDashboard.tsx
frontend/src/routes/hr.tsx
frontend/src/components/hr/weather/__tests__/WeatherDashboard.test.tsx
frontend/src/components/hr/weather/__tests__/WeatherStatCard.test.tsx
docs/guides/hr_weather_dashboard.md
~/erp_references/analysis/ameliorations/rh.md
docs/guides/hr_analytics.md
docs/guides/hr_analytics_formation.md
services/dashboard_unified_service.py
api/v1/endpoints/dashboard_unified.py
frontend/src/types/dashboard.ts
frontend/src/components/dashboard/ModuleCard.tsx
frontend/src/components/dashboard/AlertsPanel.tsx
frontend/src/components/common/StatCard.tsx
frontend/src/components/dashboard/StatsInventaire.tsx
frontend/src/components/dashboard/modules/HRModule.tsx
frontend/src/components/dashboard/modules/ProductionModule.tsx
frontend/src/components/dashboard/modules/FinanceModule.tsx
frontend/src/components/dashboard/modules/InventoryModule.tsx
docs/guides/hr_analytics_utilisateur.md
docs/guides/hr_analytics_support_formation.md
~/erp_references/analysis/ameliorations/index.md
docs/tests/guides/ml_inventory.md
~/erp_references/analysis/suivi_analyse.md
frontend/src/components/layout/PageHeader.tsx
frontend/src/components/common/ErrorAlert.tsx
frontend/src/components/inventaire/ListeStock.tsx
frontend/src/components/inventaire/HistoriqueMouvements.tsx
frontend/src/components/projects/TaskWeatherDetails.tsx
frontend/src/components/projects/ProjectStats.tsx
frontend/src/components/projects/__tests__/ProjectStats.test.tsx
frontend/src/components/finance/__tests__/FormulaireTransaction.test.tsx
frontend/src/components/hr/EmployeeStats.tsx
frontend/src/types/hr.ts
frontend/src/components/hr/components/StatCard.tsx
frontend/src/components/hr/EmployeesList.tsx
frontend/src/components/hr/LeaveRequests.tsx
frontend/src/components/hr/AttendanceOverview.tsx
frontend/src/components/hr/components/InfoItem.tsx
frontend/src/types/contract.ts
frontend/src/services/contract.ts
frontend/src/components/hr/ContractForm.tsx
frontend/src/components/hr/ContractList.tsx
frontend/src/components/hr/ContractsPage.tsx
frontend/src/components/hr/__tests__/ContractForm.test.tsx
frontend/src/components/hr/EmployeeDetails.tsx
frontend/src/components/hr/__tests__/ContractList.test.tsx
frontend/src/components/hr/__tests__/ContractsPage.test.tsx
docs/api/contracts.md
tests/integration/test_contract_integration.py
tests/e2e/test_contract_management.py
docs/modules/hr_contract.md
README.md
node_modules/react-hook-form/dist/types/fieldArray.d.ts
frontend/src/components/hr/EmployeeForm.tsx
frontend/src/components/hr/sections/MainInfoSection.tsx
frontend/src/components/hr/sections/FormationSection.tsx
frontend/src/components/hr/sections/AddressSection.tsx
frontend/src/components/hr/constants/employeeConstants.ts
src/components/hr/EmployeesList.tsx
src/components/hr/LeaveRequests.tsx
src/components/hr/AttendanceOverview.tsx
src/components/hr/EmployeeDetails.tsx
src/components/hr/LeaveRequestForm.tsx
src/components/hr/EmployeeForm.tsx
frontend/src/components/inventaire/StatsInventaire.tsx
src/hooks/useAuth.tsx
src/hooks/useThemeMode.ts
src/routes/hr.tsx
src/components/hr/EmployeeStats.tsx
node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts
src/components/hr/HRPage.tsx
src/components/inventaire/StatsInventaire.tsx
src/components/layout/DashboardLayout.tsx
src/components/layout/NotificationCenter.tsx
src/components/inventaire/ListeStock.tsx
src/components/inventaire/HistoriqueMouvements.tsx
src/components/inventaire/PageInventaire.tsx
frontend/src/components/inventory/InventoryPage.tsx
models/inventory.py
services/inventory_ml/__init__.py
services/inventory_ml/base.py
services/ml/inventaire/__init__.py
tests/ml/inventaire/__init__.py
tests/ml/inventaire/test_base.py
tests/ml/inventaire/test_performance.py
tests/ml/inventaire/test_optimization.py
tests/ml/inventaire/test_quality.py
services/inventory_ml_service.py
tests/ml/inventaire/test_integration.py
tests/ml/inventaire/test_analysis.py
~/erp_references/analysis/stocks_module_analysis.md
schemas/inventaire.py
services/inventory_service.py
tests/integration/test_production_inventory_integration.py
tests/integration/test_iot_inventory_integration.py
tests/e2e/test_iot_inventory_dashboard.py
tests/integration/test_hr_service.py
src/services/hr.ts
~/erp_references/analysis/ameliorations/projets_ml.md
~/erp_references/analysis/ameliorations/monitoring_iot.md
~/erp_references/analysis/ameliorations/production.md
~/erp_references/analysis/ameliorations/finance_comptabilite.md
api/v1/endpoints/inventory.py
models/.arena_temp/llm_response2.txt
src/routes/index.tsx
src/routes/ProtectedRoute.tsx
src/services/dashboard.ts
src/components/projects/ProjectStats.tsx
frontend/src/services/projects.ts
problemes build frontend.md
frontend/src/types/production.ts
frontend/src/components/production/__tests__/TableauMeteoParcelleaire.test.tsx
frontend/src/components/production/ParcelleDetails.tsx
frontend/src/components/production/ParcellesList.tsx
frontend/src/components/production/ParcelleForm.tsx
frontend/src/services/production.ts
frontend/src/services/finance.ts
package.json
frontend/src/components/finance/GraphiqueTresorerie.tsx
frontend/src/services/inventaire.ts
tests/integration/test_task_integration.py
frontend/src/components/inventory/StockMovementDialog.tsx
src/components/layout/PageHeader.tsx
frontend/src/components/projects/__tests__/TaskForm.test.tsx
tests/integration/test_task_form_integration.py
tests/e2e/conftest.py
tests/e2e/test_task_management.py
frontend/src/components/projects/TaskForm.tsx
.gitignore
src/components/finance/FinancePage.tsx
frontend/src/components/comptabilite/__tests__/FinanceStats.test.tsx
frontend/src/components/comptabilite/FinanceStats.tsx
~/erp_references/analysis/architecture_notes.md
~/erp_references/analysis/data_models.md
~/erp_references/README.md
~/erp_references/analysis/modules_a_analyser.md
~/erp_references/analysis/plan_analyse.md
~/erp_references/analysis/README.md
~/erp_references/analysis/templates/module_analysis.md
~/erp_references/analysis/templates/integration_analysis.md
~/erp_references/analysis/templates/workflow_analysis.md
~/erp_references/analysis/prompts_analyse.md
~/erp_references/analysis/production_module_analysis.md
api/v1/endpoints/iot.py
frontend/src/types/iot.ts
frontend/src/services/iot.ts
frontend/src/components/production/AddSensorDialog.tsx
frontend/src/components/production/SensorChartsDialog.tsx
frontend/src/components/production/__tests__/IoTDashboard.test.tsx
frontend/src/components/production/__tests__/AddSensorDialog.test.tsx
frontend/src/components/production/__tests__/SensorChartsDialog.test.tsx
frontend/src/components/production/IoTDashboard.tsx
~/erp_references/analysis/finance_module_analysis.md
services/cache_service.py
~/erp_references/analysis/comptabilite_module_analysis.md
~/erp_references/analysis/finance_comptabilite_integration_analysis.md
~/erp_references/analysis/production_stocks_integration_analysis.md
docs/guides/payroll.md
docs/guides/payroll_integration.md
~/erp_references/analysis/projets_module_analysis.md
~/erp_references/analysis/rh_projets_integration_analysis.md
~/erp_references/analysis/analytique_module_analysis.md
~/erp_references/analysis/technique_module_analysis.md
~/erp_references/analysis/analytique_technique_integration_analysis.md
~/erp_references/analysis/rapport_final_synthese.md
~/erp_references/analysis/workflows.md
~/erp_references/analysis/implementation_ideas.md
tests/test_production_report_service.py
tests/test_task_service.py
tests/test_weather_service.py
tsconfig.json
vitest.config.ts
src/test/setup.ts
src/App.tsx
src/index.css
src/main.tsx
src/theme.ts
frontend/components/projects/ProjectDetails.tsx
pyproject.toml
db/database.py
tests/test_iot_monitoring_service.py
docs/api/iot_monitoring.md
api/v1/endpoints/hr_agricole.py
docs/api/hr_agricole.md
frontend/src/types/hr_agricole.ts
frontend/src/test/setup.ts
frontend/src/test/setupPerformance.ts
frontend/src/components/dashboard/__tests__/DashboardPage.perf.tsx
.github/workflows/ci.yml
frontend/src/components/hr/agricole/CompetenceForm.tsx
frontend/src/components/hr/agricole/__tests__/CompetenceForm.test.tsx
frontend/src/components/hr/agricole/CompetencesAgricoles.tsx
frontend/src/components/hr/agricole/__tests__/CompetencesAgricoles.test.tsx
frontend/src/services/__tests__/hr_agricole.test.ts
frontend/src/components/hr/agricole/__tests__/CompetencesList.test.tsx
frontend/src/components/hr/agricole/CompetencesList.tsx
frontend/src/types/weather.ts
frontend/src/components/projects/DétailsMétéoTâche.tsx
frontend/src/components/projects/__tests__/TasksOverview.test.tsx
frontend/src/components/projects/__tests__/TaskWeatherDetails.test.tsx
docs/api/weather.md
docs/guides/task_management.md
frontend/src/services/weather.ts
docs/reorganisation_projet.md
docs/instructions to_do
services/weather_service.py
frontend/.env
frontend/src/components/production/TableauMeteoParcelleaire.tsx
frontend/src/types/comptabilite.ts
frontend/src/components/comptabilite/rapports/Balance.tsx
frontend/package.json
alembic/env.py
core/config.py
alembic.ini
alembic/versions/003_notifications.py
alembic/versions/004_projects.py
alembic/versions/002_parametrage.py
alembic/versions/005_finance.py
alembic/versions/001_1_employes.py
alembic/versions/006_documents.py
frontend/package.json.tmp
api/v1/endpoints/production.py
models/notification.py
core/security.py
models/finance.py
main.py
../../.npm/_logs/2024-11-30T02_34_16_983Z-eresolve-report.txt
models/parametrage.py
schemas/parametrage.py
api/v1/endpoints/parametrage.py
models/iot_sensor.py
services/iot_service.py
schemas/iot_monitoring.py
docs/analyse_doublons.md
frontend/src/components/production/ProductionDashboard.tsx
frontend/src/components/dashboard/UnifiedDashboard.tsx
docs/modules/hr_agricole/index.md
docs/modules/hr_agricole/composants.md
schemas/hr_contract.py
services/hr_contract_service.py
services/hr_service.py
api/v1/endpoints/hr_contract.py
docs/modules/hr_agricole/types.md
docs/modules/hr_agricole/exemples.md
docs/modules/hr_agricole/methodes.md
frontend/components/auth/LoginPage.tsx
services/finance_comptabilite/__init__.py
tests/integration/test_finance_comptabilite_integration.py
docs/modules/comptabilite_index.md
services/finance_comptabilite/analyse.py
services/finance_comptabilite/couts.py
tests/test_finance_comptabilite_couts.py
services/finance_comptabilite/meteo.py
tests/ml/finance_comptabilite/__init__.py
tests/test_finance_comptabilite_meteo.py
services/finance_comptabilite/iot.py
tests/test_finance_comptabilite_iot.py
services/finance_comptabilite/cloture.py
tests/test_finance_comptabilite_cloture.py
services/finance_comptabilite_integration_service.py
services/analytics_cross_module_service.py
api/v1/endpoints/analytics_cross_module.py
docs/api/analytics_cross_module.md
frontend/src/types/analytics_cross_module.ts
frontend/src/services/analytics_cross_module.ts
frontend/src/components/analytics/CrossModuleAnalytics.tsx
frontend/src/components/projects/ProjectForm.tsx
frontend/src/components/analytics/__tests__/ModuleImpactGrid.test.tsx
frontend/src/components/analytics/CorrelationsChart.tsx
frontend/src/components/analytics/MLPredictionsChart.tsx
frontend/src/components/analytics/__tests__/CrossModuleAnalytics.test.tsx
frontend/src/components/analytics/__tests__/CorrelationsChart.test.tsx
frontend/src/components/analytics/__tests__/MLPredictionsChart.test.tsx
frontend/src/components/analytics/ModuleImpactGrid.tsx
frontend/src/components/analytics/RecommendationsList.tsx
tests/integration/test_inventory_finance_integration.py
tests/integration/test_inventory_ml_integration.py
tests/integration/test_inventory_quality_integration.py
docs/tests/README.md
docs/tests/guides/configuration.md
docs/tests/guides/react.md
docs/tests/guides/e2e.md
docs/tests/guides/best_practices.md
docs/tests/guides/ml.md
docs/tests/guides/maintenance.md
docs/tests.md
tests/test_finance_comptabilite_integration.py
tests/test_comptabilite_stats_service.py
tests/test_finance_comptabilite_analyse.py
services/comptabilite_stats_service.py
models/base.py
models/document.py
models/production.py
schemas/activity.py
tests/test_production_ml_service.py
services/production_service.py
docs/modules/production_ml.md
services/project_service.py
tests/test_project_service.py
services/finance_service.py
tests/test_finance_service.py
services/comptabilite_service.py
tests/integration/test_comptabilite_integration.py
tests/e2e/test_comptabilite_e2e.py
models/.arena_temp/llm_response1.txt
models/__init__.py
vite.config.ts
src/config/queryClient.ts
src/types/finance.ts
package-lock.json
.gitattributes
models/hr_agricole.py
models/hr.py
schemas/hr_agricole.py
services/hr_agricole_service.py
tsconfig.node.json
.flake8
src/types/inventaire.ts
src/services/inventaire.ts
src/components/inventaire/DetailsProduit.tsx
src/components/inventaire/DialogueMouvementStock.tsx
../../../../var/folders/29/p26vn3vd0rb5zsgndkkgwtx00000gn/T/temp_image_1732932217482.webp
docs/diagrammes/db_schema.md
docs/diagrammes/infrastructure.md
docs/diagrammes/flux_projets.md
tests/test_inventory_service.py
frontend/src/i18n.ts
frontend/src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx
docs/reorganisation/phase1_inventaire.md
services/ml/core/__init__.py
services/ml/core/base.py
services/ml/inventaire/base.py
services/ml/core/types.py
services/ml/core/config.py
frontend/src/routes/inventaire.tsx
frontend/src/types/auth.ts
frontend/src/hooks/useAuth.tsx
frontend/src/components/auth/ProtectedRoute.tsx
frontend/src/components/finance/FormulaireTransaction.tsx
frontend/src/components/finance/__tests__/ListeTransactions.test.tsx
frontend/src/components/finance/ListeTransactions.tsx
frontend/src/routes/finance.tsx
frontend/src/components/finance/__tests__/StatsFinance.test.tsx
frontend/src/components/finance/PageFinance.tsx
frontend/src/components/finance/ProjectionsFinancieres.tsx
frontend/src/components/finance/__tests__/ProjectionsFinancieres.test.tsx
frontend/src/components/finance/__tests__/GraphiqueTresorerie.test.tsx
tests/test_dashboard.py
tests/ml/test_ml_dashboard.py
frontend/src/components/production/TableauMeteo.tsx
frontend/src/components/production/__tests__/TableauMeteo.test.tsx
frontend/src/components/dashboard/__tests__/StatsProduction.test.tsx
frontend/src/types/finance.ts
frontend/src/components/dashboard/StatsFinance.tsx
frontend/src/components/finance/__tests__/PageFinance.test.tsx
frontend/src/components/dashboard/__tests__/StatsFinance.test.tsx
frontend/src/services/rh.ts
frontend/src/components/dashboard/StatsRH.tsx
frontend/src/components/dashboard/__tests__/StatsRH.test.tsx
frontend/src/components/dashboard/modules/WeatherModule.tsx
frontend/src/components/dashboard/__tests__/WidgetMeteo.test.tsx
frontend/src/components/dashboard/ActivitesRecentes.tsx
frontend/src/components/dashboard/__tests__/ActivitesRecentes.test.tsx
frontend/src/components/dashboard/GraphiqueProduction.tsx
frontend/src/components/dashboard/__tests__/GraphiqueProduction.test.tsx
frontend/src/components/dashboard/GraphiqueTresorerie.tsx
frontend/src/components/dashboard/__tests__/GraphiqueTresorerie.test.tsx
../../../../Untitled-1
src/components/inventaire/.arena_temp/llm_response2.txt
src/components/inventaire/FormulaireProduit.tsx
frontend/src/types/task.ts
docs/api/finance.md
frontend/src/routes/ProtectedRoute.tsx
frontend/src/components/finance/VueBudget.tsx
frontend/src/components/finance/__tests__/VueBudget.test.tsx
frontend/src/components/finance/BudgetAnalysis.tsx
frontend/src/components/finance/AnalyseBudget.tsx
frontend/src/components/finance/__tests__/AnalyseBudget.test.tsx
frontend/src/components/finance/FinancialProjections.tsx
models/comptabilite.py
api/v1/endpoints/comptabilite.py
docs/api/comptabilite.md
frontend/src/components/comptabilite/ComptabilitePage.tsx
frontend/src/components/comptabilite/__tests__/BudgetOverview.test.tsx
frontend/src/components/comptabilite/__tests__/Balance.test.tsx
docs/modules/comptabilite_part1.md
frontend/src/components/comptabilite/__tests__/CashFlowChart.test.tsx
</environment_details>

Le fichier problemes build frontend.md est vide, ce qui indique que les problèmes de build n'ont pas été documentés.

Les erreurs de build indiquent des problèmes d'importation dans les fichiers TypeScript du frontend. Plus précisément, certains types ou interfaces ne sont pas exportés correctement depuis les fichiers src/types/inventaire.ts et src/types/production.ts.

Voici les erreurs spécifiques :

No matching export in "src/types/inventaire.ts" for import "SeuilStock" dans src/components/inventaire/StatsInventaire.tsx
No matching export in "src/types/production.ts" for import "QualiteRecolte" dans src/components/production/ParcelleDetails.tsx
No matching export in "src/types/production.ts" for import "CultureType" dans src/components/production/ParcellesList.tsx
No matching export in "src/types/production.ts" for import "ParcelleStatus" dans src/components/production/ParcellesList.tsx
No matching export in "src/types/production.ts" for import "CultureType" dans src/components/production/ProductionStats.tsx
Pour résoudre ces problèmes, il faut :

Examiner les fichiers src/types/inventaire.ts et src/types/production.ts pour vérifier si les types mentionnés dans les erreurs sont définis et exportés.
Si les types ne sont pas définis, les ajouter.
Si les types sont définis mais ne sont pas exportés, ajouter le mot-clé export devant leur déclaration.
Enregistrer les modifications dans les fichiers src/types/inventaire.ts et src/types/production.ts.
Relancer le build pour vérifier si les erreurs ont été corrigées.
Je vais commencer par lire les fichiers src/types/inventaire.ts et src/types/production.ts.


Cline read this file:


je t'ai interrompu parceque certains problemes du fichier ont deja été résolus. le fichier n'est pas à jour . IL faudrait de nouveau executer la commande build frontend pour voir les problemes qui persistent


L'utilisateur a interrompu la tâche précédente car certains problèmes de build du frontend ont déjà été résolus. Il demande de réexécuter la commande de build pour identifier les problèmes persistants.

La dernière action effectuée était la lecture du fichier frontend/src/types/inventaire.ts. Comme l'utilisateur indique que le fichier n'est pas à jour, il n'est pas pertinent de continuer à analyser ce fichier pour le moment.

Au lieu de cela, je vais suivre la demande de l'utilisateur et exécuter la commande de build du frontend pour identifier les problèmes restants.

La commande de build du frontend est généralement npm run build ou npm run dev dans le dossier frontend. Je vais d'abord vérifier le fichier package.json du frontend pour confirmer la commande exacte.

Ensuite, j'exécuterai la commande dans le dossier frontend et j'analyserai les messages d'erreur pour identifier les problèmes de build restants.


Cline read this file:


Le fichier frontend/package.json indique que la commande de build est vite build et la commande de développement est vite.

L'utilisateur demande d'exécuter la commande de build du frontend pour identifier les problèmes de build restants.

Je vais donc exécuter la commande npm run dev dans le dossier frontend.


Cline wants to execute this command:
cd frontend && npm run dev
Command Output

cette commande ne permet pas d'obtenir les logs des pbs de buil . Quand je clique sur le lien lapage est vierge


L'utilisateur signale que la commande npm run dev dans le dossier frontend ne fournit pas les logs des problèmes de build et que la page est vierge lorsqu'il clique sur le lien.

Cela suggère que la commande npm run dev lance un serveur de développement qui ne compile pas le code de la même manière que la commande de build. Pour obtenir les logs de build, il faut utiliser la commande npm run build.

Je vais donc exécuter la commande npm run build dans le dossier frontend pour obtenir les logs de build et identifier les problèmes restants.


Cline wants to execute this command:
cd frontend && npm run build
Command Output
> fofal-erp@0.1.0 build
> tsc && vite build
src/components/analytics/__tests__/ModuleImpactGrid.test.tsx:13:5 - error TS2353: Object literal may only specify known properties and 'impact' does not exist in type 'Activity'.
13     impact: 'HIGH'
       ~~~~~~
src/components/comptabilite/__tests__/BudgetOverview.test.tsx:6:10 - error TS2305: Module '"../../../services/comptabilite"' has no exported member 'comptabiliteService'.
6 import { comptabiliteService } from '../../../services/comptabilite';
           ~~~~~~~~~~~~~~~~~~~
src/components/comptabilite/__tests__/CashFlowChart.test.tsx:6:10 - error TS2305: Module '"../../../services/comptabilite"' has no exported member 'comptabiliteService'.
6 import { comptabiliteService } from '../../../services/comptabilite';
           ~~~~~~~~~~~~~~~~~~~
src/components/comptabilite/ComptabilitePage.tsx:2:32 - error TS6133: 'Typography' is declared but its value is never read.
2 import { Grid Box Tabs Tab Typography } from '@mui/material';
                                 ~~~~~~~~~~
src/components/comptabilite/ComptabilitePage.tsx:54:28 - error TS6133: 'event' is declared but its value is never read.
54   const handleTabChange = (event: React.SyntheticEvent newValue: number) => {
                              ~~~~~
src/components/comptabilite/ComptesList.tsx:20:16 - error TS6133: 'Delete' is declared but its value is never read.
20 import { Edit Delete } from '@mui/icons-material';
                  ~~~~~~
src/components/comptabilite/ComptesList.tsx:21:27 - error TS2305: Module '"../../types/comptabilite"' has no exported member 'TypeCompte'.
21 import { CompteComptable TypeCompte CompteComptableFormData } from '../../types/comptabilite';
                             ~~~~~~~~~~
src/components/comptabilite/ComptesList.tsx:21:27 - error TS6133: 'TypeCompte' is declared but its value is never read.
21 import { CompteComptable TypeCompte CompteComptableFormData } from '../../types/comptabilite';
                             ~~~~~~~~~~
src/components/comptabilite/ComptesList.tsx:34:5 - error TS2322: Type '"ACTIF"' is not assignable to type 'TypeCompteComptable'.
34     type_compte: 'ACTIF'
       ~~~~~~~~~~~
src/components/comptabilite/ComptesList.tsx:65:9 - error TS2322: Type '"ACTIF"' is not assignable to type 'TypeCompteComptable'.
65         type_compte: 'ACTIF'
           ~~~~~~~~~~~
src/components/comptabilite/ComptesList.tsx:132:65 - error TS2339: Property 'solde_debit' does not exist on type 'CompteComptable'.
132                 <TableCell align="right">{formatCurrency(compte.solde_debit)}</TableCell>
                                                                    ~~~~~~~~~~~
src/components/comptabilite/ComptesList.tsx:133:65 - error TS2339: Property 'solde_credit' does not exist on type 'CompteComptable'.
133                 <TableCell align="right">{formatCurrency(compte.solde_credit)}</TableCell>
                                                                    ~~~~~~~~~~~~
src/components/comptabilite/EcrituresForm.tsx:20:3 - error TS6133: 'EcritureComptableFormData' is declared but its value is never read.
20   EcritureComptableFormData
     ~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/comptabilite/EcrituresForm.tsx:130:11 - error TS2353: Object literal may only specify known properties and 'numero_piece' does not exist in type 'EcritureComptableFormData'.
130           numero_piece
              ~~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:17:3 - error TS6133: 'MenuItem' is declared but its value is never read.
17   MenuItem
     ~~~~~~~~
src/components/comptabilite/JournauxList.tsx:22:10 - error TS6133: 'Edit' is declared but its value is never read.
22 import { Edit Visibility } from '@mui/icons-material';
            ~~~~
src/components/comptabilite/JournauxList.tsx:23:28 - error TS2305: Module '"../../types/comptabilite"' has no exported member 'TypeJournal'.
23 import { JournalComptable TypeJournal EcritureComptable } from '../../types/comptabilite';
                              ~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:23:28 - error TS6133: 'TypeJournal' is declared but its value is never read.
23 import { JournalComptable TypeJournal EcritureComptable } from '../../types/comptabilite';
                              ~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:27:7 - error TS6133: 'TYPES_JOURNAL' is declared but its value is never read.
27 const TYPES_JOURNAL = ['ACHAT' 'VENTE' 'BANQUE' 'CAISSE' 'OPERATIONS_DIVERSES'] as const;
         ~~~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:59:49 - error TS2554: Expected 1 arguments but got 3.
59       const data = await getJournal(journal.id dateDebut dateFin);
                                                   ~~~~~~~~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:60:20 - error TS2345: Argument of type 'JournalComptable' is not assignable to parameter of type 'SetStateAction<EcritureComptable[]>'.
60       setEcritures(data);
                      ~~~~
src/components/comptabilite/JournauxList.tsx:76:59 - error TS2554: Expected 1 arguments but got 3.
76         const data = await getJournal(selectedJournal.id dateDebut dateFin);
                                                             ~~~~~~~~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:77:22 - error TS2345: Argument of type 'JournalComptable' is not assignable to parameter of type 'SetStateAction<EcritureComptable[]>'.
77         setEcritures(data);
                        ~~~~
src/components/comptabilite/JournauxList.tsx:87:37 - error TS2339: Property 'debit' does not exist on type 'EcritureComptable'.
87         debit: acc.debit + ecriture.debit
                                       ~~~~~
src/components/comptabilite/JournauxList.tsx:88:39 - error TS2339: Property 'credit' does not exist on type 'EcritureComptable'.
88         credit: acc.credit + ecriture.credit
                                         ~~~~~~
src/components/comptabilite/JournauxList.tsx:111:37 - error TS2339: Property 'type_journal' does not exist on type 'JournalComptable'.
111                 <TableCell>{journal.type_journal}</TableCell>
                                        ~~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:184:42 - error TS2339: Property 'numero_piece' does not exist on type 'EcritureComptable'.
184                     <TableCell>{ecriture.numero_piece}</TableCell>
                                             ~~~~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:185:42 - error TS2339: Property 'compte_id' does not exist on type 'EcritureComptable'.
185                     <TableCell>{ecriture.compte_id}</TableCell>
                                             ~~~~~~~~~
src/components/comptabilite/JournauxList.tsx:186:42 - error TS2339: Property 'libelle' does not exist on type 'EcritureComptable'.
186                     <TableCell>{ecriture.libelle}</TableCell>
                                             ~~~~~~~
src/components/comptabilite/JournauxList.tsx:187:71 - error TS2339: Property 'debit' does not exist on type 'EcritureComptable'.
187                     <TableCell align="right">{formatCurrency(ecriture.debit)}</TableCell>
                                                                          ~~~~~
src/components/comptabilite/JournauxList.tsx:188:71 - error TS2339: Property 'credit' does not exist on type 'EcritureComptable'.
188                     <TableCell align="right">{formatCurrency(ecriture.credit)}</TableCell>
                                                                          ~~~~~~
src/components/comptabilite/rapports/Bilan.tsx:17:10 - error TS2305: Module '"../../../types/comptabilite"' has no exported member 'Bilan'.
17 import { Bilan as BilanType } from '../../../types/comptabilite';
            ~~~~~
src/components/comptabilite/rapports/Bilan.tsx:31:35 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'Date'.
31       const data = await getBilan(dateFin);
                                     ~~~~~~~
src/components/comptabilite/rapports/CompteResultat.tsx:17:10 - error TS2305: Module '"../../../types/comptabilite"' has no exported member 'CompteResultat'.
17 import { CompteResultat as CompteResultatType } from '../../../types/comptabilite';
            ~~~~~~~~~~~~~~
src/components/comptabilite/rapports/CompteResultat.tsx:36:44 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'Date'.
36       const data = await getCompteResultat(dateDebut dateFin);
                                              ~~~~~~~~~
src/components/comptabilite/rapports/GrandLivre.tsx:20:32 - error TS2724: '"../../../types/comptabilite"' has no exported member named 'LigneGrandLivre'. Did you mean 'GrandLivre'?
20 import type { CompteComptable LigneGrandLivre } from '../../../types/comptabilite';
                                  ~~~~~~~~~~~~~~~
src/components/comptabilite/rapports/GrandLivre.tsx:46:49 - error TS2554: Expected 0 arguments but got 1.
 46     queryKey: queryKeys.comptabilite.grandLivre({
                                                    ~
 47       compte_id: selectedCompte
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
...
 49       date_fin: dateFin
    ~~~~~~~~~~~~~~~~~~~~~~~
 50     })
    ~~~~~
src/components/dashboard/__tests__/ActivitesRecentes.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/DashboardPage.perf.tsx:23:7 - error TS6133: 'wrapper' is declared but its value is never read.
23 const wrapper = ({ children }: { children: React.ReactNode }) => (
         ~~~~~~~
src/components/dashboard/__tests__/FinanceStats.test.tsx:11:7 - error TS2739: Type '{ revenue: number; revenueVariation: { value: number; type: "increase"; }; expenses: number; expensesVariation: { value: number; type: "decrease"; }; profit: number; profitVariation: { value: number; type: "increase"; }; cashflow: number; cashflowVariation: { ...; }; }' is missing the following properties from type 'FinanceStats': tresorerie variation_tresorerie factures_impayees paiements_prevus
11 const mockStats: FinanceStatsType = {
         ~~~~~~~~~
src/components/dashboard/__tests__/InventoryStats.test.tsx:4:28 - error TS2307: Cannot find module '../InventoryStats' or its corresponding type declarations.
4 import InventoryStats from '../InventoryStats';
                             ~~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/InventoryStats.test.tsx:5:35 - error TS2307: Cannot find module '../../../services/inventory' or its corresponding type declarations.
5 import { getInventoryStats } from '../../../services/inventory';
                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/MLDashboard.test.tsx:4:25 - error TS2307: Cannot find module '../MLDashboard' or its corresponding type declarations.
4 import MLDashboard from '../MLDashboard'
                          ~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/MLDashboard.test.tsx:5:10 - error TS2724: '"../../../services/dashboard"' has no exported member named 'dashboardService'. Did you mean 'DashboardService'?
5 import { dashboardService } from '../../../services/dashboard'
           ~~~~~~~~~~~~~~~~
  src/services/dashboard.ts:6:14
    6 export const DashboardService = {
                   ~~~~~~~~~~~~~~~~
    'DashboardService' is declared here.
src/components/dashboard/__tests__/StatsFinance.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/StatsFinance.test.tsx:20:9 - error TS2322: Type '"hausse"' is not assignable to type '"increase" | "decrease"'.
20         type: 'hausse'
           ~~~~
  src/types/finance.ts:3:3
    3   type: 'increase' | 'decrease';
        ~~~~
    The expected type comes from property 'type' which is declared here on type 'Variation'
src/components/dashboard/__tests__/StatsFinance.test.tsx:55:9 - error TS2322: Type '"baisse"' is not assignable to type '"increase" | "decrease"'.
55         type: 'baisse'
           ~~~~
  src/types/finance.ts:3:3
    3   type: 'increase' | 'decrease';
        ~~~~
    The expected type comes from property 'type' which is declared here on type 'Variation'
src/components/dashboard/__tests__/StatsProduction.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/StatsProduction.test.tsx:6:10 - error TS2614: Module '"../../../services/production"' has no exported member 'getStatsProduction'. Did you mean to use 'import getStatsProduction from "../../../services/production"' instead?
6 import { getStatsProduction } from '../../../services/production';
           ~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/StatsRH.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/WidgetMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/dashboard/__tests__/WidgetMeteo.test.tsx:25:9 - error TS2353: Object literal may only specify known properties and 'timestamp' does not exist in type 'WeatherCondition'.
25         timestamp: new Date().toISOString()
           ~~~~~~~~~
src/components/dashboard/AlertsPanel.tsx:38:7 - error TS6133: 'getSeverityColor' is declared but its value is never read.
38 const getSeverityColor = (severity: 'low' | 'medium' | 'high') => {
         ~~~~~~~~~~~~~~~~
src/components/dashboard/FinanceStats.tsx:7:53 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(queryKey: "finance-stats" options?: Omit<UseQueryOptions<unknown unknown unknown "finance-stats"> "queryKey"> | undefined): UseQueryResult<unknown unknown>' gave the following error.
    Type '(periode?: string | undefined) => Promise<FinanceStats>' has no properties in common with type 'Omit<UseQueryOptions<unknown unknown unknown "finance-stats"> "queryKey">'.
  Overload 2 of 3 '(queryKey: "finance-stats" queryFn: QueryFunction<FinanceStats "finance-stats"> options?: Omit<UseQueryOptions<FinanceStats unknown FinanceStats "finance-stats"> "queryKey" | "queryFn"> | undefined): UseQueryResult<...>' gave the following error.
    Argument of type '(periode?: string) => Promise<FinanceStats>' is not assignable to parameter of type 'QueryFunction<FinanceStats "finance-stats">'.
      Types of parameters 'periode' and 'context' are incompatible.
        Type 'QueryFunctionContext<"finance-stats" any>' is not assignable to type 'string'.
7   const { data: stats } = useQuery('finance-stats' getFinanceStats);
                                                      ~~~~~~~~~~~~~~~
src/components/dashboard/FinanceStats.tsx:29:36 - error TS2339: Property 'recettes' does not exist on type '{}'.
29             {formatCurrency(stats?.recettes || 0)}
                                      ~~~~~~~~
src/components/dashboard/FinanceStats.tsx:31:19 - error TS2339: Property 'variation' does not exist on type '{}'.
31           {stats?.variation && (
                     ~~~~~~~~~
src/components/dashboard/FinanceStats.tsx:34:28 - error TS2339: Property 'variation' does not exist on type '{}'.
34               color={stats.variation.type === 'increase' ? 'success.main' : 'error.main'}
                              ~~~~~~~~~
src/components/dashboard/FinanceStats.tsx:36:22 - error TS2339: Property 'variation' does not exist on type '{}'.
36               {stats.variation.type === 'increase' ? '+' : '-'}
                        ~~~~~~~~~
src/components/dashboard/FinanceStats.tsx:37:22 - error TS2339: Property 'variation' does not exist on type '{}'.
37               {stats.variation.value}% ce mois
                        ~~~~~~~~~
src/components/dashboard/FinanceStats.tsx:48:27 - error TS2339: Property 'solde' does not exist on type '{}'.
48             color={stats?.solde && stats.solde >= 0 ? 'success.main' : 'error.main'}
                             ~~~~~
src/components/dashboard/FinanceStats.tsx:48:42 - error TS2339: Property 'solde' does not exist on type '{}'.
48             color={stats?.solde && stats.solde >= 0 ? 'success.main' : 'error.main'}
                                            ~~~~~
src/components/dashboard/FinanceStats.tsx:50:36 - error TS2339: Property 'solde' does not exist on type '{}'.
50             {formatCurrency(stats?.solde || 0)}
                                      ~~~~~
src/components/dashboard/HRStats.tsx:21:21 - error TS2339: Property 'effectif_total' does not exist on type 'EmployeeStats'.
21             {stats?.effectif_total || 0}
                       ~~~~~~~~~~~~~~
src/components/dashboard/HRStats.tsx:27:30 - error TS2339: Property 'en_conge' does not exist on type 'EmployeeStats'.
27             label={`${stats?.en_conge || 0} En congé`}
                                ~~~~~~~~
src/components/dashboard/HRStats.tsx:32:30 - error TS2339: Property 'presents' does not exist on type 'EmployeeStats'.
32             label={`${stats?.presents || 0} Présents`}
                                ~~~~~~~~
src/components/dashboard/ModuleCard.tsx:20:3 - error TS6133: 'module' is declared but its value is never read.
20   module
     ~~~~~~
src/components/dashboard/modules/InventoryModule.tsx:15:9 - error TS6133: 'formatCurrency' is declared but its value is never read.
15   const formatCurrency = (amount: number) => {
           ~~~~~~~~~~~~~~
src/components/dashboard/StatisticsCards.tsx:6:10 - error TS2614: Module '"../../services/dashboard"' has no exported member 'getDashboardStats'. Did you mean to use 'import getDashboardStats from "../../services/dashboard"' instead?
6 import { getDashboardStats } from '../../services/dashboard';
           ~~~~~~~~~~~~~~~~~
src/components/dashboard/StatisticsCards.tsx:16:25 - error TS2339: Property 'production' does not exist on type '{}'.
16           value={stats?.production.total || 0}
                           ~~~~~~~~~~
src/components/dashboard/StatisticsCards.tsx:18:29 - error TS2339: Property 'production' does not exist on type '{}'.
18           variation={stats?.production.variation}
                               ~~~~~~~~~~
src/components/dashboard/StatisticsCards.tsx:27:25 - error TS2339: Property 'inventory' does not exist on type '{}'.
27           value={stats?.inventory.value || 0}
                           ~~~~~~~~~
src/components/dashboard/StatisticsCards.tsx:29:29 - error TS2339: Property 'inventory' does not exist on type '{}'.
29           variation={stats?.inventory.variation}
                               ~~~~~~~~~
src/components/dashboard/StatisticsCards.tsx:38:25 - error TS2339: Property 'finance' does not exist on type '{}'.
38           value={stats?.finance.revenue || 0}
                           ~~~~~~~
src/components/dashboard/StatisticsCards.tsx:40:29 - error TS2339: Property 'finance' does not exist on type '{}'.
40           variation={stats?.finance.variation}
                               ~~~~~~~
src/components/dashboard/StatisticsCards.tsx:49:25 - error TS2339: Property 'hr' does not exist on type '{}'.
49           value={stats?.hr.activeEmployees || 0}
                           ~~
src/components/dashboard/StatisticsCards.tsx:50:29 - error TS2339: Property 'hr' does not exist on type '{}'.
50           variation={stats?.hr.variation}
                               ~~
src/components/dashboard/StatsProduction.tsx:4:10 - error TS2614: Module '"../../services/production"' has no exported member 'getStatsProduction'. Did you mean to use 'import getStatsProduction from "../../services/production"' instead?
4 import { getStatsProduction } from '../../services/production';
           ~~~~~~~~~~~~~~~~~~
src/components/dashboard/StatsProduction.tsx:28:21 - error TS2339: Property 'total' does not exist on type 'ProductionStats'.
28             {stats?.total || 0} T
                       ~~~~~
src/components/dashboard/StatsProduction.tsx:30:19 - error TS2339: Property 'variation' does not exist on type 'ProductionStats'.
30           {stats?.variation && (
                     ~~~~~~~~~
src/components/dashboard/StatsProduction.tsx:33:28 - error TS2339: Property 'variation' does not exist on type 'ProductionStats'.
33               color={stats.variation.type === 'increase' ? 'success.main' : 'error.main'}
                              ~~~~~~~~~
src/components/dashboard/StatsProduction.tsx:35:22 - error TS2339: Property 'variation' does not exist on type 'ProductionStats'.
35               {stats.variation.type === 'increase' ? '+' : '-'}
                        ~~~~~~~~~
src/components/dashboard/StatsProduction.tsx:36:22 - error TS2339: Property 'variation' does not exist on type 'ProductionStats'.
36               {stats.variation.value}% par rapport au mois dernier
                        ~~~~~~~~~
src/components/dashboard/StatsProduction.tsx:43:40 - error TS2339: Property 'parcellesActives' does not exist on type 'ProductionStats'.
43             Parcelles Actives: {stats?.parcellesActives || 0}
                                          ~~~~~~~~~~~~~~~~
src/components/dashboard/StatsProduction.tsx:47:28 - error TS2339: Property 'parcellesActives' does not exist on type 'ProductionStats'.
47             value={(stats?.parcellesActives || 0) / 70 * 100}
                              ~~~~~~~~~~~~~~~~
src/components/documents/__tests__/DocumentList.test.tsx:5:30 - error TS2306: File '/Users/cherylmaevahfodjo/ERP/ERP/frontend/src/services/documents.ts' is not a module.
5 import { getDocuments } from '../../../services/documents';
                               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/documents/__tests__/DocumentUploadDialog.test.tsx:5:32 - error TS2306: File '/Users/cherylmaevahfodjo/ERP/ERP/frontend/src/services/documents.ts' is not a module.
5 import { uploadDocument } from '../../../services/documents';
                                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/documents/DocumentList.tsx:20:46 - error TS2306: File '/Users/cherylmaevahfodjo/ERP/ERP/frontend/src/services/documents.ts' is not a module.
20 import { getDocuments deleteDocument } from '../../services/documents';
                                                ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/documents/DocumentList.tsx:35:28 - error TS6133: 'isLoading' is declared but its value is never read.
35   const { data: documents isLoading } = useQuery(
                              ~~~~~~~~~
src/components/documents/DocumentList.tsx:46:47 - error TS7006: Parameter 'doc' implicitly has an 'any' type.
46   const filteredDocuments = documents?.filter(doc =>
                                                 ~~~
src/components/documents/DocumentList.tsx:57:29 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'void'.
57       deleteMutation.mutate(id);
                               ~~
src/components/documents/DocumentList.tsx:110:38 - error TS7006: Parameter 'doc' implicitly has an 'any' type.
110             {filteredDocuments?.map((doc) => (
                                         ~~~
src/components/documents/DocumentUploadDialog.tsx:14:29 - error TS2307: Cannot find module 'react-dropzone' or its corresponding type declarations.
14 import { useDropzone } from 'react-dropzone';
                               ~~~~~~~~~~~~~~~~
src/components/documents/DocumentUploadDialog.tsx:16:32 - error TS2306: File '/Users/cherylmaevahfodjo/ERP/ERP/frontend/src/services/documents.ts' is not a module.
16 import { uploadDocument } from '../../services/documents';
                                  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/documents/DocumentUploadDialog.tsx:38:14 - error TS7006: Parameter 'acceptedFiles' implicitly has an 'any' type.
38     onDrop: (acceptedFiles) => {
                ~~~~~~~~~~~~~
src/components/documents/DocumentUploadDialog.tsx:63:23 - error TS2345: Argument of type 'FormData' is not assignable to parameter of type 'void'.
63       mutation.mutate(formData);
                         ~~~~~~~~
src/components/finance/__tests__/AnalyseBudget.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/AnalyseBudget.test.tsx:62:44 - error TS2345: Argument of type '{ total_prevu: number; total_realise: number; categories: { Équipement: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; Personnel: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; }; impact_meteo: { ...; }; recommandations: string[]; }' is not assignable to parameter of type 'AnalyseBudgetaire | Promise<AnalyseBudgetaire>'.
  Type '{ total_prevu: number; total_realise: number; categories: { Équipement: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; Personnel: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; }; impact_meteo: { ...; }; recommandations: string[]; }' is missing the following properties from type 'AnalyseBudgetaire': periode total alertes
62     mockGetAnalyseBudget.mockResolvedValue(mockAnalyse);
                                              ~~~~~~~~~~~
src/components/finance/__tests__/AnalyseBudget.test.tsx:137:48 - error TS2345: Argument of type '{ total_prevu: number; total_realise: number; categories: {}; impact_meteo: { score: number; facteurs: never[]; projections: {}; }; recommandations: never[]; }' is not assignable to parameter of type 'AnalyseBudgetaire | Promise<AnalyseBudgetaire>'.
  Type '{ total_prevu: number; total_realise: number; categories: {}; impact_meteo: { score: number; facteurs: never[]; projections: {}; }; recommandations: never[]; }' is missing the following properties from type 'AnalyseBudgetaire': periode total alertes
137     mockGetAnalyseBudget.mockResolvedValueOnce(emptyAnalyse);
                                                   ~~~~~~~~~~~~
src/components/finance/__tests__/BudgetOverview.test.tsx:4:28 - error TS2307: Cannot find module '../BudgetOverview' or its corresponding type declarations.
4 import BudgetOverview from '../BudgetOverview';
                             ~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/BudgetOverview.test.tsx:5:10 - error TS2614: Module '"../../../services/finance"' has no exported member 'getBudgetOverview'. Did you mean to use 'import getBudgetOverview from "../../../services/finance"' instead?
5 import { getBudgetOverview } from '../../../services/finance';
           ~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/FinancePage.test.tsx:5:25 - error TS2307: Cannot find module '../FinancePage' or its corresponding type declarations.
5 import FinancePage from '../FinancePage';
                          ~~~~~~~~~~~~~~~~
src/components/finance/__tests__/FormulaireTransaction.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:10 - error TS2724: '"../../../services/finance"' has no exported member named 'creerTransaction'. Did you mean 'createTransaction'?
10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
            ~~~~~~~~~~~~~~~~
  src/services/finance.ts:40:14
    40 export const createTransaction = async (data: TransactionFormData): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~~~~
    'createTransaction' is declared here.
src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:28 - error TS2614: Module '"../../../services/finance"' has no exported member 'modifierTransaction'. Did you mean to use 'import modifierTransaction from "../../../services/finance"' instead?
10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                              ~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:28 - error TS6133: 'modifierTransaction' is declared but its value is never read.
10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                              ~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:49 - error TS6133: 'getTransaction' is declared but its value is never read.
10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                                                   ~~~~~~~~~~~~~~
src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:65 - error TS2614: Module '"../../../services/finance"' has no exported member 'getComptes'. Did you mean to use 'import getComptes from "../../../services/finance"' instead?
10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                                                                   ~~~~~~~~~~
src/components/finance/__tests__/FormulaireTransaction.test.tsx:11:28 - error TS2305: Module '"../../../types/finance"' has no exported member 'Compte'.
11 import type { Transaction Compte } from '../../../types/finance';
                              ~~~~~~
src/components/finance/__tests__/GraphiqueTresorerie.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/GraphiqueTresorerie.test.tsx:25:48 - error TS2345: Argument of type '{ labels: string[]; recettes: number[]; depenses: number[]; }' is not assignable to parameter of type 'DonneesTresorerie | Promise<DonneesTresorerie>'.
25     mockGetDonneesTresorerie.mockResolvedValue(mockData);
                                                  ~~~~~~~~
src/components/finance/__tests__/ListeTransactions.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/ListeTransactions.test.tsx:7:27 - error TS2724: '"../../../services/finance"' has no exported member named 'TypeTransaction'. Did you mean 'getTransaction'?
7 import { getTransactions TypeTransaction StatutTransaction } from '../../../services/finance';
                            ~~~~~~~~~~~~~~~
  src/services/finance.ts:35:14
    35 export const getTransaction = async (id: UUID): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~
    'getTransaction' is declared here.
src/components/finance/__tests__/ListeTransactions.test.tsx:7:44 - error TS2614: Module '"../../../services/finance"' has no exported member 'StatutTransaction'. Did you mean to use 'import StatutTransaction from "../../../services/finance"' instead?
7 import { getTransactions TypeTransaction StatutTransaction } from '../../../services/finance';
                                             ~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/ListeTransactions.test.tsx:43:43 - error TS2345: Argument of type '{ id: string; date: string; reference: string; description: string; montant: number; type: TypeTransaction; statut: StatutTransaction; categorie: string; }[]' is not assignable to parameter of type 'TransactionListResponse | Promise<TransactionListResponse>'.
43     mockGetTransactions.mockResolvedValue(mockTransactions);
                                             ~~~~~~~~~~~~~~~~
src/components/finance/__tests__/ListeTransactions.test.tsx:89:47 - error TS2345: Argument of type 'never[]' is not assignable to parameter of type 'TransactionListResponse | Promise<TransactionListResponse>'.
89     mockGetTransactions.mockResolvedValueOnce([]);
                                                 ~~
src/components/finance/__tests__/PageFinance.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/ProjectionsFinancieres.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/StatsFinance.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/StatsFinance.test.tsx:30:43 - error TS2345: Argument of type '{ revenue: number; revenueVariation: { value: number; type: "increase"; }; profit: number; profitVariation: { value: number; type: "increase"; }; cashflow: number; cashflowVariation: { value: number; type: "decrease"; }; expenses: number; expensesVariation: { ...; }; }' is not assignable to parameter of type 'FinanceStats | Promise<FinanceStats>'.
  Type '{ revenue: number; revenueVariation: { value: number; type: "increase"; }; profit: number; profitVariation: { value: number; type: "increase"; }; cashflow: number; cashflowVariation: { value: number; type: "decrease"; }; expenses: number; expensesVariation: { ...; }; }' is missing the following properties from type 'FinanceStats': tresorerie variation_tresorerie factures_impayees paiements_prevus
30     mockGetStatsFinance.mockResolvedValue(mockStats);
                                             ~~~~~~~~~
src/components/finance/__tests__/TransactionDetails.test.tsx:54:26 - error TS2741: Property 'transactionId' is missing in type '{}' but required in type 'TransactionDetailsProps'.
54     renderWithProviders(<TransactionDetails />);
                            ~~~~~~~~~~~~~~~~~~
  src/components/finance/TransactionDetails.tsx:19:3
    19   transactionId: string;
         ~~~~~~~~~~~~~
    'transactionId' is declared here.
src/components/finance/__tests__/TransactionDetails.test.tsx:63:26 - error TS2741: Property 'transactionId' is missing in type '{}' but required in type 'TransactionDetailsProps'.
63     renderWithProviders(<TransactionDetails />);
                            ~~~~~~~~~~~~~~~~~~
  src/components/finance/TransactionDetails.tsx:19:3
    19   transactionId: string;
         ~~~~~~~~~~~~~
    'transactionId' is declared here.
src/components/finance/__tests__/TransactionDetails.test.tsx:69:26 - error TS2741: Property 'transactionId' is missing in type '{}' but required in type 'TransactionDetailsProps'.
69     renderWithProviders(<TransactionDetails />);
                            ~~~~~~~~~~~~~~~~~~
  src/components/finance/TransactionDetails.tsx:19:3
    19   transactionId: string;
         ~~~~~~~~~~~~~
    'transactionId' is declared here.
src/components/finance/__tests__/TransactionDetails.test.tsx:77:26 - error TS2741: Property 'transactionId' is missing in type '{}' but required in type 'TransactionDetailsProps'.
77     renderWithProviders(<TransactionDetails />);
                            ~~~~~~~~~~~~~~~~~~
  src/components/finance/TransactionDetails.tsx:19:3
    19   transactionId: string;
         ~~~~~~~~~~~~~
    'transactionId' is declared here.
src/components/finance/__tests__/TransactionForm.test.tsx:6:29 - error TS6133: 'updateTransaction' is declared but its value is never read.
6 import { createTransaction updateTransaction getTransaction getComptes } from '../../../services/finance';
                              ~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/TransactionForm.test.tsx:6:48 - error TS6133: 'getTransaction' is declared but its value is never read.
6 import { createTransaction updateTransaction getTransaction getComptes } from '../../../services/finance';
                                                 ~~~~~~~~~~~~~~
src/components/finance/__tests__/TransactionForm.test.tsx:6:64 - error TS2614: Module '"../../../services/finance"' has no exported member 'getComptes'. Did you mean to use 'import getComptes from "../../../services/finance"' instead?
6 import { createTransaction updateTransaction getTransaction getComptes } from '../../../services/finance';
                                                                 ~~~~~~~~~~
src/components/finance/__tests__/TransactionList.test.tsx:5:29 - error TS2307: Cannot find module '../TransactionList' or its corresponding type declarations.
5 import TransactionList from '../TransactionList';
                              ~~~~~~~~~~~~~~~~~~~~
src/components/finance/__tests__/VueBudget.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/AnalyseBudget.tsx:20:28 - error TS2614: Module '"../../services/finance"' has no exported member 'AnalyseBudgetaire'. Did you mean to use 'import AnalyseBudgetaire from "../../services/finance"' instead?
20 import { getAnalyseBudget AnalyseBudgetaire } from '../../services/finance';
                              ~~~~~~~~~~~~~~~~~
src/components/finance/AnalyseBudget.tsx:25:9 - error TS6133: 'theme' is declared but its value is never read.
25   const theme = useTheme();
           ~~~~~
src/components/finance/AnalyseBudget.tsx:111:58 - error TS18046: 'donnees' is of type 'unknown'.
111                 <TableCell align="right">{formatCurrency(donnees.prevu)}</TableCell>
                                                             ~~~~~~~
src/components/finance/AnalyseBudget.tsx:112:58 - error TS18046: 'donnees' is of type 'unknown'.
112                 <TableCell align="right">{formatCurrency(donnees.realise)}</TableCell>
                                                             ~~~~~~~
src/components/finance/AnalyseBudget.tsx:113:58 - error TS18046: 'donnees' is of type 'unknown'.
113                 <TableCell align="right">{formatCurrency(donnees.ecart)}</TableCell>
                                                             ~~~~~~~
src/components/finance/AnalyseBudget.tsx:116:31 - error TS18046: 'donnees' is of type 'unknown'.
116                     label={`${donnees.ecart_pourcentage}%`}
                                  ~~~~~~~
src/components/finance/AnalyseBudget.tsx:117:28 - error TS18046: 'donnees' is of type 'unknown'.
117                     color={donnees.ecart_pourcentage < 0 ? 'error' : 'success'}
                               ~~~~~~~
src/components/finance/AnalyseBudget.tsx:134:49 - error TS7006: Parameter 'facteur' implicitly has an 'any' type.
134             {analyse.impact_meteo.facteurs.map((facteur index) => (
                                                    ~~~~~~~
src/components/finance/AnalyseBudget.tsx:134:58 - error TS7006: Parameter 'index' implicitly has an 'any' type.
134             {analyse.impact_meteo.facteurs.map((facteur index) => (
                                                             ~~~~~
src/components/finance/AnalyseBudget.tsx:148:45 - error TS2769: No overload matches this call.
  Overload 1 of 2 '(props: { component: ElementType<any keyof IntrinsicElements>; } & TypographyOwnProps & CommonProps & Omit<any "children" | ... 112 more ... | "variantMapping">): Element | null' gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
  Overload 2 of 2 '(props: DefaultComponentProps<TypographyTypeMap<{} "span">>): Element | null' gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
148               <strong>{categorie}:</strong> {projection}
                                                ~~~~~~~~~~~~
src/components/finance/AnalyseBudget.tsx:160:41 - error TS7006: Parameter 'recommandation' implicitly has an 'any' type.
160           {analyse.recommandations.map((recommandation index) => (
                                            ~~~~~~~~~~~~~~
src/components/finance/AnalyseBudget.tsx:160:57 - error TS7006: Parameter 'index' implicitly has an 'any' type.
160           {analyse.recommandations.map((recommandation index) => (
                                                            ~~~~~
src/components/finance/CashFlowChart.tsx:63:26 - error TS2339: Property 'labels' does not exist on type 'CashFlowData'.
63     labels: cashflowData.labels
                            ~~~~~~
src/components/finance/CashFlowChart.tsx:67:28 - error TS2339: Property 'recettes' does not exist on type 'CashFlowData'.
67         data: cashflowData.recettes
                              ~~~~~~~~
src/components/finance/CashFlowChart.tsx:75:28 - error TS2339: Property 'depenses' does not exist on type 'CashFlowData'.
75         data: cashflowData.depenses
                              ~~~~~~~~
src/components/finance/CashFlowChart.tsx:101:28 - error TS2339: Property 'impact_meteo' does not exist on type 'CashFlowData'.
101         data: cashflowData.impact_meteo
                               ~~~~~~~~~~~~
src/components/finance/FinanceStats.tsx:35:11 - error TS2322: Type '{ valeur: Variation; type: "hausse" | "baisse"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Type '{ valeur: Variation; type: "hausse" | "baisse"; }' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; }'.
    Types of property 'valeur' are incompatible.
      Type 'Variation' is not assignable to type 'number'.
35           variation={stats ? {
             ~~~~~~~~~
  src/components/common/StatCard.tsx:9:3
    9   variation?: {
        ~~~~~~~~~
    The expected type comes from property 'variation' which is declared here on type 'IntrinsicAttributes & StatCardProps'
src/components/finance/FinanceStats.tsx:37:19 - error TS2365: Operator '>=' cannot be applied to types 'Variation' and 'number'.
37             type: stats.revenueVariation >= 0 ? 'hausse' : 'baisse'
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/FinanceStats.tsx:50:11 - error TS2322: Type '{ valeur: Variation; type: "hausse" | "baisse"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Type '{ valeur: Variation; type: "hausse" | "baisse"; }' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; }'.
    Types of property 'valeur' are incompatible.
      Type 'Variation' is not assignable to type 'number'.
50           variation={stats ? {
             ~~~~~~~~~
  src/components/common/StatCard.tsx:9:3
    9   variation?: {
        ~~~~~~~~~
    The expected type comes from property 'variation' which is declared here on type 'IntrinsicAttributes & StatCardProps'
src/components/finance/FinanceStats.tsx:52:19 - error TS2365: Operator '>=' cannot be applied to types 'Variation' and 'number'.
52             type: stats.profitVariation >= 0 ? 'hausse' : 'baisse'
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/FinanceStats.tsx:65:11 - error TS2322: Type '{ valeur: Variation; type: "hausse" | "baisse"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Type '{ valeur: Variation; type: "hausse" | "baisse"; }' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; }'.
    Types of property 'valeur' are incompatible.
      Type 'Variation' is not assignable to type 'number'.
65           variation={stats ? {
             ~~~~~~~~~
  src/components/common/StatCard.tsx:9:3
    9   variation?: {
        ~~~~~~~~~
    The expected type comes from property 'variation' which is declared here on type 'IntrinsicAttributes & StatCardProps'
src/components/finance/FinanceStats.tsx:67:19 - error TS2365: Operator '>=' cannot be applied to types 'Variation' and 'number'.
67             type: stats.cashflowVariation >= 0 ? 'hausse' : 'baisse'
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/FinanceStats.tsx:82:19 - error TS2365: Operator '<=' cannot be applied to types 'Variation' and 'number'.
82             type: stats.expensesVariation <= 0 ? 'hausse' : 'baisse'
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/FormulaireTransaction.tsx:18:10 - error TS2724: '"../../services/finance"' has no exported member named 'creerTransaction'. Did you mean 'createTransaction'?
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
            ~~~~~~~~~~~~~~~~
  src/services/finance.ts:40:14
    40 export const createTransaction = async (data: TransactionFormData): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~~~~
    'createTransaction' is declared here.
src/components/finance/FormulaireTransaction.tsx:18:28 - error TS2614: Module '"../../services/finance"' has no exported member 'modifierTransaction'. Did you mean to use 'import modifierTransaction from "../../services/finance"' instead?
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                              ~~~~~~~~~~~~~~~~~~~
src/components/finance/FormulaireTransaction.tsx:18:65 - error TS2614: Module '"../../services/finance"' has no exported member 'getComptes'. Did you mean to use 'import getComptes from "../../services/finance"' instead?
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                   ~~~~~~~~~~
src/components/finance/FormulaireTransaction.tsx:18:77 - error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                               ~~~~~~~~~~~
  src/services/finance.ts:35:14
    35 export const getTransaction = async (id: UUID): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~
    'getTransaction' is declared here.
src/components/finance/FormulaireTransaction.tsx:18:90 - error TS2724: '"../../services/finance"' has no exported member named 'TypeTransaction'. Did you mean 'getTransaction'?
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                            ~~~~~~~~~~~~~~~
  src/services/finance.ts:35:14
    35 export const getTransaction = async (id: UUID): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~
    'getTransaction' is declared here.
src/components/finance/FormulaireTransaction.tsx:18:90 - error TS6133: 'TypeTransaction' is declared but its value is never read.
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                            ~~~~~~~~~~~~~~~
src/components/finance/FormulaireTransaction.tsx:18:107 - error TS2614: Module '"../../services/finance"' has no exported member 'StatutTransaction'. Did you mean to use 'import StatutTransaction from "../../services/finance"' instead?
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                                             ~~~~~~~~~~~~~~~~~
src/components/finance/FormulaireTransaction.tsx:18:126 - error TS2614: Module '"../../services/finance"' has no exported member 'Compte'. Did you mean to use 'import Compte from "../../services/finance"' instead?
18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                                                                ~~~~~~
src/components/finance/FormulaireTransaction.tsx:59:29 - error TS2339: Property 'date' does not exist on type 'Transaction'.
59         date: new Date(data.date)
                               ~~~~
src/components/finance/ListeTransactions.tsx:19:27 - error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?
19 import { getTransactions Transaction TypeTransaction } from '../../services/finance';
                             ~~~~~~~~~~~
  src/services/finance.ts:35:14
    35 export const getTransaction = async (id: UUID): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~
    'getTransaction' is declared here.
src/components/finance/ListeTransactions.tsx:19:40 - error TS2724: '"../../services/finance"' has no exported member named 'TypeTransaction'. Did you mean 'getTransaction'?
19 import { getTransactions Transaction TypeTransaction } from '../../services/finance';
                                          ~~~~~~~~~~~~~~~
  src/services/finance.ts:35:14
    35 export const getTransaction = async (id: UUID): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~
    'getTransaction' is declared here.
src/components/finance/ListeTransactions.tsx:27:36 - error TS6133: 'isLoading' is declared but its value is never read.
27   const { data: transactions = [] isLoading } = useQuery<Transaction[]>('transactions' getTransactions);
                                      ~~~~~~~~~
src/components/finance/ListeTransactions.tsx:27:90 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(queryKey: QueryKey options?: Omit<UseQueryOptions<Transaction[] unknown Transaction[] QueryKey> "queryKey"> | undefined): UseQueryResult<Transaction[] unknown>' gave the following error.
    Type '(filter?: TransactionFilter | undefined) => Promise<TransactionListResponse>' has no properties in common with type 'Omit<UseQueryOptions<Transaction[] unknown Transaction[] QueryKey> "queryKey">'.
  Overload 2 of 3 '(queryKey: QueryKey queryFn: QueryFunction<Transaction[] QueryKey> options?: Omit<UseQueryOptions<Transaction[] unknown Transaction[] QueryKey> "queryKey" | "queryFn"> | undefined): UseQueryResult<...>' gave the following error.
    Argument of type '(filter?: TransactionFilter) => Promise<TransactionListResponse>' is not assignable to parameter of type 'QueryFunction<Transaction[] QueryKey>'.
      Types of parameters 'filter' and 'context' are incompatible.
        Type 'QueryFunctionContext<QueryKey any>' has no properties in common with type 'TransactionFilter'.
27   const { data: transactions = [] isLoading } = useQuery<Transaction[]>('transactions' getTransactions);
                                                                                            ~~~~~~~~~~~~~~~
src/components/finance/ListeTransactions.tsx:29:45 - error TS2339: Property 'filter' does not exist on type 'never[] | TQueryFnData'.
  Property 'filter' does not exist on type 'TQueryFnData'.
29   const transactionsFiltrees = transactions.filter(transaction =>
                                               ~~~~~~
src/components/finance/ListeTransactions.tsx:29:52 - error TS7006: Parameter 'transaction' implicitly has an 'any' type.
29   const transactionsFiltrees = transactions.filter(transaction =>
                                                      ~~~~~~~~~~~
src/components/finance/ListeTransactions.tsx:78:40 - error TS7006: Parameter 'transaction' implicitly has an 'any' type.
78             {transactionsFiltrees.map((transaction) => (
                                          ~~~~~~~~~~~
src/components/finance/PageFinance.tsx:43:35 - error TS6133: 'event' is declared but its value is never read.
43   const handleChangementOnglet = (event: React.SyntheticEvent nouvelOnglet: number) => {
                                     ~~~~~
src/components/finance/ProjectionsFinancieres.tsx:7:3 - error TS6133: 'Grid' is declared but its value is never read.
7   Grid
    ~~~~
src/components/finance/ProjectionsFinancieres.tsx:21:37 - error TS2724: '"../../services/finance"' has no exported member named 'ProjectionsFinancieres'. Did you mean 'getProjectionsFinancieres'?
21 import { getProjectionsFinancieres ProjectionsFinancieres as IProjectionsFinancieres } from '../../services/finance';
                                       ~~~~~~~~~~~~~~~~~~~~~~
  src/services/finance.ts:131:14
    131 export const getProjectionsFinancieres = async (periode: string): Promise<ProjectionsFinancieres> => {
                     ~~~~~~~~~~~~~~~~~~~~~~~~~
    'getProjectionsFinancieres' is declared here.
src/components/finance/ProjectionsFinancieres.tsx:28:9 - error TS6133: 'theme' is declared but its value is never read.
28   const theme = useTheme();
           ~~~~~
src/components/finance/ProjectionsFinancieres.tsx:32:37 - error TS2345: Argument of type 'number' is not assignable to parameter of type 'string'.
32     () => getProjectionsFinancieres(3)
                                       ~
src/components/finance/ProjectionsFinancieres.tsx:73:46 - error TS7006: Parameter 'facteur' implicitly has an 'any' type.
73             {projections.facteurs_meteo.map((facteur index) => (
                                                ~~~~~~~
src/components/finance/ProjectionsFinancieres.tsx:73:55 - error TS7006: Parameter 'index' implicitly has an 'any' type.
73             {projections.facteurs_meteo.map((facteur index) => (
                                                         ~~~~~
src/components/finance/ProjectionsFinancieres.tsx:104:44 - error TS7006: Parameter 'projection' implicitly has an 'any' type.
104                 {projections.recettes.map((projection index) => {
                                               ~~~~~~~~~~
src/components/finance/ProjectionsFinancieres.tsx:104:56 - error TS7006: Parameter 'index' implicitly has an 'any' type.
104                 {projections.recettes.map((projection index) => {
                                                           ~~~~~
src/components/finance/ProjectionsFinancieres.tsx:167:44 - error TS7006: Parameter 'projection' implicitly has an 'any' type.
167                 {projections.depenses.map((projection index) => {
                                               ~~~~~~~~~~
src/components/finance/ProjectionsFinancieres.tsx:167:56 - error TS7006: Parameter 'index' implicitly has an 'any' type.
167                 {projections.depenses.map((projection index) => {
                                                           ~~~~~
src/components/finance/StatsFinance.tsx:6:27 - error TS2724: '"../../services/finance"' has no exported member named 'FinanceStats'. Did you mean 'getFinanceStats'?
6 import { getStatsFinance FinanceStats } from '../../services/finance';
                            ~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:9:24 - error TS6133: 'isLoading' is declared but its value is never read.
9   const { data: stats isLoading } = useQuery<FinanceStats>('finance-stats' getStatsFinance);
                         ~~~~~~~~~
src/components/finance/StatsFinance.tsx:9:78 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(queryKey: QueryKey options?: Omit<UseQueryOptions<FinanceStats unknown FinanceStats QueryKey> "queryKey"> | undefined): UseQueryResult<FinanceStats unknown>' gave the following error.
    Type '(periode?: string | undefined) => Promise<FinanceStats>' has no properties in common with type 'Omit<UseQueryOptions<FinanceStats unknown FinanceStats QueryKey> "queryKey">'.
  Overload 2 of 3 '(queryKey: QueryKey queryFn: QueryFunction<FinanceStats QueryKey> options?: Omit<UseQueryOptions<FinanceStats unknown FinanceStats QueryKey> "queryKey" | "queryFn"> | undefined): UseQueryResult<...>' gave the following error.
    Argument of type '(periode?: string) => Promise<FinanceStats>' is not assignable to parameter of type 'QueryFunction<FinanceStats QueryKey>'.
      Types of parameters 'periode' and 'context' are incompatible.
        Type 'QueryFunctionContext<QueryKey any>' is not assignable to type 'string'.
9   const { data: stats isLoading } = useQuery<FinanceStats>('finance-stats' getStatsFinance);
                                                                               ~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:16:25 - error TS2339: Property 'revenue' does not exist on type 'NonNullable<TQueryFnData>'.
16           value={stats?.revenue || 0}
                           ~~~~~~~
src/components/finance/StatsFinance.tsx:19:13 - error TS2353: Object literal may only specify known properties and 'value' does not exist in type '{ valeur: number; type: "hausse" | "baisse"; }'.
19             value: stats?.revenueVariation?.value || 0
               ~~~~~
  src/components/common/StatCard.tsx:9:3
    9   variation?: {
        ~~~~~~~~~
    The expected type comes from property 'variation' which is declared here on type 'IntrinsicAttributes & StatCardProps'
src/components/finance/StatsFinance.tsx:19:27 - error TS2339: Property 'revenueVariation' does not exist on type 'NonNullable<TQueryFnData>'.
19             value: stats?.revenueVariation?.value || 0
                             ~~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:20:26 - error TS2339: Property 'revenueVariation' does not exist on type 'NonNullable<TQueryFnData>'.
20             type: stats?.revenueVariation?.type || 'increase'
                            ~~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:30:25 - error TS2339: Property 'profit' does not exist on type 'NonNullable<TQueryFnData>'.
30           value={stats?.profit || 0}
                           ~~~~~~
src/components/finance/StatsFinance.tsx:33:13 - error TS2353: Object literal may only specify known properties and 'value' does not exist in type '{ valeur: number; type: "hausse" | "baisse"; }'.
33             value: stats?.profitVariation?.value || 0
               ~~~~~
  src/components/common/StatCard.tsx:9:3
    9   variation?: {
        ~~~~~~~~~
    The expected type comes from property 'variation' which is declared here on type 'IntrinsicAttributes & StatCardProps'
src/components/finance/StatsFinance.tsx:33:27 - error TS2339: Property 'profitVariation' does not exist on type 'NonNullable<TQueryFnData>'.
33             value: stats?.profitVariation?.value || 0
                             ~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:34:26 - error TS2339: Property 'profitVariation' does not exist on type 'NonNullable<TQueryFnData>'.
34             type: stats?.profitVariation?.type || 'increase'
                            ~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:44:25 - error TS2339: Property 'cashflow' does not exist on type 'NonNullable<TQueryFnData>'.
44           value={stats?.cashflow || 0}
                           ~~~~~~~~
src/components/finance/StatsFinance.tsx:47:13 - error TS2353: Object literal may only specify known properties and 'value' does not exist in type '{ valeur: number; type: "hausse" | "baisse"; }'.
47             value: stats?.cashflowVariation?.value || 0
               ~~~~~
  src/components/common/StatCard.tsx:9:3
    9   variation?: {
        ~~~~~~~~~
    The expected type comes from property 'variation' which is declared here on type 'IntrinsicAttributes & StatCardProps'
src/components/finance/StatsFinance.tsx:47:27 - error TS2339: Property 'cashflowVariation' does not exist on type 'NonNullable<TQueryFnData>'.
47             value: stats?.cashflowVariation?.value || 0
                             ~~~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:48:26 - error TS2339: Property 'cashflowVariation' does not exist on type 'NonNullable<TQueryFnData>'.
48             type: stats?.cashflowVariation?.type || 'increase'
                            ~~~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:58:25 - error TS2339: Property 'expenses' does not exist on type 'NonNullable<TQueryFnData>'.
58           value={stats?.expenses || 0}
                           ~~~~~~~~
src/components/finance/StatsFinance.tsx:61:13 - error TS2353: Object literal may only specify known properties and 'value' does not exist in type '{ valeur: number; type: "hausse" | "baisse"; }'.
61             value: stats?.expensesVariation?.value || 0
               ~~~~~
  src/components/common/StatCard.tsx:9:3
    9   variation?: {
        ~~~~~~~~~
    The expected type comes from property 'variation' which is declared here on type 'IntrinsicAttributes & StatCardProps'
src/components/finance/StatsFinance.tsx:61:27 - error TS2339: Property 'expensesVariation' does not exist on type 'NonNullable<TQueryFnData>'.
61             value: stats?.expensesVariation?.value || 0
                             ~~~~~~~~~~~~~~~~~
src/components/finance/StatsFinance.tsx:62:26 - error TS2339: Property 'expensesVariation' does not exist on type 'NonNullable<TQueryFnData>'.
62             type: stats?.expensesVariation?.type || 'increase'
                            ~~~~~~~~~~~~~~~~~
src/components/finance/TransactionDetails.tsx:153:49 - error TS2339: Property 'numero' does not exist on type 'string'.
153                   {transaction.compte_source_id.numero}
                                                    ~~~~~~
src/components/finance/TransactionDetails.tsx:156:49 - error TS2339: Property 'libelle' does not exist on type 'string'.
156                   {transaction.compte_source_id.libelle}
                                                    ~~~~~~~
src/components/finance/TransactionDetails.tsx:173:54 - error TS2339: Property 'numero' does not exist on type 'string'.
173                   {transaction.compte_destination_id.numero}
                                                         ~~~~~~
src/components/finance/TransactionDetails.tsx:176:54 - error TS2339: Property 'libelle' does not exist on type 'string'.
176                   {transaction.compte_destination_id.libelle}
                                                         ~~~~~~~
src/components/finance/TransactionDetails.tsx:186:24 - error TS2551: Property 'validee_par_id' does not exist on type 'Transaction'. Did you mean 'validee_par'?
186           {transaction.validee_par_id && (
                           ~~~~~~~~~~~~~~
  src/types/finance.ts:51:3
    51   validee_par?: {
         ~~~~~~~~~~~
    'validee_par' is declared here.
src/components/finance/TransactionDetails.tsx:193:32 - error TS2551: Property 'validee_par_id' does not exist on type 'Transaction'. Did you mean 'validee_par'?
193                   {transaction.validee_par_id.nom} {transaction.validee_par_id.prenom}
                                   ~~~~~~~~~~~~~~
  src/types/finance.ts:51:3
    51   validee_par?: {
         ~~~~~~~~~~~
    'validee_par' is declared here.
src/components/finance/TransactionDetails.tsx:193:65 - error TS2551: Property 'validee_par_id' does not exist on type 'Transaction'. Did you mean 'validee_par'?
193                   {transaction.validee_par_id.nom} {transaction.validee_par_id.prenom}
                                                                    ~~~~~~~~~~~~~~
  src/types/finance.ts:51:3
    51   validee_par?: {
         ~~~~~~~~~~~
    'validee_par' is declared here.
src/components/finance/TransactionForm.tsx:18:64 - error TS2614: Module '"../../services/finance"' has no exported member 'getComptes'. Did you mean to use 'import getComptes from "../../services/finance"' instead?
18 import { createTransaction updateTransaction getTransaction getComptes Transaction } from '../../services/finance';
                                                                  ~~~~~~~~~~
src/components/finance/TransactionForm.tsx:18:76 - error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?
18 import { createTransaction updateTransaction getTransaction getComptes Transaction } from '../../services/finance';
                                                                              ~~~~~~~~~~~
  src/services/finance.ts:35:14
    35 export const getTransaction = async (id: UUID): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~
    'getTransaction' is declared here.
src/components/finance/TransactionForm.tsx:64:5 - error TS2554: Expected 1-2 arguments but got 3.
64     { enabled: isEdit }
       ~~~~~~~~~~~~~~~~~~~
src/components/finance/TransactionForm.tsx:67:43 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(options: DefinedInitialDataOptions<unknown Error unknown QueryKey> queryClient?: QueryClient | undefined): DefinedUseQueryResult<unknown Error>' gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<unknown Error unknown QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown Error unknown QueryKey>'.
  Overload 2 of 3 '(options: UndefinedInitialDataOptions<unknown Error unknown QueryKey> queryClient?: QueryClient | undefined): UseQueryResult<unknown Error>' gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<unknown Error unknown QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown Error unknown QueryKey>'.
  Overload 3 of 3 '(options: UseQueryOptions<unknown Error unknown QueryKey> queryClient?: QueryClient | undefined): UseQueryResult<unknown Error>' gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<unknown Error unknown QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown Error unknown QueryKey>'.
67   const { data: comptes = [] } = useQuery(['comptes'] getComptes);
                                             ~~~~~~~~~~~
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
src/components/finance/TransactionForm.tsx:82:5 - error TS2322: Type 'Resolver<{ description?: string | undefined; compte_source?: string | undefined; compte_destination?: string | undefined; statut: string; categorie: string; reference: string; type_transaction: string; montant: number; date_transaction: string; }>' is not assignable to type 'Resolver<TransactionFormData any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type 'TransactionFormData' is missing the following properties from type '{ description?: string | undefined; compte_source?: string | undefined; compte_destination?: string | undefined; statut: string; categorie: string; reference: string; type_transaction: string; montant: number; date_transaction: string; }': statut categorie reference type_transaction and 2 more.
82     resolver: yupResolver(schema)
       ~~~~~~~~
src/components/finance/TransactionForm.tsx:89:5 - error TS2559: Type '(data: TransactionFormData) => Promise<Transaction>' has no properties in common with type 'UseMutationOptions<unknown Error void unknown>'.
89     (data: TransactionFormData) => {
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/finance/TransactionForm.tsx:94:46 - error TS2559: Type '{ date_transaction: string; compte_source?: string | undefined; compte_destination?: string | undefined; }' has no properties in common with type 'Partial<TransactionFormData>'.
94       return isEdit ? updateTransaction(id! transactionData) : createTransaction(transactionData);
                                                ~~~~~~~~~~~~~~~
src/components/finance/TransactionForm.tsx:94:83 - error TS2345: Argument of type '{ date_transaction: string; compte_source?: string; compte_destination?: string; }' is not assignable to parameter of type 'TransactionFormData'.
  Type '{ date_transaction: string; compte_source?: string | undefined; compte_destination?: string | undefined; }' is missing the following properties from type 'TransactionFormData': reference type_transaction categorie montant
94       return isEdit ? updateTransaction(id! transactionData) : createTransaction(transactionData);
                                                                                     ~~~~~~~~~~~~~~~
src/components/finance/TransactionForm.tsx:98:39 - error TS2559: Type 'string[]' has no properties in common with type 'InvalidateQueryFilters'.
98         queryClient.invalidateQueries(['transactions']);
                                         ~~~~~~~~~~~~~~~~
src/components/finance/TransactionForm.tsx:105:21 - error TS2345: Argument of type 'TransactionFormData' is not assignable to parameter of type 'void'.
105     mutation.mutate(data);
                        ~~~~
src/components/finance/TransactionForm.tsx:116:60 - error TS2339: Property 'reference' does not exist on type '{}'.
116         subtitle={isEdit ? `Modification de ${transaction?.reference}` : 'Création d\'une nouvelle transaction'}
                                                               ~~~~~~~~~
src/components/finance/TransactionForm.tsx:241:26 - error TS18046: 'comptes' is of type 'unknown'.
241                         {comptes.map((compte) => (
                             ~~~~~~~
src/components/finance/TransactionForm.tsx:241:39 - error TS7006: Parameter 'compte' implicitly has an 'any' type.
241                         {comptes.map((compte) => (
                                          ~~~~~~
src/components/finance/TransactionForm.tsx:266:26 - error TS18046: 'comptes' is of type 'unknown'.
266                         {comptes.map((compte) => (
                             ~~~~~~~
src/components/finance/TransactionForm.tsx:266:39 - error TS7006: Parameter 'compte' implicitly has an 'any' type.
266                         {comptes.map((compte) => (
                                          ~~~~~~
src/components/finance/TransactionForm.tsx:306:39 - error TS2339: Property 'isLoading' does not exist on type 'UseMutationResult<unknown Error void unknown>'.
  Property 'isLoading' does not exist on type 'Override<MutationObserverIdleResult<unknown Error void unknown> { mutate: UseMutateFunction<unknown Error void unknown>; }> & { ...; }'.
306                     loading={mutation.isLoading}
                                          ~~~~~~~~~
src/components/finance/TransactionsList.tsx:19:27 - error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?
19 import { getTransactions Transaction } from '../../services/finance';
                             ~~~~~~~~~~~
  src/services/finance.ts:35:14
    35 export const getTransaction = async (id: UUID): Promise<Transaction> => {
                    ~~~~~~~~~~~~~~
    'getTransaction' is declared here.
src/components/finance/TransactionsList.tsx:27:63 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(options: DefinedInitialDataOptions<Transaction[] Error Transaction[] QueryKey> queryClient?: QueryClient | undefined): DefinedUseQueryResult<Transaction[] Error>' gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<Transaction[] Error Transaction[] QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Transaction[] Error Transaction[] QueryKey>'.
  Overload 2 of 3 '(options: UndefinedInitialDataOptions<Transaction[] Error Transaction[] QueryKey> queryClient?: QueryClient | undefined): UseQueryResult<Transaction[] Error>' gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<Transaction[] Error Transaction[] QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Transaction[] Error Transaction[] QueryKey>'.
  Overload 3 of 3 '(options: UseQueryOptions<Transaction[] Error Transaction[] QueryKey> queryClient?: QueryClient | undefined): UseQueryResult<Transaction[] Error>' gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<Transaction[] Error Transaction[] QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Transaction[] Error Transaction[] QueryKey>'.
27   const { data: transactions = [] } = useQuery<Transaction[]>(['transactions'] getTransactions);
                                                                 ~~~~~~~~~~~~~~~~
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
src/components/finance/TransactionsList.tsx:29:45 - error TS2339: Property 'filter' does not exist on type 'never[] | TQueryFnData'.
  Property 'filter' does not exist on type 'TQueryFnData'.
29   const filteredTransactions = transactions.filter(transaction =>
                                               ~~~~~~
src/components/finance/TransactionsList.tsx:29:52 - error TS7006: Parameter 'transaction' implicitly has an 'any' type.
29   const filteredTransactions = transactions.filter(transaction =>
                                                      ~~~~~~~~~~~
src/components/finance/TransactionsList.tsx:78:40 - error TS7006: Parameter 'transaction' implicitly has an 'any' type.
78             {filteredTransactions.map((transaction) => (
                                          ~~~~~~~~~~~
src/components/finance/VueBudget.tsx:16:52 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(queryKey: "vue-budget" options?: Omit<UseQueryOptions<unknown unknown unknown "vue-budget"> "queryKey"> | undefined): UseQueryResult<unknown unknown>' gave the following error.
    Type '(periode: string) => Promise<VueBudgetaire[]>' has no properties in common with type 'Omit<UseQueryOptions<unknown unknown unknown "vue-budget"> "queryKey">'.
  Overload 2 of 3 '(queryKey: "vue-budget" queryFn: QueryFunction<VueBudgetaire[] "vue-budget"> options?: Omit<UseQueryOptions<VueBudgetaire[] unknown VueBudgetaire[] "vue-budget"> "queryKey" | "queryFn"> | undefined): UseQueryResult<...>' gave the following error.
    Argument of type '(periode: string) => Promise<VueBudgetaire[]>' is not assignable to parameter of type 'QueryFunction<VueBudgetaire[] "vue-budget">'.
      Types of parameters 'periode' and 'context' are incompatible.
        Type 'QueryFunctionContext<"vue-budget" any>' is not assignable to type 'string'.
16   const { data: budgets } = useQuery('vue-budget' getVueBudget);
                                                      ~~~~~~~~~~~~
src/components/finance/VueBudget.tsx:32:21 - error TS2339: Property 'map' does not exist on type '{}'.
32           {budgets?.map((budget) => {
                       ~~~
src/components/finance/VueBudget.tsx:32:26 - error TS7006: Parameter 'budget' implicitly has an 'any' type.
32           {budgets?.map((budget) => {
                            ~~~~~~
src/components/hr/__tests__/AttendanceChart.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/hr/__tests__/AttendanceOverview.test.tsx:5:10 - error TS2305: Module '"../../../services/hr"' has no exported member 'getAttendanceOverview'.
5 import { getAttendanceOverview } from '../../../services/hr';
           ~~~~~~~~~~~~~~~~~~~~~
src/components/hr/__tests__/EmployeeDetails.test.tsx:2:37 - error TS6133: 'waitFor' is declared but its value is never read.
2 import { render screen fireEvent waitFor } from '@testing-library/react';
                                      ~~~~~~~
src/components/hr/__tests__/EmployeeDetails.test.tsx:6:23 - error TS2724: '"../../../services/hr"' has no exported member named 'getEmployeeLeaves'. Did you mean 'getEmployees'?
6 import { getEmployee getEmployeeLeaves } from '../../../services/hr';
                        ~~~~~~~~~~~~~~~~~
  src/services/hr.ts:42:14
    42 export const getEmployees = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'employees']>): Promise<Employee[]> => {
                    ~~~~~~~~~~~~
    'getEmployees' is declared here.
src/components/hr/__tests__/EmployeeForm.test.tsx:6:26 - error TS6133: 'updateEmployee' is declared but its value is never read.
6 import { createEmployee updateEmployee getEmployee } from '../../../services/hr';
                           ~~~~~~~~~~~~~~
src/components/hr/__tests__/EmployeeForm.test.tsx:6:42 - error TS6133: 'getEmployee' is declared but its value is never read.
6 import { createEmployee updateEmployee getEmployee } from '../../../services/hr';
                                           ~~~~~~~~~~~
src/components/hr/__tests__/LeaveRequestForm.test.tsx:5:10 - error TS2305: Module '"../../../services/hr"' has no exported member 'createLeaveRequest'.
5 import { createLeaveRequest } from '../../../services/hr';
           ~~~~~~~~~~~~~~~~~~
src/components/hr/__tests__/LeaveRequestForm.test.tsx:35:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.
35         open={true}
           ~~~~
src/components/hr/__tests__/LeaveRequestForm.test.tsx:50:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.
50         open={true}
           ~~~~
src/components/hr/__tests__/LeaveRequestForm.test.tsx:66:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.
66         open={true}
           ~~~~
src/components/hr/__tests__/LeaveRequestForm.test.tsx:89:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.
89         open={true}
           ~~~~
src/components/hr/__tests__/LeaveRequestForm.test.tsx:120:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.
120         open={true}
            ~~~~
src/components/hr/analytics/__tests__/HRAnalyticsDashboard.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/hr/analytics/HRAnalyticsDashboard.tsx:7:1 - error TS6133: 'queryKeys' is declared but its value is never read.
7 import { queryKeys } from '../../../config/queryClient';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/hr/AttendanceOverview.tsx:65:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "primary"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.
65             total={stats.totalEmployees}
               ~~~~~
src/components/hr/AttendanceOverview.tsx:75:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "info"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.
75             total={stats.totalEmployees}
               ~~~~~
src/components/hr/AttendanceOverview.tsx:85:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "warning"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.
85             total={stats.totalEmployees}
               ~~~~~
src/components/hr/AttendanceOverview.tsx:95:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "error"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.
95             total={stats.totalEmployees}
               ~~~~~
src/components/hr/formation/__tests__/FormationForm.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/hr/formation/__tests__/FormationList.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/hr/formation/__tests__/FormationPage.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/hr/types/formTypes.ts:1:38 - error TS6133: 'UseFormRegister' is declared but its value is never read.
1 import { Control FieldErrors Path UseFormRegister } from 'react-hook-form';
                                       ~~~~~~~~~~~~~~~
src/components/hr/weather/__tests__/CarteMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/hr/weather/__tests__/TableauDeBordMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/inventaire/__tests__/DetailsProduit.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/inventaire/__tests__/DetailsProduit.test.tsx:7:22 - error TS2305: Module '"../../../services/inventaire"' has no exported member 'getProductMovements'.
7 import { getProduit getProductMovements } from '../../../services/inventaire';
                       ~~~~~~~~~~~~~~~~~~~
src/components/inventaire/__tests__/DialogueMouvementStock.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/inventaire/__tests__/FormulaireProduit.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/inventaire/__tests__/FormulaireProduit.test.tsx:7:53 - error TS2305: Module '"../../../services/inventaire"' has no exported member 'verifierCodeUnique'.
7 import { creerProduit modifierProduit getProduit verifierCodeUnique } from '../../../services/inventaire';
                                                      ~~~~~~~~~~~~~~~~~~
src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:6:25 - error TS2305: Module '"../../../services/inventaire"' has no exported member 'getTendances'.
6 import { getMouvements getTendances } from '../../../services/inventaire';
                          ~~~~~~~~~~~~
src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:31:5 - error TS2561: Object literal may only specify known properties but 'responsable' does not exist in type 'MouvementStock'. Did you mean to write 'responsable_id'?
31     responsable: {
       ~~~~~~~~~~~
src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:55:5 - error TS2561: Object literal may only specify known properties but 'responsable' does not exist in type 'MouvementStock'. Did you mean to write 'responsable_id'?
55     responsable: {
       ~~~~~~~~~~~
src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:66:33 - error TS2339: Property 'L' does not exist on type 'typeof UniteMesure'.
66       unite_mesure: UniteMesure.L
                                   ~
src/components/inventaire/__tests__/ListeStock.test.tsx:14:3 - error TS2322: Type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: UniteMesure.KG; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' is not assignable to type 'Stock & { produit: Produit; }'.
  Property 'entrepot_id' is missing in type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: UniteMesure.KG; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' but required in type 'Stock'.
 14   {
      ~
 15     id: '1'
    ~~~~~~~~~~~~
...
 30     }
    ~~~~~
 31   }
    ~~~
  src/types/inventaire.ts:118:3
    118   entrepot_id: string;
          ~~~~~~~~~~~
    'entrepot_id' is declared here.
src/components/inventaire/__tests__/ListeStock.test.tsx:32:3 - error TS2322: Type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: any; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' is not assignable to type 'Stock & { produit: Produit; }'.
  Property 'entrepot_id' is missing in type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: any; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' but required in type 'Stock'.
 32   {
      ~
 33     id: '2'
    ~~~~~~~~~~~~
...
 48     }
    ~~~~~
 49   }
    ~~~
  src/types/inventaire.ts:118:3
    118   entrepot_id: string;
          ~~~~~~~~~~~
    'entrepot_id' is declared here.
src/components/inventaire/__tests__/ListeStock.test.tsx:44:33 - error TS2339: Property 'L' does not exist on type 'typeof UniteMesure'.
44       unite_mesure: UniteMesure.L
                                   ~
src/components/inventaire/__tests__/StatsInventaire.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/inventaire/DetailsProduit.tsx:26:22 - error TS2305: Module '"../../services/inventaire"' has no exported member 'getProductMovements'.
26 import { getProduit getProductMovements } from '../../services/inventaire';
                        ~~~~~~~~~~~~~~~~~~~
src/components/inventaire/DetailsProduit.tsx:75:14 - error TS7006: Parameter 'movement' implicitly has an 'any' type.
75     ?.filter(movement =>
                ~~~~~~~~
src/components/inventaire/DetailsProduit.tsx:80:12 - error TS7006: Parameter 'a' implicitly has an 'any' type.
80     .sort((a b) => {
              ~
src/components/inventaire/DetailsProduit.tsx:80:15 - error TS7006: Parameter 'b' implicitly has an 'any' type.
80     .sort((a b) => {
                 ~
src/components/inventaire/DetailsProduit.tsx:104:24 - error TS7006: Parameter 'm' implicitly has an 'any' type.
104       ...movements.map(m => [
                           ~
src/components/inventaire/DetailsProduit.tsx:199:31 - error TS2769: No overload matches this call.
  Overload 1 of 2 '(value: number | bigint): string' gave the following error.
    Argument of type 'number | undefined' is not assignable to parameter of type 'number | bigint'.
      Type 'undefined' is not assignable to type 'number | bigint'.
  Overload 2 of 2 '(value: number): string' gave the following error.
    Argument of type 'number | undefined' is not assignable to parameter of type 'number'.
      Type 'undefined' is not assignable to type 'number'.
199                     }).format(product.prix_unitaire)}
                                  ~~~~~~~~~~~~~~~~~~~~~
src/components/inventaire/DetailsProduit.tsx:304:26 - error TS7006: Parameter 'movement' implicitly has an 'any' type.
304                     .map(movement => (
                             ~~~~~~~~
src/components/inventaire/DialogueMouvementStock.tsx:86:32 - error TS2339: Property 'quantite_stock' does not exist on type 'Produit'.
86     context: { stock: product?.quantite_stock }
                                  ~~~~~~~~~~~~~~
src/components/inventaire/DialogueMouvementStock.tsx:117:23 - error TS2345: Argument of type '{ type_mouvement: TypeMouvement; quantite: number; reference_document: string; cout_unitaire?: number; notes?: string; produit_id: string; }' is not assignable to parameter of type 'Omit<MouvementStock "id" | "date_mouvement">'.
  Property 'responsable_id' is missing in type '{ type_mouvement: TypeMouvement; quantite: number; reference_document: string; cout_unitaire?: number; notes?: string; produit_id: string; }' but required in type 'Omit<MouvementStock "id" | "date_mouvement">'.
117       mutation.mutate({
                          ~
118         produit_id: productId
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
119         ...data
    ~~~~~~~~~~~~~~~
120       });
    ~~~~~~~
  src/types/inventaire.ts:138:3
    138   responsable_id: string;
          ~~~~~~~~~~~~~~
    'responsable_id' is declared here.
src/components/inventaire/DialogueMouvementStock.tsx:160:44 - error TS2339: Property 'quantite_stock' does not exist on type 'Produit'.
160                     Stock actuel: {product.quantite_stock ?? 0} {product.unite_mesure}
                                               ~~~~~~~~~~~~~~
src/components/inventaire/DialogueMouvementStock.tsx:239:48 - error TS2339: Property 'quantite_stock' does not exist on type 'Produit'.
239                     Stock disponible: {product.quantite_stock ?? 0} {product.unite_mesure}
                                                   ~~~~~~~~~~~~~~
src/components/inventaire/DialogueMouvementStock.tsx:363:42 - error TS2339: Property 'quantite_stock' does not exist on type 'Produit'.
363                   Stock actuel: {product.quantite_stock ?? 0} {product.unite_mesure}
                                             ~~~~~~~~~~~~~~
src/components/inventaire/DialogueMouvementStock.tsx:366:52 - error TS2339: Property 'quantite_stock' does not exist on type 'Produit'.
366                   Stock après opération: {(product.quantite_stock ?? 0) - (watchQuantite || 0)} {product.unite_mesure}
                                                       ~~~~~~~~~~~~~~
src/components/inventaire/FormulaireProduit.tsx:25:53 - error TS2305: Module '"../../services/inventaire"' has no exported member 'verifierCodeUnique'.
25 import { creerProduit modifierProduit getProduit verifierCodeUnique } from '../../services/inventaire';
                                                       ~~~~~~~~~~~~~~~~~~
src/components/inventaire/FormulaireProduit.tsx:81:24 - error TS2339: Property 'L' does not exist on type 'typeof UniteMesure'.
81   { value: UniteMesure.L label: 'Litre' }
                          ~
src/components/inventaire/FormulaireProduit.tsx:83:24 - error TS2339: Property 'CARTON' does not exist on type 'typeof UniteMesure'.
83   { value: UniteMesure.CARTON label: 'Carton' }
                          ~~~~~~
src/components/inventaire/StatsInventaire.tsx:17:11 - error TS6196: 'Variation' is declared but never used.
17 interface Variation {
             ~~~~~~~~~
src/components/parametrage/__tests__/ParametrageLayout.test.tsx:41:8 - error TS2559: Type '{ children: Element; }' has no properties in common with type 'IntrinsicAttributes'.
41       <ParametrageLayout>
          ~~~~~~~~~~~~~~~~~
src/components/parametrage/ConfigurationModules.tsx:10:3 - error TS6133: 'IconButton' is declared but its value is never read.
10   IconButton
     ~~~~~~~~~~
src/components/production/__tests__/ParcelleForm.test.tsx:6:26 - error TS6133: 'updateParcelle' is declared but its value is never read.
6 import { createParcelle updateParcelle getParcelle } from '../../../services/production';
                           ~~~~~~~~~~~~~~
src/components/production/__tests__/ParcelleForm.test.tsx:6:42 - error TS6133: 'getParcelle' is declared but its value is never read.
6 import { createParcelle updateParcelle getParcelle } from '../../../services/production';
                                           ~~~~~~~~~~~
src/components/production/__tests__/ParcellesList.test.tsx:2:26 - error TS6133: 'fireEvent' is declared but its value is never read.
2 import { render screen fireEvent } from '@testing-library/react';
                           ~~~~~~~~~
src/components/production/__tests__/TableauMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/production/__tests__/TableauMeteo.test.tsx:25:9 - error TS2353: Object literal may only specify known properties and 'timestamp' does not exist in type 'WeatherCondition'.
25         timestamp: new Date().toISOString()
           ~~~~~~~~~
src/components/production/HarvestQualityForm.tsx:98:9 - error TS2740: Type '{ temperature: number; humidite: number; precipitation: number; }' is missing the following properties from type 'WeatherConditions': timestamp humidity wind_speed conditions and 2 more.
98         conditions_meteo: formData.conditions_meteo
           ~~~~~~~~~~~~~~~~
  src/types/production.ts:85:3
    85   conditions_meteo: WeatherConditions;
         ~~~~~~~~~~~~~~~~
    The expected type comes from property 'conditions_meteo' which is declared here on type 'Partial<Recolte>'
src/components/production/ParcelleMap.tsx:6:21 - error TS2307: Cannot find module '/home/user/ERP/src/services/api' or its corresponding type declarations.
6 import { api } from "/home/user/ERP/src/services/api"
                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/production/RecolteForm.tsx:52:7 - error TS2322: Type 'null' is not assignable to type 'Date | undefined'.
52       date_recolte: null
         ~~~~~~~~~~~~
src/components/production/RecolteForm.tsx:53:7 - error TS2322: Type 'string' is not assignable to type 'number'.
53       quantite_kg: ''
         ~~~~~~~~~~~
src/components/production/RecolteForm.tsx:57:9 - error TS2322: Type 'string' is not assignable to type 'number'.
57         temperature: ''
           ~~~~~~~~~~~
src/components/production/RecolteForm.tsx:58:9 - error TS2322: Type 'string' is not assignable to type 'number'.
58         humidite: ''
           ~~~~~~~~
src/components/projects/__tests__/ProjectDetails.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/projects/__tests__/ProjectForm.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/projects/__tests__/TaskForm.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.
1 import React from 'react';
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/projects/__tests__/TaskList.test.tsx:5:10 - error TS2724: '"../../../services/projects"' has no exported member named 'getProjectTasks'. Did you mean 'getProjectStats'?
5 import { getProjectTasks } from '../../../services/projects';
           ~~~~~~~~~~~~~~~
  src/services/projects.ts:4:14
    4 export const getProjectStats = async (): Promise<ProjectStats> => {
                   ~~~~~~~~~~~~~~~
    'getProjectStats' is declared here.
src/components/projects/__tests__/TasksOverview.test.tsx:5:10 - error TS2305: Module '"../../../services/projects"' has no exported member 'getRecentTasks'.
5 import { getRecentTasks } from '../../../services/projects';
           ~~~~~~~~~~~~~~
src/components/projects/ProjectDetails.tsx:9:3 - error TS6133: 'Button' is declared but its value is never read.
9   Button
    ~~~~~~
src/components/projects/ProjectDetails.tsx:10:3 - error TS6133: 'Link' is declared but its value is never read.
10   Link
     ~~~~
src/components/projects/ProjectDetails.tsx:24:38 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(options: DefinedInitialDataOptions<unknown Error unknown QueryKey> queryClient?: QueryClient | undefined): DefinedUseQueryResult<unknown Error>' gave the following error.
    Argument of type '(string | undefined)[]' is not assignable to parameter of type 'DefinedInitialDataOptions<unknown Error unknown QueryKey>'.
      Property 'queryKey' is missing in type '(string | undefined)[]' but required in type 'UseQueryOptions<unknown Error unknown QueryKey>'.
  Overload 2 of 3 '(options: UndefinedInitialDataOptions<unknown Error unknown QueryKey> queryClient?: QueryClient | undefined): UseQueryResult<unknown Error>' gave the following error.
    Argument of type '(string | undefined)[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<unknown Error unknown QueryKey>'.
      Property 'queryKey' is missing in type '(string | undefined)[]' but required in type 'UseQueryOptions<unknown Error unknown QueryKey>'.
  Overload 3 of 3 '(options: UseQueryOptions<unknown Error unknown QueryKey> queryClient?: QueryClient | undefined): UseQueryResult<unknown Error>' gave the following error.
    Argument of type '(string | undefined)[]' is not assignable to parameter of type 'UseQueryOptions<unknown Error unknown QueryKey>'.
      Property 'queryKey' is missing in type '(string | undefined)[]' but required in type 'UseQueryOptions<unknown Error unknown QueryKey>'.
24   const { data: project } = useQuery(['project' id] () => getProject(id!));
                                        ~~~~~~~~~~~~~~~
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
  node_modules/@tanstack/query-core/build/modern/hydration-D-INNavI.d.ts:583:5
    583     queryKey?: TQueryKey;
            ~~~~~~~~
    'queryKey' is declared here.
src/components/projects/ProjectDetails.tsx:44:35 - error TS2339: Property 'code' does not exist on type '{}'.
44         title={`Projet ${project?.code}`}
                                     ~~~~
src/components/projects/ProjectDetails.tsx:45:28 - error TS2339: Property 'nom' does not exist on type '{}'.
45         subtitle={project?.nom}
                              ~~~
src/components/projects/ProjectDetails.tsx:67:37 - error TS2339: Property 'statut' does not exist on type '{}'.
67                     label={project?.statut}
                                       ~~~~~~
src/components/projects/ProjectDetails.tsx:68:52 - error TS2339: Property 'statut' does not exist on type '{}'.
68                     color={getStatusColor(project?.statut || '')}
                                                      ~~~~~~
src/components/projects/ProjectDetails.tsx:80:40 - error TS2339: Property 'budget' does not exist on type '{}'.
80                     }).format(project?.budget || 0)}
                                          ~~~~~~
src/components/projects/ProjectDetails.tsx:89:38 - error TS2339: Property 'date_debut' does not exist on type '{}'.
89                     Début: {project?.date_debut &&
                                        ~~~~~~~~~~
src/components/projects/ProjectDetails.tsx:90:47 - error TS2339: Property 'date_debut' does not exist on type '{}'.
90                       format(new Date(project.date_debut) 'PP' { locale: fr })}
                                                 ~~~~~~~~~~
src/components/projects/ProjectDetails.tsx:93:43 - error TS2339: Property 'date_fin_prevue' does not exist on type '{}'.
93                     Fin prévue: {project?.date_fin_prevue &&
                                             ~~~~~~~~~~~~~~~
src/components/projects/ProjectDetails.tsx:94:47 - error TS2339: Property 'date_fin_prevue' does not exist on type '{}'.
94                       format(new Date(project.date_fin_prevue) 'PP' { locale: fr })}
                                                 ~~~~~~~~~~~~~~~
src/components/projects/ProjectForm.tsx:10:3 - error TS6133: 'MenuItem' is declared but its value is never read.
10   MenuItem
     ~~~~~~~~
src/components/projects/ProjectForm.tsx:45:5 - error TS2554: Expected 1-2 arguments but got 3.
45     { enabled: isEdit }
       ~~~~~~~~~~~~~~~~~~~
src/components/projects/ProjectForm.tsx:49:5 - error TS2322: Type 'Resolver<{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; budget: number; nom: string; date_fin_prevue: Date; }>' is not assignable to type 'Resolver<{} any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type '{}' is missing the following properties from type '{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; budget: number; nom: string; date_fin_prevue: Date; }': code date_debut responsable_id budget and 2 more.
49     resolver: yupResolver(schema)
       ~~~~~~~~
src/components/projects/ProjectForm.tsx:64:5 - error TS2559: Type '(data: any) => Promise<Project>' has no properties in common with type 'UseMutationOptions<unknown Error void unknown>'.
64     (data: any) => isEdit ? updateProject(id! data) : createProject(data)
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/components/projects/ProjectForm.tsx:67:39 - error TS2559: Type '"projects"' has no properties in common with type 'InvalidateQueryFilters'.
67         queryClient.invalidateQueries('projects');
                                         ~~~~~~~~~~
src/components/projects/ProjectForm.tsx:85:56 - error TS2339: Property 'nom' does not exist on type '{}'.
85         subtitle={isEdit ? `Modification de ${project?.nom}` : 'Création d\'un nouveau projet'}
                                                          ~~~
src/components/projects/ProjectForm.tsx:100:19 - error TS2322: Type 'string' is not assignable to type 'never'.
100                   name="code"
                      ~~~~
  node_modules/react-hook-form/dist/types/controller.d.ts:20:5
    20     name: TName;
           ~~~~
    The expected type comes from property 'name' which is declared here on type 'IntrinsicAttributes & { render: ({ field fieldState formState }: { field: ControllerRenderProps<{} never>; fieldState: ControllerFieldState; formState: UseFormStateReturn<...>; }) => ReactElement<...>; } & UseControllerProps<...>'
src/components/projects/ProjectForm.tsx:107:39 - error TS2339: Property 'code' does not exist on type 'FieldErrors<{}>'.
107                       error={!!errors.code}
                                          ~~~~
src/components/projects/ProjectForm.tsx:108:42 - error TS2339: Property 'code' does not exist on type 'FieldErrors<{}>'.
108                       helperText={errors.code?.message}
                                             ~~~~
src/components/projects/ProjectForm.tsx:116:19 - error TS2322: Type 'string' is not assignable to type 'never'.
116                   name="nom"
                      ~~~~
  node_modules/react-hook-form/dist/types/controller.d.ts:20:5
    20     name: TName;
           ~~~~
    The expected type comes from property 'name' which is declared here on type 'IntrinsicAttributes & { render: ({ field fieldState formState }: { field: ControllerRenderProps<{} never>; fieldState: ControllerFieldState; formState: UseFormStateReturn<...>; }) => ReactElement<...>; } & UseControllerProps<...>'
src/components/projects/ProjectForm.tsx:123:39 - error TS2339: Property 'nom' does not exist on type 'FieldErrors<{}>'.
123                       error={!!errors.nom}
                                          ~~~
src/components/projects/ProjectForm.tsx:124:42 - error TS2339: Property 'nom' does not exist on type 'FieldErrors<{}>'.
124                       helperText={errors.nom?.message}
                                             ~~~
src/components/projects/ProjectForm.tsx:132:19 - error TS2322: Type 'string' is not assignable to type 'never'.
132                   name="description"
                      ~~~~
  node_modules/react-hook-form/dist/types/controller.d.ts:20:5
    20     name: TName;
           ~~~~
    The expected type comes from property 'name' which is declared here on type 'IntrinsicAttributes & { render: ({ field fieldState formState }: { field: ControllerRenderProps<{} never>; fieldState: ControllerFieldState; formState: UseFormStateReturn<...>; }) => ReactElement<...>; } & UseControllerProps<...>'
src/components/projects/ProjectForm.tsx:141:39 - error TS2339: Property 'description' does not exist on type 'FieldErrors<{}>'.
141                       error={!!errors.description}
                                          ~~~~~~~~~~~
src/components/projects/ProjectForm.tsx:142:42 - error TS2339: Property 'description' does not exist on type 'FieldErrors<{}>'.
142                       helperText={errors.description?.message}
                                             ~~~~~~~~~~~
src/components/projects/ProjectForm.tsx:150:19 - error TS2322: Type 'string' is not assignable to type 'never'.
150                   name="date_debut"
                      ~~~~
  node_modules/react-hook-form/dist/types/controller.d.ts:20:5
    20     name: TName;
           ~~~~
    The expected type comes from property 'name' which is declared here on type 'IntrinsicAttributes & { render: ({ field fieldState formState }: { field: ControllerRenderProps<{} never>; fieldState: ControllerFieldState; formState: UseFormStateReturn<...>; }) => ReactElement<...>; } & UseControllerProps<...>'
src/components/projects/ProjectForm.tsx:159:43 - error TS2339: Property 'date_debut' does not exist on type 'FieldErrors<{}>'.
159                           error: !!errors.date_debut
                                              ~~~~~~~~~~
src/components/projects/ProjectForm.tsx:160:46 - error TS2339: Property 'date_debut' does not exist on type 'FieldErrors<{}>'.
160                           helperText: errors.date_debut?.message
                                                 ~~~~~~~~~~
src/components/projects/ProjectForm.tsx:170:19 - error TS2322: Type 'string' is not assignable to type 'never'.
170                   name="date_fin_prevue"
                      ~~~~
  node_modules/react-hook-form/dist/types/controller.d.ts:20:5
    20     name: TName;
           ~~~~
    The expected type comes from property 'name' which is declared here on type 'IntrinsicAttributes & { render: ({ field fieldState formState }: { field: ControllerRenderProps<{} never>; fieldState: ControllerFieldState; formState: UseFormStateReturn<...>; }) => ReactElement<...>; } & UseControllerProps<...>'
src/components/projects/ProjectForm.tsx:179:43 - error TS2339: Property 'date_fin_prevue' does not exist on type 'FieldErrors<{}>'.
179                           error: !!errors.date_fin_prevue
                                              ~~~~~~~~~~~~~~~
src/components/projects/ProjectForm.tsx:180:46 - error TS2339: Property 'date_fin_prevue' does not exist on type 'FieldErrors<{}>'.
180                           helperText: errors.date_fin_prevue?.message
                                                 ~~~~~~~~~~~~~~~
src/components/projects/ProjectForm.tsx:190:19 - error TS2322: Type 'string' is not assignable to type 'never'.
190                   name="budget"
                      ~~~~
  node_modules/react-hook-form/dist/types/controller.d.ts:20:5
    20     name: TName;
           ~~~~
    The expected type comes from property 'name' which is declared here on type 'IntrinsicAttributes & { render: ({ field fieldState formState }: { field: ControllerRenderProps<{} never>; fieldState: ControllerFieldState; formState: UseFormStateReturn<...>; }) => ReactElement<...>; } & UseControllerProps<...>'
src/components/projects/ProjectForm.tsx:198:39 - error TS2339: Property 'budget' does not exist on type 'FieldErrors<{}>'.
198                       error={!!errors.budget}
                                          ~~~~~~
src/components/projects/ProjectForm.tsx:199:42 - error TS2339: Property 'budget' does not exist on type 'FieldErrors<{}>'.
199                       helperText={errors.budget?.message}
                                             ~~~~~~
src/components/projects/ProjectForm.tsx:216:39 - error TS2339: Property 'isLoading' does not exist on type 'UseMutationResult<unknown Error void unknown>'.
  Property 'isLoading' does not exist on type 'Override<MutationObserverIdleResult<unknown Error void unknown> { mutate: UseMutateFunction<unknown Error void unknown>; }> & { ...; }'.
216                     loading={mutation.isLoading}
                                          ~~~~~~~~~
src/components/projects/ProjectsList.tsx:28:51 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(queryKey: "projects" options?: Omit<UseQueryOptions<unknown unknown unknown "projects"> "queryKey"> | undefined): UseQueryResult<unknown unknown>' gave the following error.
    Type '(page?: number size?: number filters?: { status?: string | undefined; search?: string | undefined; } | undefined) => Promise<ProjectList>' has no properties in common with type 'Omit<UseQueryOptions<unknown unknown unknown "projects"> "queryKey">'.
  Overload 2 of 3 '(queryKey: "projects" queryFn: QueryFunction<ProjectList "projects"> options?: Omit<UseQueryOptions<ProjectList unknown ProjectList "projects"> "queryKey" | "queryFn"> | undefined): UseQueryResult<...>' gave the following error.
    Argument of type '(page?: number size?: number filters?: { status?: string; search?: string; }) => Promise<ProjectList>' is not assignable to parameter of type 'QueryFunction<ProjectList "projects">'.
      Types of parameters 'page' and 'context' are incompatible.
        Type 'QueryFunctionContext<"projects" any>' is not assignable to type 'number'.
28   const { data: projects } = useQuery('projects' getProjects);
                                                     ~~~~~~~~~~~
src/components/projects/ProjectsList.tsx:30:38 - error TS2339: Property 'filter' does not exist on type '{}'.
30   const filteredProjects = projects?.filter(project =>
                                        ~~~~~~
src/components/projects/ProjectsList.tsx:30:45 - error TS7006: Parameter 'project' implicitly has an 'any' type.
30   const filteredProjects = projects?.filter(project =>
                                               ~~~~~~~
src/components/projects/ProjectsList.tsx:89:37 - error TS7006: Parameter 'project' implicitly has an 'any' type.
89             {filteredProjects?.map((project) => (
                                       ~~~~~~~
src/components/projects/ProjectTimeline.tsx:8:44 - error TS2307: Cannot find module 'react-big-calendar' or its corresponding type declarations.
8 import { Calendar dateFnsLocalizer } from 'react-big-calendar';
                                             ~~~~~~~~~~~~~~~~~~~~
src/components/projects/ProjectTimeline.tsx:31:57 - error TS2769: No overload matches this call.
  Overload 1 of 3 '(queryKey: "project-timeline" options?: Omit<UseQueryOptions<unknown unknown unknown "project-timeline"> "queryKey"> | undefined): UseQueryResult<unknown unknown>' gave the following error.
    Type '(projectId: string) => Promise<{ planned_start: string; planned_end: string; actual_start?: string | undefined; actual_end?: string | undefined; milestones: { date: string; description: string; completed: boolean; }[]; }>' has no properties in common with type 'Omit<UseQueryOptions<unknown unknown unknown "project-timeline"> "queryKey">'.
  Overload 2 of 3 '(queryKey: "project-timeline" queryFn: QueryFunction<{ planned_start: string; planned_end: string; actual_start?: string | undefined; actual_end?: string | undefined; milestones: { date: string; description: string; completed: boolean; }[]; } "project-timeline"> options?: Omit<...> | undefined): UseQueryResult<...>' gave the following error.
    Argument of type '(projectId: string) => Promise<{ planned_start: string; planned_end: string; actual_start?: string; actual_end?: string; milestones: Array<{ date: string; description: string; completed: boolean; }>; }>' is not assignable to parameter of type 'QueryFunction<{ planned_start: string; planned_end: string; actual_start?: string | undefined; actual_end?: string | undefined; milestones: { date: string; description: string; completed: boolean; }[]; } "project-timeline">'.
      Types of parameters 'projectId' and 'context' are incompatible.
        Type 'QueryFunctionContext<"project-timeline" any>' is not assignable to type 'string'.
31   const { data: events } = useQuery('project-timeline' getProjectTimeline);
                                                           ~~~~~~~~~~~~~~~~~~
src/components/projects/ProjectTimeline.tsx:58:31 - error TS7006: Parameter 'event' implicitly has an 'any' type.
58             eventPropGetter={(event) => ({
                                 ~~~~~
src/components/projects/TaskForm.tsx:23:50 - error TS6133: 'Task' is declared but its value is never read.
23 import { TaskStatus TaskPriority TaskCategory Task TaskFormData } from '../../types/task';
                                                    ~~~~
src/components/projects/TaskForm.tsx:300:23 - error TS2322: Type '{ label: string; render: (params: any) => Element; onChange: (...event: any[]) => void; onBlur: Noop; value: Date | undefined; disabled?: boolean | undefined; name: "start_date"; ref: RefCallBack; }' is not assignable to type 'IntrinsicAttributes & DatePickerProps<Date> & RefAttributes<HTMLDivElement>'.
  Property 'render' does not exist on type 'IntrinsicAttributes & DatePickerProps<Date> & RefAttributes<HTMLDivElement>'.
300                       render={(params) => (
                          ~~~~~~
src/components/projects/TaskForm.tsx:300:32 - error TS7006: Parameter 'params' implicitly has an 'any' type.
300                       render={(params) => (
                                   ~~~~~~
src/components/projects/TaskForm.tsx:322:23 - error TS2322: Type '{ label: string; renderInput: (params: any) => Element; onChange: (...event: any[]) => void; onBlur: Noop; value: Date; disabled?: boolean | undefined; name: "due_date"; ref: RefCallBack; }' is not assignable to type 'IntrinsicAttributes & DatePickerProps<Date> & RefAttributes<HTMLDivElement>'.
  Property 'renderInput' does not exist on type 'IntrinsicAttributes & DatePickerProps<Date> & RefAttributes<HTMLDivElement>'.
322                       renderInput={(params) => (
                          ~~~~~~~~~~~
src/components/projects/TaskForm.tsx:322:37 - error TS7006: Parameter 'params' implicitly has an 'any' type.
322                       renderInput={(params) => (
                                        ~~~~~~
src/components/projects/TasksOverview.tsx:17:10 - error TS2305: Module '"../../services/projects"' has no exported member 'getRecentTasks'.
17 import { getRecentTasks } from '../../services/projects';
            ~~~~~~~~~~~~~~
src/components/projects/TasksOverview.tsx:45:19 - error TS2339: Property 'map' does not exist on type '{}'.
45           {tasks?.map((task) => (
                     ~~~
src/components/projects/TasksOverview.tsx:45:24 - error TS7006: Parameter 'task' implicitly has an 'any' type.
45           {tasks?.map((task) => (
                          ~~~~
src/contexts/ThemeModeContext.tsx:2:25 - error TS6133: 'createTheme' is declared but its value is never read.
2 import { ThemeProvider createTheme } from '@mui/material/styles';
                          ~~~~~~~~~~~
src/hooks/useAuth.tsx:3:33 - error TS6133: 'LoginCredentials' is declared but its value is never read.
3 import { User AuthContextType LoginCredentials } from '../types/auth';
                                  ~~~~~~~~~~~~~~~~
src/routes/comptabilite.tsx:1:8 - error TS6133: 'React' is declared but its value is never read.
1 import React { lazy Suspense } from 'react';
         ~~~~~
src/routes/inventory.tsx:2:27 - error TS2307: Cannot find module '../components/inventory/InventoryPage' or its corresponding type declarations.
2 import InventoryPage from '../components/inventory/InventoryPage';
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/routes/inventory.tsx:3:25 - error TS2307: Cannot find module '../components/inventory/ProductForm' or its corresponding type declarations.
3 import ProductForm from '../components/inventory/ProductForm';
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/routes/inventory.tsx:4:28 - error TS2307: Cannot find module '../components/inventory/ProductDetails' or its corresponding type declarations.
4 import ProductDetails from '../components/inventory/ProductDetails';
                             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/services/hr.ts:42:36 - error TS6133: 'queryKey' is declared but its value is never read.
42 export const getEmployees = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'employees']>): Promise<Employee[]> => {
                                      ~~~~~~~~~~~~
src/services/hr.ts:96:33 - error TS6133: 'queryKey' is declared but its value is never read.
96 export const getLeaves = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'leaves']>): Promise<Leave[]> => {
                                   ~~~~~~~~~~~~
src/services/hr.ts:156:36 - error TS6133: 'queryKey' is declared but its value is never read.
156 export const getTrainings = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'trainings']>): Promise<Training[]> => {
                                       ~~~~~~~~~~~~
src/services/hr.ts:184:38 - error TS6133: 'queryKey' is declared but its value is never read.
184 export const getAttendances = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'attendances']>): Promise<Attendance[]> => {
                                         ~~~~~~~~~~~~
Found 362 errors in 103 files.
Errors  Files
     1  src/components/analytics/__tests__/ModuleImpactGrid.test.tsx:13
     1  src/components/comptabilite/__tests__/BudgetOverview.test.tsx:6
     1  src/components/comptabilite/__tests__/CashFlowChart.test.tsx:6
     2  src/components/comptabilite/ComptabilitePage.tsx:2
     7  src/components/comptabilite/ComptesList.tsx:20
     2  src/components/comptabilite/EcrituresForm.tsx:20
    17  src/components/comptabilite/JournauxList.tsx:17
     2  src/components/comptabilite/rapports/Bilan.tsx:17
     2  src/components/comptabilite/rapports/CompteResultat.tsx:17
     2  src/components/comptabilite/rapports/GrandLivre.tsx:20
     1  src/components/dashboard/__tests__/ActivitesRecentes.test.tsx:1
     1  src/components/dashboard/__tests__/DashboardPage.perf.tsx:23
     1  src/components/dashboard/__tests__/FinanceStats.test.tsx:11
     2  src/components/dashboard/__tests__/InventoryStats.test.tsx:4
     2  src/components/dashboard/__tests__/MLDashboard.test.tsx:4
     3  src/components/dashboard/__tests__/StatsFinance.test.tsx:1
     2  src/components/dashboard/__tests__/StatsProduction.test.tsx:1
     1  src/components/dashboard/__tests__/StatsRH.test.tsx:1
     2  src/components/dashboard/__tests__/WidgetMeteo.test.tsx:1
     1  src/components/dashboard/AlertsPanel.tsx:38
     9  src/components/dashboard/FinanceStats.tsx:7
     3  src/components/dashboard/HRStats.tsx:21
     1  src/components/dashboard/ModuleCard.tsx:20
     1  src/components/dashboard/modules/InventoryModule.tsx:15
     9  src/components/dashboard/StatisticsCards.tsx:6
     8  src/components/dashboard/StatsProduction.tsx:4
     1  src/components/documents/__tests__/DocumentList.test.tsx:5
     1  src/components/documents/__tests__/DocumentUploadDialog.test.tsx:5
     5  src/components/documents/DocumentList.tsx:20
     4  src/components/documents/DocumentUploadDialog.tsx:14
     3  src/components/finance/__tests__/AnalyseBudget.test.tsx:1
     2  src/components/finance/__tests__/BudgetOverview.test.tsx:4
     1  src/components/finance/__tests__/FinancePage.test.tsx:5
     7  src/components/finance/__tests__/FormulaireTransaction.test.tsx:1
     2  src/components/finance/__tests__/GraphiqueTresorerie.test.tsx:1
     5  src/components/finance/__tests__/ListeTransactions.test.tsx:1
     1  src/components/finance/__tests__/PageFinance.test.tsx:1
     1  src/components/finance/__tests__/ProjectionsFinancieres.test.tsx:1
     2  src/components/finance/__tests__/StatsFinance.test.tsx:1
     4  src/components/finance/__tests__/TransactionDetails.test.tsx:54
     3  src/components/finance/__tests__/TransactionForm.test.tsx:6
     1  src/components/finance/__tests__/TransactionList.test.tsx:5
     1  src/components/finance/__tests__/VueBudget.test.tsx:1
    12  src/components/finance/AnalyseBudget.tsx:20
     4  src/components/finance/CashFlowChart.tsx:63
     7  src/components/finance/FinanceStats.tsx:35
     9  src/components/finance/FormulaireTransaction.tsx:18
     7  src/components/finance/ListeTransactions.tsx:19
     1  src/components/finance/PageFinance.tsx:43
    10  src/components/finance/ProjectionsFinancieres.tsx:7
    19  src/components/finance/StatsFinance.tsx:6
     7  src/components/finance/TransactionDetails.tsx:153
    16  src/components/finance/TransactionForm.tsx:18
     5  src/components/finance/TransactionsList.tsx:19
     3  src/components/finance/VueBudget.tsx:16
     1  src/components/hr/__tests__/AttendanceChart.test.tsx:1
     1  src/components/hr/__tests__/AttendanceOverview.test.tsx:5
     2  src/components/hr/__tests__/EmployeeDetails.test.tsx:2
     2  src/components/hr/__tests__/EmployeeForm.test.tsx:6
     6  src/components/hr/__tests__/LeaveRequestForm.test.tsx:5
     1  src/components/hr/analytics/__tests__/HRAnalyticsDashboard.test.tsx:1
     1  src/components/hr/analytics/HRAnalyticsDashboard.tsx:7
     4  src/components/hr/AttendanceOverview.tsx:65
     1  src/components/hr/formation/__tests__/FormationForm.test.tsx:1
     1  src/components/hr/formation/__tests__/FormationList.test.tsx:1
     1  src/components/hr/formation/__tests__/FormationPage.test.tsx:1
     1  src/components/hr/types/formTypes.ts:1
     1  src/components/hr/weather/__tests__/CarteMeteo.test.tsx:1
     1  src/components/hr/weather/__tests__/TableauDeBordMeteo.test.tsx:1
     2  src/components/inventaire/__tests__/DetailsProduit.test.tsx:1
     1  src/components/inventaire/__tests__/DialogueMouvementStock.test.tsx:1
     2  src/components/inventaire/__tests__/FormulaireProduit.test.tsx:1
     4  src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:6
     3  src/components/inventaire/__tests__/ListeStock.test.tsx:14
     1  src/components/inventaire/__tests__/StatsInventaire.test.tsx:1
     7  src/components/inventaire/DetailsProduit.tsx:26
     6  src/components/inventaire/DialogueMouvementStock.tsx:86
     3  src/components/inventaire/FormulaireProduit.tsx:25
     1  src/components/inventaire/StatsInventaire.tsx:17
     1  src/components/parametrage/__tests__/ParametrageLayout.test.tsx:41
     1  src/components/parametrage/ConfigurationModules.tsx:10
     2  src/components/production/__tests__/ParcelleForm.test.tsx:6
     1  src/components/production/__tests__/ParcellesList.test.tsx:2
     2  src/components/production/__tests__/TableauMeteo.test.tsx:1
     1  src/components/production/HarvestQualityForm.tsx:98
     1  src/components/production/ParcelleMap.tsx:6
     4  src/components/production/RecolteForm.tsx:52
     1  src/components/projects/__tests__/ProjectDetails.test.tsx:1
     1  src/components/projects/__tests__/ProjectForm.test.tsx:1
     1  src/components/projects/__tests__/TaskForm.test.tsx:1
     1  src/components/projects/__tests__/TaskList.test.tsx:5
     1  src/components/projects/__tests__/TasksOverview.test.tsx:5
    12  src/components/projects/ProjectDetails.tsx:9
    25  src/components/projects/ProjectForm.tsx:10
     4  src/components/projects/ProjectsList.tsx:28
     3  src/components/projects/ProjectTimeline.tsx:8
     5  src/components/projects/TaskForm.tsx:23
     3  src/components/projects/TasksOverview.tsx:17
     1  src/contexts/ThemeModeContext.tsx:2
     1  src/hooks/useAuth.tsx:3
     1  src/routes/comptabilite.tsx:1
     3  src/routes/inventory.tsx:2
     4  src/services/hr.ts:42