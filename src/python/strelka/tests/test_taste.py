import redis
import yaml

from pathlib import Path
from unittest import TestCase, mock

from strelka import strelka


def test_taste(mocker) -> None:
    """
    Pass: All test fixtures match the given yara and mime matches.
    Failure: At least one test fixture does not match the given yara and mime matches.
    """

    test_taste: dict = {
        "test.7z": [{"mime": ["application/x-7z-compressed"], "yara": ["_7zip_file"]}],
        "test.b64": [{"mime": ["text/plain"], "yara": []}],  # No file-specific match
        "test.bat": [{"mime": ["text/x-msdos-batch"], "yara": []}],  # Not in backend.cfg
        "test.bz2": [{"mime": ["application/x-bzip2"], "yara": ["bzip2_file"]}],
        "test.cpio": [{"mime": ["application/x-cpio"], "yara": []}],
        "test.deb": [
            {
                "mime": ["application/vnd.debian.binary-package"],
                "yara": ["debian_package_file"],
            }
        ],
        "test.der": [{"mime": ["application/octet-stream"], "yara": ["x509_der_file"]}],
        "test.dmg": [
            {"mime": ["application/octet-stream"], "yara": ["hfsplus_disk_image"]}
        ],
        "test.doc": [{"mime": ["application/msword"], "yara": ["olecf_file"]}],
        "test.docx": [
            {
                "mime": [
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ],
                "yara": ["ooxml_file"],
            }
        ],
        "test.elf": [{"mime": ["application/x-sharedlib"], "yara": ["elf_file"]}],
        "test.eml": [{"mime": ["message/rfc822"], "yara": ["email_file"]}],
        "test.empty": [{"mime": ["application/x-empty"], "yara": []}],
        "test.exe": [{"mime": ["application/x-dosexec"], "yara": ["mz_file"]}],
        "test.gif": [{"mime": ["image/gif"], "yara": ["gif_file"]}],
        "test.gz": [{"mime": ["application/gzip"], "yara": ["gzip_file"]}],
        "test.html": [{"mime": ["text/html"], "yara": ["html_file"]}],
        "test.ini": [{"mime": ["text/plain"], "yara": ["ini_file"]}],
        "test.iso": [{"mime": ["application/x-iso9660-image"], "yara": ["iso_file"]}],
        "test.jpg": [{"mime": ["image/jpeg"], "yara": ["jpeg_file"]}],
        "test.js": [{"mime": ["text/plain"], "yara": ["javascript_file"]}],
        "test.json": [{"mime": ["application/json"], "yara": ["json_file"]}],
        "test.lnk": [{"mime": ["application/octet-stream"], "yara": ["lnk_file"]}],
        "test.macho": [{"mime": ["application/x-mach-binary"], "yara": ["macho_file"]}],
        "test.msi": [{"mime": ["application/vnd.ms-msi"], "yara": ["olecf_file"]}],  # CDF format needs subtypes
        "test.pdf": [{"mime": ["application/pdf"], "yara": ["pdf_file"]}],
        "test.pem": [{"mime": ["text/plain"], "yara": ["x509_pem_file"]}],
        "test.png": [{"mime": ["image/png"], "yara": ["png_file"]}],
        "test.rar": [{"mime": ["application/x-rar"], "yara": ["rar_file"]}],
        "test.tar": [{"mime": ["application/x-tar"], "yara": ["tar_file"]}],
        "test.txt": [{"mime": ["text/plain"], "yara": []}],
        "test.url": [{"mime": ["text/plain"], "yara": []}],
        "test.vhd": [{"mime": ["application/octet-stream"], "yara": ["vhd_file"]}],
        "test.vhdx": [{"mime": ["application/octet-stream"], "yara": ["vhdx_file"]}],
        "test.xar": [{"mime": ["application/x-xar"], "yara": ["xar_file"]}],
        "test.xml": [{"mime": ["text/xml"], "yara": ["xml_file"]}],
        "test.xz": [{"mime": ["application/x-xz"], "yara": ["xz_file"]}],
        "test.yara": [{"mime": ["text/plain"], "yara": []}],
        "test.zip": [{"mime": ["application/zip"], "yara": ["zip_file"]}],
        "test_aes256_password.zip": [
            {"mime": ["application/zip"], "yara": ["encrypted_zip", "zip_file"]}
        ],
        "test_broken_iend.png": [{"mime": ["image/png"], "yara": ["png_file"]}],
        "test_lzx.cab": [
            {"mime": ["application/vnd.ms-cab-compressed"], "yara": ["cab_file"]}
        ],
        "test_manifest.json": [
            {"mime": ["application/json"], "yara": ["browser_manifest", "json_file"]}
        ],
        "test_password.doc": [{"mime": ["application/msword"], "yara": ["olecf_file"]}],
        "test_password.docx": [
            {
                "mime": ["application/encrypted"],
                "yara": ["encrypted_word_document", "olecf_file"],
            }
        ],
        "test_password_brute.doc": [
            {"mime": ["application/msword"], "yara": ["olecf_file"]}
        ],
        "test_password_brute.docx": [
            {
                "mime": ["application/encrypted"],
                "yara": ["encrypted_word_document", "olecf_file"],
            }
        ],
        "test_pe.b64": [{"mime": ["text/plain"], "yara": ["base64_pe"]}],
        "test_pe_overlay.bmp": [{"mime": ["image/bmp"], "yara": ["bmp_file"]}],
        "test_pe_overlay.jpg": [{"mime": ["image/jpeg"], "yara": ["jpeg_file"]}],
        "test_pe_overlay.png": [{"mime": ["image/png"], "yara": ["png_file"]}],
        "test_pii.csv": [{"mime": ["text/csv"], "yara": ["credit_cards"]}],
        "test_qr.png": [{"mime": ["image/png"], "yara": ["png_file"]}],
        "test_readonly.dmg": [
            {"mime": ["application/octet-stream"], "yara": ["dmg_disk_image"]}
        ],  # Missing taste
        "test_readwrite.dmg": [{"mime": ["application/octet-stream"], "yara": []}],
        "test_text.jpg": [{"mime": ["image/jpeg"], "yara": ["jpeg_file"]}],
        "test_upx.exe": [
            {"mime": ["application/x-dosexec"], "yara": ["mz_file", "upx_file"]}
        ],
        "test_xor.exe": [{"mime": ["application/x-dosexec"], "yara": ["mz_file"]}],
        "test_zip.cab": [
            {"mime": ["application/vnd.ms-cab-compressed"], "yara": ["cab_file"]}
        ],
        "test_zip_password.zip": [
            {"mime": ["application/zip"], "yara": ["encrypted_zip", "zip_file"]}
        ],
    }

    test_fixtures = sorted(
        list(Path(Path(__file__).parent / "fixtures/").glob("test*"))
    )

    backend_cfg_path: str = "/etc/strelka/backend.yaml"

    with open(backend_cfg_path, "r") as f:
        backend_cfg = yaml.safe_load(f.read())

        coordinator = redis.StrictRedis(host="127.0.0.1", port=65535, db=0)

        backend = strelka.Backend(backend_cfg, coordinator)

        taste = {}

        for test_fixture in test_fixtures:
            with open(
                Path(Path(__file__).parent / f"fixtures/{test_fixture.name}"), "rb"
            ) as test_file:
                entries = []
                data = test_file.read()
                entries.append(backend.match_flavors(data))
                taste[test_fixture.name] = entries

        TestCase.maxDiff = None
        TestCase().assertDictEqual(test_taste, taste)
