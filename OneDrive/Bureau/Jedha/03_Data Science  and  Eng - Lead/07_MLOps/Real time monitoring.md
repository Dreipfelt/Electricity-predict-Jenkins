Continuous Monitoring
Real time monitoring ☁️
60 min
What you will learn in this course 🧐🧐

While reading reports from a notebook is useful, in the context of MLOps you will want to update some kind of Dashboard automatically. Fortunately for us, evidently offers this great feature. In this course, you will learn:

    How to use Evidently Cloud

    How to log data on a remote evidently dashboard

    https://docs.evidentlyai.com/tutorials-and-examples/tutorial-cloud

Create your Evidently Cloud Account

If you haven't already, you will need to create an account on Evidently:

    Go to https://www.evidentlyai.com/register
    Register & verify your email

If everything went smoothly, you should land to this page:

You will be asked to create a Team and a demo project. You can definitely do so, but no matter what, the code below will show you how to create those using the Python SDK.
Get your Evidently Token

Now the most important element you should get from your evidently cloud interface is a token. To generate one, simply:

    Go to Personal Tokens
    Click on Generate Token
    Save your token somewhere safe 🔐

Alright now that you have your basic setup, we can move on to the next steps 😉
Install Evidently client

If you haven't done it already, you need to install evidently on your client device. You can either run:

    pip install evidently directly on a notebook
    Or pull an image like: jedha/sample-evidently-app and run it in a docker container with the following command:
        docker run -it -p 8888:8888 -v $(pwd):/home sample-evidently-app

Import Libraries

import pandas as pd
import datetime
from evidently.ui.workspace.cloud import CloudWorkspace

from evidently.report import Report

from evidently import metrics
from evidently.metric_preset import DataQualityPreset
from evidently.metric_preset import DataDriftPreset

from evidently.test_suite import TestSuite
from evidently.tests import *
from evidently.test_preset import DataDriftTestPreset
from evidently.tests.base_test import TestResult, TestStatus
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import DashboardPanelTestSuite
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.dashboards import TestFilter
from evidently.ui.dashboards import TestSuitePanelType
from evidently.renderers.html_widgets import WidgetSize

Load Data

For the following demo, we will be using datasets measuring employees performance over the years. We have three datasets:

    employee_performance_2022.csv
    employee_performance_2023.csv
    employee_performance_2024.csv

past = pd.read_csv("src/02-sample-evidently-app/data/employee_performance_2022.csv")
reference = pd.read_csv("src/02-sample-evidently-app/data/employee_performance_2023.csv")
current = pd.read_csv("src/02-sample-evidently-app/data/employee_performance_2024.csv")

Connect to Evidently Cloud

Now to connect our client to our Evidently Cloud interface, we will use the CloudWorkspace class:

TOKEN="REPLACE_BY_YOUR_TOKEN"

ws = CloudWorkspace(
token=TOKEN,
url="https://app.evidently.cloud")

Create a Team

If you haven't created a team, you can very easily do so like this:

ws.create_team("My team name", org_id="YOUR ORG ID HERE")

Team(id=UUID('01970ce3-f932-7838-81a7-d8a7ffc2de0b'), name='lead-example', org_id=UUID('019270a8-271d-7818-a31d-3e77dc7df446'))

Your ORG ID can be found here:

Create a Project

If you haven't created a project already, you can do so like this.

project = ws.create_project("employee_performance", team_id="01970ce3-f932-7838-81a7-d8a7ffc2de0b")
project.description = "Study on what drives employees performance"
project.save()

Project(id=UUID('01970cf2-5175-76b1-a490-2aaae3e61494'), name='employee_performance', description='Study on what drives employees performance', dashboard=DashboardConfig(name='employee_performance', panels=[], tabs=[], tab_id_to_panel_ids={}), team_id=UUID('01970ce3-f932-7838-81a7-d8a7ffc2de0b'), org_id=UUID('019270a8-271d-7818-a31d-3e77dc7df446'), date_from=None, date_to=None, created_at=datetime.datetime(2025, 5, 26, 16, 14, 56, 630066))

If you did created a project, you can use: ws.get_project("YOUR_PROJECT_ID") more on that in the sections below 👇
Compute snapshots

As we've seen in the previous lecture, running a report can be done using Report class. Now the cool thing is that you can generate this report locally or you can send the report back to your Evidently Cloud application:

data_report = Report(
        metrics=[
            DataDriftPreset(stattest='psi', stattest_threshold='0.3'),
            DataQualityPreset(),
        ],
        timestamp=datetime.datetime.now(),
    )

data_report.run(reference_data=reference, current_data=current)

# Send report to Evidently Cloud
# ws.add_report(project.id, data_report)

# Send report including the dataset
ws.add_report(project.id, data_report, include_data=True)

Now go back your Evidently Cloud application, click on your project and go to the Reports section, then click on Explore. You should see all your report created above:

Load Datasets from evidently cloud

If you've uploaded datasets to Evidently cloud, you can get them back simply by using the load_dataset method.

#download dataset from the project
downloaded_data_from_the_project = ws.load_dataset(dataset_id = "01970cf5-3293-7e25-b328-33090bedc2cd")
downloaded_data_from_the_project.head()

   EmployeeID Department  YearsAtCompany OverTime  Age               JobRole  \
0           1  Marketing               9       No   40  Marketing Specialist
1           2    Finance              20       No   57            Accountant
2           3         HR              17       No   33            HR Manager
3           4    Finance              17       No   40     Financial Analyst
4           5    Finance              20      Yes   33     Financial Analyst

   MonthlyIncome  PerformanceRating  WorkLifeBalance  SatisfactionScore  \
0           5655                5.0                5                6.0
1           8400                5.0                5                6.0
2           8880                5.0                5                6.0
3           9435                5.0                4                5.5
4          10200                5.0                3                5.0

   TrainingHoursLastYear
0                     19
1                     32
2                     22
3                     27
4                     29

Your dataset ID can be found here:

#when you upload data to a project a column mapping may be specified as well
ws.add_dataset(
    past,
    name = "2022 Employee Performance",
    project_id = project.id)

UUID('227810b3-5a22-49e4-b87d-58555f2044d2')

Add custom panels

Custom panels are specific views of your tests & monitoring dashboard, you can customize them directly with your SDK. First you will need to get your project id here:

project = ws.get_project("YOUR_PROJECT_ID")

project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Daily inference Count",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
            	PanelValue(
                	metric_id="DatasetSummaryMetric",
                	field_path=metrics.DatasetSummaryMetric.fields.current.number_of_rows,
                	legend="count",
            	),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.FULL,
        ),
        tab="Summary"
    )
project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Share of drifting features (PSI > 0.3)",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                	metric_id="DatasetDriftMetric",
                	field_path="share_of_drifted_columns",
                	legend="share",
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.FULL,
        ),
        tab="Summary"
)
project.save()

Project(id=UUID('01970cf2-5175-76b1-a490-2aaae3e61494'), name='employee_performance', description='Study on what drives employees performance', dashboard=DashboardConfig(name='employee_performance', panels=[DashboardPanelPlot(type='evidently:dashboard_panel:DashboardPanelPlot', id=UUID('01970d0e-8eb2-75b6-8038-53d72447ee54'), title='Daily inference Count', filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=False), size=<WidgetSize.FULL: 2>, values=[PanelValue(field_path='current.number_of_rows', metric_id='DatasetSummaryMetric', metric_fingerprint=None, metric_args={}, legend='count')], plot_type=<PlotType.LINE: 'line'>), DashboardPanelPlot(type='evidently:dashboard_panel:DashboardPanelPlot', id=UUID('01970d0e-8eb4-7243-af2f-632cb45045be'), title='Share of drifting features (PSI > 0.3)', filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=False), size=<WidgetSize.FULL: 2>, values=[PanelValue(field_path='share_of_drifted_columns', metric_id='DatasetDriftMetric', metric_fingerprint=None, metric_args={}, legend='share')], plot_type=<PlotType.LINE: 'line'>)], tabs=[DashboardTab(id=UUID('01970d0e-8eb3-7baf-9f99-e202a9df397a'), title='Summary')], tab_id_to_panel_ids={'01970d0e-8eb3-7baf-9f99-e202a9df397a': ['01970d0e-8eb2-75b6-8038-53d72447ee54', '01970d0e-8eb4-7243-af2f-632cb45045be']}), team_id=UUID('01970ce3-f932-7838-81a7-d8a7ffc2de0b'), org_id=UUID('019270a8-271d-7818-a31d-3e77dc7df446'), date_from=None, date_to=None, created_at=datetime.datetime(2025, 5, 26, 16, 14, 56, 630066))

Run tests

Finally, you can run any specific test you want and upload them onto your Evidently dashboard:

drift_tests = TestSuite(
    tests=[
        DataDriftTestPreset(stattest_threshold=0.3),
        TestShareOfMissingValues(lte=0.05),
        TestNumberOfConstantColumns(eq=0),
        TestNumberOfEmptyRows(eq=0),
        TestNumberOfEmptyColumns(eq=0),
        TestNumberOfDuplicatedColumns(eq=0)
    ])

drift_tests.run(reference_data=reference, current_data=current)
ws.add_test_suite(project.id, drift_tests)

Once our tests have run we can add the tests to the dashboard testing panel.

project.dashboard.add_panel(
        DashboardPanelTestSuite(
            title="Data quality tests",
            test_filters=[
                TestFilter(test_id="TestNumberOfConstantColumns", test_args={}),
                TestFilter(test_id="TestShareOfMissingValues", test_args={}),
                TestFilter(test_id="TestNumberOfEmptyRows", test_args={}),
                TestFilter(test_id="TestNumberOfEmptyColumns", test_args={}),
                TestFilter(test_id="TestNumberOfDuplicatedColumns", test_args={}),
            ],
            filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
            size=WidgetSize.FULL,
            panel_type=TestSuitePanelType.DETAILED,
            time_agg="1D",
        ),
        tab="Data Tests"
)
project.dashboard.add_panel(
        DashboardPanelTestSuite(
            title="Data drift per column in time",
            test_filters=[
                TestFilter(test_id="TestColumnDrift", test_args={}),
            ],
            filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
            size=WidgetSize.FULL,
            panel_type=TestSuitePanelType.DETAILED,
            time_agg="1D",
        ),
        tab="Data Tests"
)
project.save()

Project(id=UUID('01970cf2-5175-76b1-a490-2aaae3e61494'), name='employee_performance', description='Study on what drives employees performance', dashboard=DashboardConfig(name='employee_performance', panels=[DashboardPanelPlot(type='evidently:dashboard_panel:DashboardPanelPlot', id=UUID('01970d0e-8eb2-75b6-8038-53d72447ee54'), title='Daily inference Count', filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=False), size=<WidgetSize.FULL: 2>, values=[PanelValue(field_path='current.number_of_rows', metric_id='DatasetSummaryMetric', metric_fingerprint=None, metric_args={}, legend='count')], plot_type=<PlotType.LINE: 'line'>), DashboardPanelPlot(type='evidently:dashboard_panel:DashboardPanelPlot', id=UUID('01970d0e-8eb4-7243-af2f-632cb45045be'), title='Share of drifting features (PSI > 0.3)', filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=False), size=<WidgetSize.FULL: 2>, values=[PanelValue(field_path='share_of_drifted_columns', metric_id='DatasetDriftMetric', metric_fingerprint=None, metric_args={}, legend='share')], plot_type=<PlotType.LINE: 'line'>), DashboardPanelTestSuite(type='evidently:dashboard_panel:DashboardPanelTestSuite', id=UUID('01970d11-a800-7479-8c44-d5dbd145638b'), title='Data quality tests', filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True), size=<WidgetSize.FULL: 2>, test_filters=[TestFilter(test_id='TestNumberOfConstantColumns', test_fingerprint=None, test_args={}), TestFilter(test_id='TestShareOfMissingValues', test_fingerprint=None, test_args={}), TestFilter(test_id='TestNumberOfEmptyRows', test_fingerprint=None, test_args={}), TestFilter(test_id='TestNumberOfEmptyColumns', test_fingerprint=None, test_args={}), TestFilter(test_id='TestNumberOfDuplicatedColumns', test_fingerprint=None, test_args={})], panel_type=<TestSuitePanelType.DETAILED: 'detailed'>, time_agg='1D'), DashboardPanelTestSuite(type='evidently:dashboard_panel:DashboardPanelTestSuite', id=UUID('01970d11-a802-7d66-bdf3-54de7f0b3d42'), title='Data drift per column in time', filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True), size=<WidgetSize.FULL: 2>, test_filters=[TestFilter(test_id='TestColumnDrift', test_fingerprint=None, test_args={})], panel_type=<TestSuitePanelType.DETAILED: 'detailed'>, time_agg='1D')], tabs=[DashboardTab(id=UUID('01970d0e-8eb3-7baf-9f99-e202a9df397a'), title='Summary'), DashboardTab(id=UUID('01970d11-a801-7738-a9c0-e0905b030a4c'), title='Data Tests')], tab_id_to_panel_ids={'01970d0e-8eb3-7baf-9f99-e202a9df397a': ['01970d0e-8eb2-75b6-8038-53d72447ee54', '01970d0e-8eb4-7243-af2f-632cb45045be'], '01970d11-a801-7738-a9c0-e0905b030a4c': ['01970d11-a800-7479-8c44-d5dbd145638b', '01970d11-a802-7d66-bdf3-54de7f0b3d42']}), team_id=UUID('01970ce3-f932-7838-81a7-d8a7ffc2de0b'), org_id=UUID('019270a8-271d-7818-a31d-3e77dc7df446'), date_from=None, date_to=None, created_at=datetime.datetime(2025, 5, 26, 16, 14, 56, 630066))

Resources 📚📚

    Tutorial - Data & ML Monitoring
