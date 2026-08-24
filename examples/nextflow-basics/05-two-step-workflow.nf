nextflow.enable.dsl=2

params.reads = "${projectDir}/data/reads/*_{R1,R2}.fastq"

process SUMMARIZE_READS {
    label 'small'
    tag "${sample_id}"

    input:
    tuple val(sample_id), path(reads)

    output:
    tuple val(sample_id), path("${sample_id}.counts.tsv"), emit: counts

    script:
    r1 = reads[0]
    r2 = reads[1]
    """
    r1_lines=\$(wc -l < ${r1})
    r2_lines=\$(wc -l < ${r2})
    test \$(( r1_lines % 4 )) -eq 0
    test \$(( r2_lines % 4 )) -eq 0

    printf 'sample\\tR1_reads\\tR2_reads\\n%s\\t%s\\t%s\\n' \\
      '${sample_id}' \\
      "\$(( r1_lines / 4 ))" \\
      "\$(( r2_lines / 4 ))" \\
      > ${sample_id}.counts.tsv
    """
}

process FORMAT_REPORT {
    label 'small'
    tag "${sample_id}"
    publishDir 'results/05-two-step', mode: 'copy'

    input:
    tuple val(sample_id), path(counts)

    output:
    path "${sample_id}.report.txt"

    script:
    """
    {
      echo 'Paired-read check'
      echo '================='
      cat ${counts}
    } > ${sample_id}.report.txt
    """
}

workflow {
    read_pairs = channel.fromFilePairs(params.reads, checkIfExists: true)
    SUMMARIZE_READS(read_pairs)
    FORMAT_REPORT(SUMMARIZE_READS.out.counts)
}
