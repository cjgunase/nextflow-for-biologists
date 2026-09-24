"""Tests for reading sample names from VCF headers."""

import pysam
import pytest

from ancestryflow.vcf import read_vcf_samples


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


def test_reads_samples_in_header_order(vcf_path):
    assert read_vcf_samples(vcf_path) == ["donor_02", "donor_01"]


def test_reads_bgzip_compressed_vcf(vcf_path):
    compressed = str(vcf_path) + ".gz"
    pysam.tabix_compress(str(vcf_path), compressed)
    pysam.tabix_index(compressed, preset="vcf")

    assert read_vcf_samples(compressed) == ["donor_02", "donor_01"]


def test_rejects_vcf_without_samples(tmp_path):
    path = tmp_path / "sites_only.vcf"
    path.write_text(
        "##fileformat=VCFv4.2\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="At least one sample ID"):
        read_vcf_samples(path)


def test_reports_missing_vcf(tmp_path):
    with pytest.raises(OSError):
        read_vcf_samples(tmp_path / "missing.vcf")
