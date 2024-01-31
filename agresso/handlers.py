import json
from datetime import datetime

from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.data.upload import Upload
from requests.exceptions import HTTPError

from agresso.service import (
    get_budget,
    get_budget_descriptions,
    get_general_ledger,
    get_user_log_contractor_invoices,
    get_workflow_comment_parked,
    get_workflow_contrator_invoices,
)

patch_all()


def import_dataset(dataset_id, data):
    print(f"Importing {len(data)} entries to dataset '{dataset_id}'...")

    dataset = Dataset()
    upload = Upload()

    try:
        version = dataset.get_latest_version(dataset_id)["version"]
    except HTTPError as e:
        if e.response.status_code == 404:
            print(f"Dataset '{dataset_id}' not found; skipping import")
            return
        raise

    edition = dataset.auto_create_edition(dataset_id, version)["Id"].split("/")[-1]

    with open(f"/tmp/{dataset_id}.json", "w") as tmpfile:
        tmpfile.write(json.dumps(data))
        tmpfile.seek(0)
        upload.upload(tmpfile.name, dataset_id, version, edition, 3)


@logging_wrapper
@xray_recorder.capture("import_datasets")
def import_datasets(event, context):
    import_dataset("arbeidsflyt-levfakt-wf68", get_workflow_contrator_invoices())
    import_dataset("brukerlog-levfakt-wf80", get_user_log_contractor_invoices())
    import_dataset("arbeidsflyt-kommentar-parkert", get_workflow_comment_parked())

    now = datetime.now()
    for year in [now.year, now.year - 1]:
        import_dataset(f"hovedbok-gl11-{year}", get_general_ledger(year))
        import_dataset(f"budsjett-{year}", get_budget(year))
        import_dataset(f"budsjett-beskrivelse-{year}", get_budget_descriptions(year))
