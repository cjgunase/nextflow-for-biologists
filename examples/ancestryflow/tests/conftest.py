"""Shared pytest fixtures."""

import pytest

@pytest.fixture
def vcf_path(tmp_path):
    path = tmp_path / "example.vcf"
    path.write_text(
        "##fileformat=VCFv4.2\n"
        "##contig=<ID=1,length=248956422>\n"
        '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT"
        "\tdonor_02\tdonor_01\n"
        "1\t100\t.\tA\tC\t.\tPASS\t.\tGT\t0/1\t0/0\n",
        encoding="utf-8",
    )
    return path
