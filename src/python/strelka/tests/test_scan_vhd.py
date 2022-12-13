import datetime
from pathlib import Path
from unittest import TestCase, mock

from strelka.scanners.scan_vhd import ScanVhd


def test_scan_vhd(mocker):
    """
    This tests the ScanVhd scanner.
    It attempts to validate several given VHD metadata values.

    Pass: Sample event matches output of ScanVhd.
    Failure: Unable to load file or sample event fails to match.
    """

    test_scan_vhd_event = {
        "elapsed": mock.ANY,
        "flags": [],
        "total": {"files": 3, "extracted": 3},
        "files": [
            {
                "filename": "System Volume Information/WPSettings.dat",
                "size": "12",
                "datetime": "2022-12-11 21:12:12",
            },
            {
                "filename": "lorem.txt",
                "size": "4015",
                "datetime": "2022-12-11 21:12:55",
            },
            {
                "filename": "$RECYCLE.BIN/S-1-5-21-3712961497-200595429-3248382696-1000/desktop.ini",
                "size": "129",
                "datetime": "2022-12-11 21:13:31",
            },
        ],
        "hidden_dirs": [
            "System Volume Information",
            "$RECYCLE.BIN",
            "$RECYCLE.BIN/S-1-5-21-3712961497-200595429-3248382696-1000",
        ],
        "meta": {
            "paritions": [
                {"path": mock.ANY, "type": "GPT"},
                {"path": "0.Basic data partition.ntfs", "file_system": "Windows BDP"},
                {
                    "path": "0.Basic data partition.ntfs",
                    "type": "NTFS",
                    "label": "New Volume",
                    "file_system": "NTFS 3.1",
                    "created": "2022-12-11 21:12:11.6656282",
                },
            ]
        },
    }

    scanner = ScanVhd(
        {"name": "ScanVhd", "key": "scan_vhd", "limits": {"scanner": 10}},
        "test_coordinate",
    )

    mocker.patch.object(ScanVhd, "upload_to_coordinator", return_value=None)
    scanner.scan_wrapper(
        Path(Path(__file__).parent / "fixtures/test.vhd").read_bytes(),
        {"uid": "12345", "name": "somename"},
        {"scanner_timeout": 5},
        datetime.date.today(),
    )

    TestCase().assertDictEqual(test_scan_vhd_event, scanner.event)


def test_scan_vhdx(mocker):
    """
    This tests the ScanVhd scanner.
    It attempts to validate several given VHDX metadata values.

    Pass: Sample event matches output of ScanVhd.
    Failure: Unable to load file or sample event fails to match.
    """

    test_scan_vhd_event = {
        "elapsed": mock.ANY,
        "flags": [],
        "total": {"files": 3, "extracted": 3},
        "files": [
            {
                "filename": "System Volume Information/WPSettings.dat",
                "size": "12",
                "datetime": "2022-12-11 21:21:48",
            },
            {
                "filename": "lorem.txt",
                "size": "4015",
                "datetime": "2022-12-11 21:12:55",
            },
            {
                "filename": "$RECYCLE.BIN/S-1-5-21-3712961497-200595429-3248382696-1000/desktop.ini",
                "size": "129",
                "datetime": "2022-12-11 21:22:04",
            },
        ],
        "hidden_dirs": [
            "System Volume Information",
            "$RECYCLE.BIN",
            "$RECYCLE.BIN/S-1-5-21-3712961497-200595429-3248382696-1000",
        ],
        "meta": {
            "paritions": [
                {
                    "path": mock.ANY,
                    "type": "VHDX",
                    "creator_application": "Microsoft Windows 10.0.19044.0",
                },
                {"path": mock.ANY, "type": "GPT"},
                {"path": "0.Basic data partition.ntfs", "file_system": "Windows BDP"},
                {
                    "path": "0.Basic data partition.ntfs",
                    "type": "NTFS",
                    "label": "New Volume",
                    "file_system": "NTFS 3.1",
                    "created": "2022-12-11 21:21:47.4094722",
                },
            ]
        },
    }

    scanner = ScanVhd(
        {"name": "ScanVhd", "key": "scan_vhd", "limits": {"scanner": 10}},
        "test_coordinate",
    )

    mocker.patch.object(ScanVhd, "upload_to_coordinator", return_value=None)
    scanner.scan_wrapper(
        Path(Path(__file__).parent / "fixtures/test.vhdx").read_bytes(),
        {"uid": "12345", "name": "somename"},
        {"scanner_timeout": 5},
        datetime.date.today(),
    )

    TestCase().assertDictEqual(test_scan_vhd_event, scanner.event)
