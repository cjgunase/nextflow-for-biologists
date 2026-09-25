"""Tests for reading sample names from VCF headers."""

import pysam
import pytest

from ancestryflow.vcf import extract_vcf_samples, read_vcf_samples

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


def test_extracts_selected_donor_and_genotype(vcf_path, tmp_path):
    output = tmp_path / "selected.vcf"

    count = extract_vcf_samples(vcf_path, output, ["donor_01"])

    assert count == 1

    with pysam.VariantFile(str(output)) as result:
        assert list(result.header.samples) == ["donor_01"]
        records = list(result)

        assert len(records) == 1
        assert records[0].contig == "1"
        assert records[0].pos == 100
        assert records[0].alleles == ("A", "C")
        assert records[0].samples["donor_01"]["GT"] == (0, 0)


def test_extraction_rejects_missing_donor(vcf_path, tmp_path):
    output = tmp_path / "selected.vcf"

    with pytest.raises(ValueError, match="Requested samples not found"):
        extract_vcf_samples(vcf_path, output, ["missing_donor"])

    assert not output.exists()


def test_extraction_preserves_existing_output(vcf_path, tmp_path):
    output = tmp_path / "selected.vcf"
    output.write_text("existing content\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="Output already exists"):
        extract_vcf_samples(vcf_path, output, ["donor_01"])

    assert output.read_text(encoding="utf-8") == "existing content\n"